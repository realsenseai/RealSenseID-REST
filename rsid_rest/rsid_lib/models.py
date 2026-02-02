# -*- coding: utf-8 -*-
# Copyright (C) 2018-2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

import copy
from typing import Any, Optional

from . import rsid_py
from pydantic import (
    BaseModel,
    Field, HttpUrl,
)

from .gen.models import (
    AlgoFlowEnum,
    AuthenticateStatusEnum,
    CameraRotationEnum,
    EnrollStatusEnum,
    MatcherConfidenceLevelEnum,
    SecurityLevelEnum,
    StatusEnum,
)


def val_examples(field: str, prefix: str, example: list[Any]) -> str:
    values: list[str] = []
    for eg in example:
        values.append(prefix + "." + str(eg) + "\n")
    return f"`{field}`: <br/>\n - " + "- ".join(values)


class UsersQueryResponse(BaseModel, validate_assignment=True):
    users: list[str]


class CommonOperationResponse(
    BaseModel,
    validate_assignment=True,
):
    status: StatusEnum = Field(
        json_schema_extra={
            "title": "status",
            "description": "Operation status",
            "examples": [
                f"{StatusEnum.Ok}",
            ],
        }
    )
    message: Optional[str]


class DeviceConfig(BaseModel, validate_assignment=True):
    algo_flow: AlgoFlowEnum = Field(
        json_schema_extra={
            "title": "algo_flow",
            "description": "AlgoFlow for device configuration.",
            "examples": [
                f"{AlgoFlowEnum.All}",
                f"{AlgoFlowEnum.FaceDetectionOnly}",
                f"{AlgoFlowEnum.SpoofOnly}",
                f"{AlgoFlowEnum.RecognitionOnly}",
            ],
        }
    )
    camera_rotation: CameraRotationEnum = Field(
        json_schema_extra={
            "title": "camera_rotation",
            "description": "CameraRotation for device",
            "examples": [
                f"{CameraRotationEnum.Rotation_0_Deg}",
                f"{CameraRotationEnum.Rotation_180_Deg}",
            ],
        }
    )
    security_level: SecurityLevelEnum = Field(
        json_schema_extra={
            "title": "security_level",
            "description": "SecurityLevel for device",
            "examples": [
                f"{SecurityLevelEnum.High}",
                f"{SecurityLevelEnum.Medium}",
                f"{SecurityLevelEnum.Low}",
            ],
        }
    )

    matcher_confidence_level: MatcherConfidenceLevelEnum = Field(
        json_schema_extra={
            "title": "matcher_confidence_level",
            "description": "Matcher Confidence Level for matcher",
            "examples": [
                f"{MatcherConfidenceLevelEnum.High}",
                f"{MatcherConfidenceLevelEnum.Medium}",
                f"{MatcherConfidenceLevelEnum.Low}",
            ],
        }
    )

    # TODO: Add max_spoofs and dump_mode
    @staticmethod
    def from_rsid_config(config: rsid_py.DeviceConfig) -> "DeviceConfig":
        return DeviceConfig(
            algo_flow=AlgoFlowEnum.from_rsid_py(config.algo_flow),
            camera_rotation=CameraRotationEnum.from_rsid_py(config.camera_rotation),
            security_level=SecurityLevelEnum.from_rsid_py(config.security_level),
            matcher_confidence_level=MatcherConfidenceLevelEnum.from_rsid_py(config.matcher_confidence_level),
        )


class DeviceConfigResponse(
    BaseModel,
    validate_assignment=True,
):
    status: StatusEnum = Field(
        json_schema_extra={
            "title": "status",
            "description": "Status for device",
            "examples": [f"{StatusEnum.Ok}", f"{StatusEnum.Error}"],
        }
    )
    config: Optional[DeviceConfig] = Field(
        json_schema_extra={
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/DeviceConfig"},
                }
            }
        }
    )


class FaceRect(BaseModel):
    x: int = Field()
    y: int = Field()
    w: int = Field()
    h: int = Field()

    @staticmethod
    def from_rsid_face_rect(face_rect: rsid_py.FaceRect) -> "FaceRect":
        return FaceRect(
            x=face_rect.x,
            y=face_rect.y,
            h=face_rect.h,
            w=face_rect.w,
        )


