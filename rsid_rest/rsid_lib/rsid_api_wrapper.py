# -*- coding: utf-8 -*-
# Copyright (C) 2018-2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

import asyncio
import copy
import math
import os
import threading
import uuid
from pathlib import Path

import cv2
import numpy as np
from . import rsid_py
from cv2.typing import MatLike
from fastapi.concurrency import run_in_threadpool
from loguru import logger
from simplejpeg import encode_jpeg
from starlette.responses import AsyncContentStream

from . import models
from .gen.models import AuthenticateStatusEnum
from .host_db_local_file import HostDBLocalFile
from .models import AuthenticationResponse, DeviceInfoResponse, EnrollResponse
from .models import FaceRect as FaceRectModel
from ..core.config import get_app_settings
from ..core.settings.base import HostModeAuthTypes, StreamEncodingStypes

if os.name == "nt":  # sys.platform == 'win32':
    from serial.tools.list_ports_windows import comports
elif os.name == "posix":
    from serial.tools.list_ports_posix import comports
else:
    raise ImportError(f"Sorry: no implementation for your platform ('{os.name}') available")


class RSIDApiWrapper:
    _instance = None
    _lock = threading.Lock()
    _condition = asyncio.Condition()
    _preview_condition = threading.Condition()
    _preview: rsid_py.Preview | None = None
    _preview_tickets: list[uuid.UUID] = []
    _preview_image = None
    _preview_encoder_lock = threading.Lock()

    def __init__(self):
        self.db = HostDBLocalFile()
        self._port = None

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def set_port(self, port: str):
        with self._lock:
            self._port = port

    async def auth(self) -> AuthenticationResponse:
        logger.info(f"authenticating with {self._port}")

        auth_result: rsid_py.AuthenticateStatus | None = None
        user_id: str | None = None
        faces: list[rsid_py.FaceRect] | None = None
        exception: Exception | None = None

        def on_hint(hint: rsid_py.AuthenticateStatus | None, score: float | None):
            # TODO: Publish on websocket
            logger.debug(f"on_hint {hint}")

        def on_result(result: rsid_py.AuthenticateStatus, result_user_id: str):
            nonlocal auth_result
            nonlocal user_id
            user_id = result_user_id
            success = result == rsid_py.AuthenticateStatus.Success
            auth_result = result
            logger.debug(f'Success "{user_id}"' if success else str(result))
            self._condition.notify()

        def on_faces(face_rects: list[rsid_py.FaceRect], timestamp: int):
            nonlocal faces
            # TODO: Publish on websocket
            faces = []
            for face in face_rects:
                faces.append(FaceRectModel.from_rsid_face_rect(face))
            logger.debug(f"detected {len(faces)} face(s)")

        with self._lock:
            async with self._condition:
                with rsid_py.FaceAuthenticator(self._port) as authenticator:
                    try:
                        authenticator.authenticate(
                            on_hint=on_hint,
                            on_result=on_result,
                            on_faces=on_faces,
                        )
                    except Exception as e:
                        logger.error(e)
                        exception = e
                    finally:
                        authenticator.disconnect()
                await self._condition.wait_for(lambda: auth_result is not None)

        if exception is not None:
            raise exception
        return AuthenticationResponse(
            user_id=user_id,
            faces=faces,
            status=AuthenticateStatusEnum.from_rsid_py(auth_result),
        )

    async def auth_host(self) -> AuthenticationResponse:
        logger.info(f"authenticating with {self._port}")

        auth_result: rsid_py.AuthenticateStatus | None = None
        extracted_faceprints: rsid_py.ExtractedFaceprintsElement | None = None
        faces: list[rsid_py.FaceRect] | None = None
        exception: Exception | None = None
        best_match_updated_faceprints: rsid_py.Faceprints | None = None
        best_match_db_record = None

        def on_hint(hint: rsid_py.AuthenticateStatus | None, score: float | None):
            # SDK Context
            # TODO: Publish on websocket
            logger.debug(f"on_hint {hint}")

        def on_faces(face_rects: list[rsid_py.FaceRect], timestamp: int):
            # SDK Context
            nonlocal faces
            # TODO: Publish on websocket?
            faces = []
            for face in face_rects:
                faces.append(FaceRectModel.from_rsid_face_rect(face))
            logger.debug(f"detected {len(faces)} face(s)")

        def on_result(
            result: rsid_py.AuthenticateStatus,
            faceprints: rsid_py.ExtractedFaceprintsElement,
        ):
            # SDK Context
            nonlocal auth_result
            nonlocal extracted_faceprints
            auth_result = result
            if faceprints is not None:
                # pybindings issue:
                #   extracted_faceprints value destroyed after leaving SDK context
                #   don't use extracted_faceprints = faceprints
                #   use copy instead
                extracted_faceprints = copy.copy(faceprints)
            self._condition.notify()

        with self._lock:
            async with self._condition:
                with rsid_py.FaceAuthenticator(self._port) as authenticator:
                    try:
                        authenticator.extract_faceprints_for_auth(
                            on_result=on_result, on_hint=on_hint, on_faces=on_faces
                        )
                    except Exception as e:
                        logger.error(e)
                        exception = e
                    finally:
                        authenticator.disconnect()

                # Wait for callback response.
                await self._condition.wait_for(lambda: auth_result is not None)

                if exception is not None:
                    raise exception

                if auth_result != rsid_py.AuthenticateStatus.Success:
                    return AuthenticationResponse(
                        user_id=None,
                        faces=faces,
                        status=AuthenticateStatusEnum.from_rsid_py(auth_result),
                    )

                faceprints_db: list = []
                if get_app_settings().host_mode_auth_type == HostModeAuthTypes.hybrid:
                    faceprints_db = await self.db.get_faceprints(extracted_faceprints)
                elif get_app_settings().host_mode_auth_type == HostModeAuthTypes.device:
                    faceprints_db = await self.db.get_all_faceprints()

                logger.info(f"Searching in {len(faceprints_db)} DB faceprints...")

                max_score = -100
                for i, db_record in enumerate(faceprints_db):
                    db_faceprints = rsid_py.Faceprints()
                    db_faceprints.flags = db_record["flags"]
                    db_faceprints.version = db_record["version"]
                    db_faceprints.features_type = db_record["features_type"]
                    db_faceprints.adaptive_descriptor_nomask = db_record["adaptive_descriptor_nomask"]
                    db_faceprints.adaptive_descriptor_withmask = db_record["adaptive_descriptor_withmask"]
                    db_faceprints.enroll_descriptor = db_record["enroll_descriptor"]

                    out_faceprints = rsid_py.Faceprints()
                    # TODO: Grab MatcherConfidenceLevel from device
                    match_result = authenticator.match_faceprints(
                        extracted_faceprints,
                        db_faceprints,
                        out_faceprints,
                        # rsid_py.MatcherConfidenceLevel.High,
                    )
                    logger.debug(f"match_result for user {i}: {match_result}")
                    if match_result.success:
                        logger.info(f"Match success for user {i} with score {match_result.score}")
                        if match_result.score > max_score:
                            max_score = match_result.score
                            best_match_db_record = db_record
                            best_match_updated_faceprints = out_faceprints

        if best_match_db_record is None:
            # Return with Forbidden status
            return AuthenticationResponse(user_id=None, faces=faces, status=AuthenticateStatusEnum.Forbidden)

        user_id = best_match_db_record["user_id"]

        if match_result.should_update:
            await self.db.update_faceprints(user_id, best_match_updated_faceprints)

        return AuthenticationResponse(
            user_id=user_id,
            faces=faces,
            status=AuthenticateStatusEnum.from_rsid_py(auth_result),
        )

    async def enroll(self, user_id: str) -> EnrollResponse:
        logger.info(f"enrolling user: {user_id}")

        enroll_result: rsid_py.EnrollStatus | None = None
        exception: Exception | None = None

        def on_progress(face_pose: rsid_py.FacePose):
            # TODO: Publish on websocket?
            logger.debug(f"on_progress {face_pose}")

        def on_hint(hint: rsid_py.EnrollStatus | None, score: float | None):
            # TODO: Publish on websocket?
            logger.debug(f"on_hint {hint}")

        def on_result(result: rsid_py.EnrollStatus, uid: str | None = None):
            nonlocal enroll_result
            success = result == rsid_py.EnrollStatus.Success
            enroll_result = result
            logger.debug(f'Success "{uid}"' if success else str(result))
            self._condition.notify()

        def on_faces(faces: list[rsid_py.FaceRect], timestamp: int):
            # TODO: Publish on websocket?
            logger.debug(f"detected {len(faces)} face(s)")

        with self._lock:
            async with self._condition:
                with rsid_py.FaceAuthenticator(self._port) as authenticator:
                    try:
                        await run_in_threadpool(authenticator.enroll,
                                                on_hint=on_hint,
                                                on_progress=on_progress,
                                                on_result=on_result,
                                                on_faces=on_faces,
                                                user_id=user_id,
                                                )
                    except Exception as e:
                        exception = e
                        logger.error(e)
                    finally:
                        authenticator.disconnect()

                await self._condition.wait_for(lambda: enroll_result is not None)

        if exception is not None:
            raise exception
        return EnrollResponse(user_id=user_id, status=models.EnrollStatusEnum.from_rsid_py(enroll_result))

    def _resize_if_big(self, im_cv: MatLike) -> MatLike:
        # TODO: Review this logic to match the one in C# instead.
        max_enroll_image_size: int = 890 * 1024  # Max allowed buffer to enroll is 900kb
        img_size = math.prod(im_cv.shape)

        if im_cv.shape[2] != 3:  # channels
            raise ValueError("image must have 3 channels / bgr24")

        if img_size > max_enroll_image_size:
            scale = math.sqrt(max_enroll_image_size / img_size)
            im_cv: MatLike = cv2.resize(im_cv, (0, 0), fx=scale, fy=scale)
            img_size_kb = int(math.prod(im_cv.shape) / 1024)
            logger.info(f"Scaled down to {im_cv.shape[1]}x{im_cv.shape[0]} ({img_size_kb} KB) to fit max size")
        return im_cv

    async def enroll_image(self, user_id: str, file_path: Path) -> EnrollResponse:
        exception: Exception | None = None
        image = await run_in_threadpool(self._resize_if_big, (cv2.imread(str(file_path))))
        h, w, _ = image.shape

        with self._lock:
            with rsid_py.FaceAuthenticator(self._port) as f:
                try:
                    enroll_result = await run_in_threadpool(f.enroll_image, user_id, image.flatten().tolist(), w, h)
                except Exception as e:
                    logger.error(e)
                    exception = e
                finally:
                    f.disconnect()

        if exception is not None:
            raise exception
        return EnrollResponse(user_id=user_id, status=models.EnrollStatusEnum.from_rsid_py(enroll_result))

    async def enroll_host(self, user_id: str) -> EnrollResponse:
        enroll_status: rsid_py.EnrollStatus | None = None
        extracted_prints: rsid_py.ExtractedFaceprintsElement | None = None

        def on_fp_enroll_result(status: rsid_py.EnrollStatus, faceprints: rsid_py.ExtractedFaceprintsElement):
            # This method runs in the Authenticator/SDK context. Finish quickly!
            nonlocal enroll_status
            nonlocal extracted_prints
            logger.info(f"on_fp_enroll_result - status: {status}", status, type(faceprints))
            enroll_status = status
            if status == rsid_py.EnrollStatus.Success and faceprints is not None:
                # TODO: Add copy constructors to python bindings.
                extracted_prints = rsid_py.ExtractedFaceprintsElement()
                extracted_prints.flags = faceprints.flags
                extracted_prints.version = faceprints.version
                extracted_prints.features_type = faceprints.features_type
                extracted_prints.features = faceprints.features
            self._condition.notify()

        def on_progress(p: rsid_py.FacePose):
            logger.info(f"on_progress {p}")

        def on_hint(s: rsid_py.EnrollStatus, score: float | None):
            logger.info(f"on_hint {s}")

        def on_faces(faces: list[rsid_py.FaceRect], i: int):
            logger.info(f"on_faces {faces}")

        with self._lock:
            async with self._condition:
                with rsid_py.FaceAuthenticator(self._port) as authenticator:
                    try:
                        await run_in_threadpool(authenticator.extract_faceprints_for_enroll,
                                                on_progress=on_progress,
                                                on_hint=on_hint,
                                                on_faces=on_faces,
                                                on_result=on_fp_enroll_result,
                                                )
                    finally:
                        authenticator.disconnect()
                await self._condition.wait_for(lambda: enroll_status is not None)

        if enroll_status == rsid_py.EnrollStatus.Success:
            try:
                db_item = rsid_py.Faceprints()
                db_item.version = extracted_prints.version
                db_item.features_type = extracted_prints.features_type
                db_item.flags = extracted_prints.flags
                db_item.adaptive_descriptor_nomask = extracted_prints.features
                db_item.adaptive_descriptor_withmask = [0] * 515  # deprecated.
                db_item.enroll_descriptor = extracted_prints.features
                await self.db.add_faceprints(user_id, db_item)
            except Exception as e:
                logger.error(e)
                raise e

        return EnrollResponse(user_id=user_id, status=models.EnrollStatusEnum.from_rsid_py(enroll_status))

    async def enroll_host_image(self, user_id: str, file_path: Path) -> EnrollResponse:
        image = await run_in_threadpool(self._resize_if_big, (cv2.imread(str(file_path))))
        h, w, _ = image.shape
        extracted_prints: rsid_py.ExtractedFaceprintsElement
        with self._lock:
            async with self._condition:
                with rsid_py.FaceAuthenticator(self._port) as f:
                    try:
                        extracted_prints = await run_in_threadpool(
                            f.extract_image_faceprints_for_enroll,
                            image.flatten().tolist(),
                            w,
                            h,
                        )
                    finally:
                        f.disconnect()
        try:
            db_item = rsid_py.Faceprints()
            db_item.version = extracted_prints.version
            db_item.features_type = extracted_prints.features_type
            db_item.flags = extracted_prints.flags
            db_item.adaptive_descriptor_nomask = extracted_prints.features
            # db_item.adaptive_descriptor_withmask = [0]    # FIXME: deprecated?
            db_item.enroll_descriptor = extracted_prints.features
            await self.db.add_faceprints(user_id, db_item)
        except Exception as e:
            logger.error(e)
            raise e

        return EnrollResponse(user_id=user_id, status=models.EnrollStatusEnum.Success)

    async def query_users(self) -> list[str]:
        users = []
        exception: Exception | None = None
        with self._lock:
            with rsid_py.FaceAuthenticator(self._port) as f:
                try:
                    users = await run_in_threadpool(f.query_user_ids)
                except Exception as e:
                    logger.error(e)
                    exception = e
                finally:
                    f.disconnect()
        if exception is not None:
            raise exception
        return users

    async def query_host_users(self) -> list[str]:
        users = await self.db.get_user_ids()
        return users

    async def remove_user(self, user_id: str) -> None:
        exception: Exception | None = None
        with self._lock:
            with rsid_py.FaceAuthenticator(self._port) as f:
                try:
                    users = f.query_user_ids()
                    if user_id in users:
                        await run_in_threadpool(f.remove_user, user_id=user_id)
                    else:
                        raise KeyError(f"User {user_id} is not in current users")
                except Exception as e:
                    logger.error(e)
                    exception = e
                finally:
                    f.disconnect()
        if exception is not None:
            raise exception

    async def remove_host_user(self, user_id: str) -> None:
        await self.db.delete_user(user_id=user_id)

    def remove_all_users(self) -> None:
        exception: Exception | None = None
        with self._lock:
            with rsid_py.FaceAuthenticator(self._port) as authenticator:
                try:
                    authenticator.remove_all_users()
                except Exception as e:
                    logger.error(e)
                    exception = e
                finally:
                    authenticator.disconnect()
        if exception is not None:
            raise exception

    def query_device_info(self) -> DeviceInfoResponse:
        exception: Exception | None = None
        with self._lock:
            with rsid_py.DeviceController(self._port) as device_controller:
                try:
                    serial_number: str = device_controller.query_serial_number()
                    firmware_version: str = device_controller.query_firmware_version()
                    device_info: DeviceInfoResponse = DeviceInfoResponse(
                        status=models.StatusEnum.Ok,
                        serial_number=serial_number,
                        firmware_version=firmware_version,
                    )
                except Exception as e:
                    logger.error(e)
                    exception = e
                finally:
                    device_controller.disconnect()
        if exception is not None:
            raise exception
        return device_info

    def query_device_config(self) -> models.DeviceConfig:
        exception: Exception | None = None
        with self._lock:
            with rsid_py.FaceAuthenticator(self._port) as f:
                try:
                    config = f.query_device_config()
                    config = models.DeviceConfig.from_rsid_config(config)
                except Exception as e:
                    logger.error(e)
                    exception = e
                finally:
                    f.disconnect()
        if exception is not None:
            raise exception
        return config

    def update_device_config(self, config: models.DeviceConfig) -> models.DeviceConfig:
        exception: Exception | None = None
        with self._lock:
            with rsid_py.FaceAuthenticator(self._port) as f:
                try:
                    rsid_config = rsid_py.DeviceConfig()
                    rsid_config.algo_flow = config.algo_flow.to_rsid_py()
                    rsid_config.camera_rotation = config.camera_rotation.to_rsid_py()
                    rsid_config.security_level = config.security_level.to_rsid_py()
                    #rsid_config.face_selection_policy = config.face_selection_policy.to_rsid_py()
                    rsid_config.matcher_confidence_level = config.matcher_confidence_level.to_rsid_py()
                    f.set_device_config(rsid_config)
                except Exception as e:
                    logger.error(e)
                    exception = e
                finally:
                    f.disconnect()
        if exception is not None:
            raise exception
        return self.query_device_config()

    async def stream(self, ticket: uuid.UUID) -> AsyncContentStream:
        self._preview_tickets.append(ticket)
        logger.info(
            f"Starting stream for user with ticket {ticket.hex}. " f"Audience count: {len(self._preview_tickets)}"
        )
        device_preview_image: rsid_py.Image | None = None

        async def encode_image_async():
            nonlocal device_preview_image
            jpeg_quality: int = get_app_settings().preview_jpeg_quality
            webp_quality: int = get_app_settings().preview_webp_quality
            with (self._preview_encoder_lock):
                if device_preview_image is None:  # Some other thread took care of this
                    return
                try:
                    buffer = memoryview(device_preview_image.get_buffer())
                    arr = np.asarray(buffer, dtype=np.uint8)
                    array2d = arr.reshape(device_preview_image.height, device_preview_image.width, -1)
                    if get_app_settings().preview_stream_type == StreamEncodingStypes.webp:
                        array2d = array2d[:, :, ::-1]  # RGB to BGR
                        _, self._preview_image = cv2.imencode(
                            ".webp", array2d, [cv2.IMWRITE_WEBP_QUALITY, webp_quality]
                        )
                    else:
                        # array2d = np.flip(array2d, 1)
                        self._preview_image = encode_jpeg(
                            array2d,
                            # colorspace="RGB",
                            fastdct=True,
                            quality=jpeg_quality,
                        )
                        # array2d = array2d[:, :, ::-1]     # RGB to BGR
                        # (flag, self._preview_image) = cv2.imencode(".jpg", array2d,
                        #   [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])
                except Exception as encoding_ex:
                    logger.error(encoding_ex)
                finally:
                    device_preview_image = None

        def on_preview_image(image: rsid_py.Image):
            # SDK context, don't do much work here.
            nonlocal device_preview_image
            try:
                with self._preview_condition:
                    device_preview_image = image
                    self._preview_condition.notify_all()
            except Exception as preview_ex:
                logger.error(preview_ex)

        with self._lock:
            if self._preview is None:
                preview_cfg = rsid_py.PreviewConfig()
                preview_cfg.camera_number = get_app_settings().preview_camera_number
                preview_cfg.preview_mode = rsid_py.PreviewMode.MJPEG_1080P
                preview_cfg.device_type = rsid_py.discover_device_type(get_app_settings().com_port)
                # preview_cfg.portrait_mode = True
                # preview_cfg.rotate_raw = False
                self._preview = rsid_py.Preview(preview_cfg)
                self._preview.start(on_preview_image, None)

        with self._preview_condition:
            try:
                while True:
                    self._preview_condition.wait()
                    if ticket not in self._preview_tickets:  # Client disconnected?
                        continue
                    # Similar to flask image streaming:
                    # https://stackoverflow.com/a/57763063
                    await encode_image_async()
                    if self._preview_image is None:  # No encoded image available?
                        continue
                    length = str(len(self._preview_image)).encode()
                    content_type = (b"image/webp"
                                    if get_app_settings().preview_stream_type == StreamEncodingStypes.webp
                                    else b"image/jpeg")
                    yield (
                        b"--frame\r\n"
                        b"Content-Type: "
                        + content_type
                        + b"\r\n"
                        + b"Content-Length: "
                        + length
                        + b"\r\n"
                        + b"\r\n"
                        + bytearray(self._preview_image)
                        + b"\r\n"
                    )

                    # This following sleep is important. It will allow us to catch the cancellation exception
                    # https://github.com/encode/starlette/discussions/1776#discussioncomment-3207518
                    await asyncio.sleep(0.0015)  # Fix to max 60fps - F400 series max is ~15fps to ~16fps @1080p
                    # Note: asyncio.sleep is a must even if set to 0
            except asyncio.CancelledError:  # Client disconnected
                self.revoke_preview_ticket(ticket)
                # raise GeneratorExit from e

    def revoke_preview_ticket(self, ticket: uuid.UUID) -> None:
        self._preview_tickets.remove(ticket)
        logger.info(f"User with ticket {ticket.hex} disconnected. " f"Audience count: {len(self._preview_tickets)}")
        if len(self._preview_tickets) == 0:
            logger.info("No more audience. Stopping preview")
            self._preview.stop()
            self._preview = None

    def query_update_status(self) -> models.UpdateCheckerResponse:
        available, local, remote = rsid_py.UpdateChecker.is_update_available(self._port)
        response = models.UpdateCheckerResponse(update_available=available,
                                                local_release_info=models.LocalReleaseInfo.from_rsid_py(local),
                                                remote_release_info=models.RemoteReleaseInfo.from_rsid_py(remote))
        return response

    async def query_fw_update_status(self, file_path: Path) -> models.FWUpdateStatusReportResponse:
        # def progress_callback(progress: float):
        #     logger.info(f"progress: {progress}")
        #     updater.update(progress_callback=progress_callback)
        with self._lock:
            with rsid_py.FWUpdater(str(file_path), self._port) as updater:
                fw_file_info = await run_in_threadpool(updater.get_firmware_bin_info)
                device_fw_info = await run_in_threadpool(updater.get_device_firmware_info)
                sku_compat, sku_msg = updater.is_sku_compatible()
                host_compat, host_mes = updater.is_host_compatible()
                db_compat, db_msg = updater.is_db_compatible()
                policy_compat, policy_msg = updater.is_policy_compatible()

            return models.FWUpdateStatusReportResponse(
                firmware_bin_info=models.FirmwareBinInfo.from_rsid_py(fw_file_info),
                device_firmware_info=models.DeviceFirmwareInfo.from_rsid_py(device_fw_info),
                sku_compat=sku_compat,
                sku_compat_display_message=sku_msg,
                host_compat=host_compat,
                host_compat_display_message=host_mes,
                db_compat=db_compat,
                db_compat_display_message=db_msg,
                update_policy_compat=policy_compat,
                update_policy_compat_display_message=policy_msg
            )


