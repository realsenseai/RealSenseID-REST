# -*- coding: utf-8 -*-
# Copyright (C) 2018-2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

import asyncio
from dataclasses import dataclass, field
from typing import Callable

import httpx
from loguru import logger
from nicegui import ui


@dataclass
class DeviceConfig:
    on_change: Callable
    camera_rotation: str | None = field(default_factory=str)
    algo_flow: str | None = field(default_factory=str)
    security_level: str | None = field(default_factory=str)
    # face_selection_policy: str | None = field(default_factory=str)
    matcher_confidence_level: str | None = field(default_factory=str)


class SettingsDialog(ui.dialog):
    def __init__(self, *, value: bool = False, base_url: str, app):
        super().__init__(value=value)
        self.spinner = None
        self.loading_notification: ui.notification | None = None
        self.base_url = base_url
        self.app = app
        self.http_client: httpx.AsyncClient = httpx.AsyncClient()
        self.dc: DeviceConfig | None = DeviceConfig(on_change=self.show_settings.refresh)
        self.enable_controls: bool = False

    async def load_settings(self):
        self.enable_controls = False
        self.update()
        response: httpx.Response = await self.http_client.get(f"{self.base_url}/v1/device/device-config/")
        if response.status_code == 200:
            self.dc.algo_flow = response.json()["config"]["algo_flow"]
            self.dc.security_level = response.json()["config"]["security_level"]
            # self.dc.face_selection_policy = response.json()["config"]["face_selection_policy"]
            self.dc.camera_rotation = response.json()["config"]["camera_rotation"]
            self.dc.matcher_confidence_level = response.json()["config"]["matcher_confidence_level"]
            self.dc.on_change()
            self.enable_controls = True
            self.update()
        else:
            ui.notify("Error while retrieving settings.", color="negative")
            logger.error(f"Error while retrieving settings: {response.text}")
        self.loading_notification.dismiss()
        # self.show_settings.refresh()

    async def save_settings(self):
        self.loading_notification = ui.notification("💽 Saving settings to device", spinner=True)
        self.enable_controls = False
        self.update()
        json = {
            "algo_flow": self.dc.algo_flow,
            "camera_rotation": self.dc.camera_rotation,
            #"face_selection_policy": self.dc.face_selection_policy,
            "security_level": self.dc.security_level,
            "matcher_confidence_level": self.dc.matcher_confidence_level,
        }
        response: httpx.Response | None = None
        try:
            response = await self.http_client.put(
                f"{self.base_url}/v1/device/device-config/", json=json, timeout=30
            )
        except httpx.ReadError as e:
            logger.error(e)
        self.loading_notification.dismiss()
        self.enable_controls = True
        self.update()
        if response is not None and response.status_code == 200:
            ui.notify("💽 Settings applied", color="positive")
        else:
            ui.notify("Error while applying settings.", color="negative")
            logger.error(f"Error while updating settings: {response.text}" if response is not None else
                         "HTTP exception while updating settings")

    @ui.refreshable
    def show_settings(self) -> None:
        with ui.row().classes("text-2xl"):
            ui.icon("settings", color="primary").style("padding: 4px 0px").classes("h-full")
            ui.label("Settings").classes("font-medium")
            # ui.spinner('dots', size='2em').bind_visibility(self, 'enable_controls')

        ui.separator()

        # if self.dc.face_selection_policy is None:
        #     self.loading_notification = ui.notification("Loading settings...", spinner=True)
        #     ui.label("Retrieving settings!").classes("mx-auto")
        #     ui.label("Please wait...").classes("mx-auto")
        #     ui.separator()
        #     with ui.row().classes("justify-center w-80"):
        #         ui.button("Close", icon="close", on_click=lambda: self.close())
        #     asyncio.create_task(self.load_settings())
        #     return

        # with ui.row().style("gap:2em").classes("place-content-center w-full"):
        #     ui.label("Face Selection").classes("font-medium").style("padding: 8px 0px")
        #     options = {
        #         "FaceSelectionPolicy.Single": "Single",
        #         "FaceSelectionPolicy.All": "Multi",
        #     }
        #     ui.toggle(options).bind_value(self.dc, "face_selection_policy").bind_enabled(self, "enable_controls")

        with ui.row().style("gap:2em").classes("place-content-center w-full"):
            ui.label("Security Level").classes("font-medium").style("padding: 8px 0px")
            options = {
                "SecurityLevel.High": "High",
                "SecurityLevel.Medium": "Enhanced",
                "SecurityLevel.Low": "Standard",
            }
            ui.toggle(options).bind_value(self.dc, "security_level").bind_enabled(self, "enable_controls")

        with ui.row().style("gap:2em").classes("place-content-center w-full"):
            ui.label("Matcher Confidence Level").classes("font-medium").style("padding: 8px 0px")
            options = {
                "MatcherConfidenceLevel.High": "High",
                "MatcherConfidenceLevel.Medium": "Enhanced",
                "MatcherConfidenceLevel.Low": "Standard",
            }
            ui.toggle(options).bind_value(self.dc, "matcher_confidence_level").bind_enabled(self, "enable_controls")

        with ui.row().style("gap:2em").classes("place-content-center w-full"):
            ui.label("Operation Mode").classes("font-medium").style("padding: 8px 0px")
            options = {
                "AlgoFlow.All": "All",
                "AlgoFlow.FaceDetectionOnly": "Detect",
                "AlgoFlow.SpoofOnly": "Spoof",
                "AlgoFlow.RecognitionOnly": "Recognition",
            }
            ui.toggle(options).bind_value(self.dc, "algo_flow").bind_enabled(self, "enable_controls")

        with ui.row().style("gap:2em").classes("place-content-center w-full"):
            ui.label("Camera Rotation").classes("font-medium").style("padding: 8px 0px")
            options = {
                "CameraRotation.Rotation_0_Deg": "0°",
                "CameraRotation.Rotation_180_Deg": "180°",
            }
            ui.toggle(options).bind_value(self.dc, "camera_rotation").bind_enabled(self, "enable_controls")

        ui.separator()

        with ui.row().classes("justify-center w-full"):
            ui.button("Close", icon="close", on_click=lambda: self.close())
            ui.button("Apply", icon="check", on_click=lambda: self.save_settings()).bind_enabled(
                self, "enable_controls"
            )

        ui.separator()

        ui.dark_mode().bind_value(self.app.storage.user, "dark_mode")
        # NOTE dark mode will be persistent for each user across tabs and server restarts
        ui.switch("dark mode").bind_value(self.app.storage.user, "dark_mode")
