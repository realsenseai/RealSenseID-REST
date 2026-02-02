# -*- coding: utf-8 -*-
# Copyright (C) 2018-2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

import asyncio
from typing import Optional

import httpx
from fastapi import FastAPI
from nicegui import app, ui

from rsid_rest.frontend.authantication_manager import AuthenticationManager
from rsid_rest.frontend.info_manager import InfoManager
from rsid_rest.frontend.settings_dialog import SettingsDialog
from rsid_rest.frontend.users_manager import UserManager

ui.colors(primary="#6e93d6")
devices: dict[int, ui.element] = {}

api = httpx.AsyncClient()
running_query: Optional[asyncio.Task] = None

preview_image: ui.interactive_image | None = None
preview_image_overlay: str | None = None
user_label: ui.label | None = None
log: ui.log | None = None


# BG: https://www.intelrealsense.com/wp-content/uploads/2024/05/1020-x-572-300-Email-Banner-Hero.png
# https://tailwindcss.com/docs/justify-content  #CSS/classes docs

base_url = "http://127.0.0.1:8000"
user_manager = UserManager(base_url=base_url)
auth_manager = AuthenticationManager(base_url=base_url, user_manager=user_manager)
info_manager = InfoManager(base_url=base_url)


def init(fastapi_app: FastAPI) -> None:
    async def startup_tasks():
        await user_manager.reload_users()
        await info_manager.load_info()

    @ui.page("/")
    def show():
        global log
        global user_label
        global preview_image
        ui.page_title("RealSense™ ID Simple Web Demo")

        with ui.header().classes(replace="row items-center"):
            ui.button(on_click=lambda: left_drawer.toggle(), icon="menu").props("flat color=white")
            ui.label("RealSense™ ID Simple Web Demo").classes("absolute-center")

        with ui.left_drawer(bordered=True).props("width=225").classes("bg-blue-100") as left_drawer:
            ui.label("API Documentation").classes("font-medium")
            ui.separator()
            ui.link("Swagger API Docs", target=f"{base_url}/docs")
            ui.link("Redoc API Docs", target=f"{base_url}/redoc")
            ui.separator()
        left_drawer.hide()

        with SettingsDialog(app=app, base_url=base_url) as s_dialog, ui.card():
            s_dialog.show_settings()

        with ui.footer(value=False):
            ui.label("RealSense ID")

        def open_settings_dialog():
            asyncio.create_task(s_dialog.load_settings())
            s_dialog.open()

        with ui.page_sticky(position="bottom-right", x_offset=20, y_offset=20):
            ui.button(on_click=open_settings_dialog, icon="settings").props("fab")
            # ui.button(on_click=i_dialog.open, icon='info').props('fab')

        with ui.column().classes("w-full items-center"):
            # ui.markdown('### RealSenseID Simple Web Demo')
            with ui.row().style("gap:2em").classes("justify-center w-full"):
                with ui.column():
                    with ui.card().tight():
                        preview_image = ui.interactive_image(f"{base_url}/v1/preview/stream/").classes("w-96 min-w-fit").style("height:90vh")
                        with ui.card_section():
                            user_label = ui.label("RealSenseID Ready").classes("mx-auto")

                    with ui.row().style("gap:2px").classes("w-full place-items-start"):
                        ui.label("S/N:").classes("text-xs font-medium justify-end")
                        ui.label("-- loading --").bind_text(info_manager, "serial_number").classes(
                            "text-xs justify-start"
                        )

                with ui.column().classes("w-80"):
                    with ui.card().classes("w-full place-items-stretch"):
                        auth_manager.preview_image = preview_image
                        auth_manager.status_label = user_label
                        auth_manager.render_controls()

                    with ui.card().classes("w-full place-items-stretch"):
                        ui.label("User list").classes("font-medium")
                        user_manager.user_table_ui()
                        ui.separator()
                        ui.label("User Enrollment").classes("font-medium")
                        user_manager.user_enrollment_ui()

            # with ui.column().classes('w-full items-stretch justify-center'):
            #     ui.label('Logs')
            #     log = ui.log(max_lines=10).classes('w-full')
            asyncio.create_task(startup_tasks())

    ui.run_with(
        fastapi_app,
        mount_path="/gui",  # NOTE this can be omitted if you want the paths passed to @ui.page to be at the root
        storage_secret="super secret value",
        # NOTE setting a secret is optional but allows for persistent storage per user
    )