def lib_log(level: rsid_py.LogLevel, message: str):
    log_map = {
        rsid_py.LogLevel.Debug: logger.debug,
        rsid_py.LogLevel.Info: logger.info,
        rsid_py.LogLevel.Warning: logger.warning,
        rsid_py.LogLevel.Error: logger.error,
        rsid_py.LogLevel.Critical: logger.critical,
        rsid_py.LogLevel.Trace: logger.trace,
    }
    log_map[level](message.strip())


rsid_py.set_log_callback(callback=lib_log,  # noqa: E741
                         log_level=rsid_py.LogLevel.Trace,
                         do_formatting=False)


def get_rsid_api() -> RSIDApiWrapper:
    settings = get_app_settings()
    if settings.auto_detect:
        iterator = sorted(comports(include_links=True))
        cam_port = ""
        for _, (port, desc, hwid) in enumerate(iterator, 1):
            if "2AAD" in hwid and "6373" in hwid:
                logger.info(f"Found cam on {port} -- desc: {desc} -- hwid: {hwid}")
                cam_port = port
        rsid_api = RSIDApiWrapper()
        rsid_api.set_port(cam_port)
        return rsid_api
    else:
        if settings.com_port is None:
            raise RuntimeError("Misconfigured: No com_port specified while auto-detect is disabled.")
        cam_port = settings.com_port
        rsid_api = RSIDApiWrapper()
        rsid_api.set_port(cam_port)
        return rsid_api