class AuthenticationResponse(
    BaseModel,
    validate_assignment=True,
):
    status: AuthenticateStatusEnum = Field(
        json_schema_extra={
            "title": "status",
            "description": "Authentication Status",
            "examples": [
                f"{rsid_py.AuthenticateStatus.Success}",
                f"{rsid_py.AuthenticateStatus.Error}",
            ],
        }
    )
    user_id: Optional[str] = Field(
        json_schema_extra={
            "title": "user_id",
            "description": "user_id if authenticated, null if unauthenticated",
            "examples": [
                "user_id",
            ],
        }
    )
    faces: Optional[list[FaceRect]] = Field(
        json_schema_extra={
            "title": "faces",
            "description": "list of faces if authenticated, null if unauthenticated",
        }
    )


class EnrollResponse(BaseModel, validate_assignment=True):
    status: EnrollStatusEnum = Field(
        json_schema_extra={
            "title": "status",
            "description": "Enrollment Status",
            "examples": [
                f"{EnrollStatusEnum.Success}",
                f"{EnrollStatusEnum.Error}",
            ],
        }
    )
    user_id: Optional[str]


class DeviceInfoResponse(
    BaseModel,
    validate_assignment=True,
):
    status: StatusEnum = Field(
        json_schema_extra={
            "title": "status",
            "description": "Operation status",
            "examples": [
                f"{StatusEnum.Ok}",
            ],
        }
    )
    serial_number: str
    firmware_version: str


class LocalReleaseInfo(
    BaseModel,
    validate_assignment=True,
):
    software_version_string: str
    firmware_version_string: str
    software_version: int
    firmware_version: int

    @staticmethod
    def from_rsid_py(release_info: rsid_py.ReleaseInfo) -> 'LocalReleaseInfo':
        return LocalReleaseInfo(software_version_string=release_info.sw_version_str,
                                firmware_version_string=release_info.fw_version_str,
                                software_version=release_info.sw_version,
                                firmware_version=release_info.fw_version)


class RemoteReleaseInfo(
    BaseModel,
    validate_assignment=True,
):
    software_version_string: str
    firmware_version_string: str
    software_version: int
    firmware_version: int
    release_notes_url: HttpUrl | str | None
    release_url: HttpUrl | str | None

    @staticmethod
    def from_rsid_py(release_info: rsid_py.ReleaseInfo) -> 'RemoteReleaseInfo':
        return RemoteReleaseInfo(software_version_string=release_info.sw_version_str,
                                 firmware_version_string=release_info.fw_version_str,
                                 software_version=release_info.sw_version,
                                 firmware_version=release_info.fw_version,
                                 release_notes_url=release_info.release_notes_url,
                                 release_url=release_info.release_url)


class UpdateCheckerResponse(BaseModel, validate_assignment=True):
    update_available: bool
    local_release_info: LocalReleaseInfo
    remote_release_info: RemoteReleaseInfo


class FirmwareBinInfo(BaseModel, validate_assignment=True):
    firmware_version: str
    module_names: list[str]
    recognition_version: str

    @staticmethod
    def from_rsid_py(bin_info: rsid_py.FirmwareBinInfo) -> 'FirmwareBinInfo':
        return FirmwareBinInfo(firmware_version=bin_info.fw_version,
                               recognition_version=bin_info.recognition_version,
                               module_names=copy.copy(bin_info.module_names))


class DeviceFirmwareInfo(BaseModel, validate_assignment=True):
    firmware_version: str
    recognition_version: str
    serial_number: str

    @staticmethod
    def from_rsid_py(bin_info: rsid_py.DeviceFirmwareInfo) -> 'DeviceFirmwareInfo':
        return DeviceFirmwareInfo(firmware_version=bin_info.fw_version,
                                  recognition_version=bin_info.recognition_version,
                                  serial_number=bin_info.serial_number)


class FWUpdateStatusReportResponse(BaseModel, validate_assignment=True):
    firmware_bin_info: FirmwareBinInfo
    device_firmware_info: DeviceFirmwareInfo
    sku_compat: bool
    sku_compat_display_message: str
    host_compat: bool
    host_compat_display_message: str
    db_compat: bool
    db_compat_display_message: str
    update_policy_compat: bool
    update_policy_compat_display_message: str
