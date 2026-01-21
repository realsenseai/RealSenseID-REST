# -*- coding: utf-8 -*-
# Copyright (C) 2018-2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

import base64
import io
from dataclasses import dataclass, field
from typing import Callable, List

import httpx
from loguru import logger
from nicegui import events, ui
from nicegui.events import GenericEventArguments, KeyEventArguments


@dataclass
class UserList:
    title: str
    on_change: Callable
    users: List[str] = field(default_factory=list)
    enabled: bool = True

    def add(self, user_id: str) -> None:
        self.users.append(user_id)
        self.on_change()

    def remove(self, user_id: str) -> None:
        self.users.remove(user_id)
        self.on_change()

    def data(self) -> list[dict]:
        d: list[dict] = []
        for user_id in self.users:
            item = {"key": user_id}
            d.append(item)
        return d


class UserManager:
    _columns = [
        {
            "name": "key",
            "label": "User ID",
            "field": "key",
            "required": True,
            "align": "left",
            "sortable": False,
        },
        {"name": "action", "label": "Action", "field": "value", "sortable": False},
    ]

    def __init__(self, base_url: str) -> None:
        self.loading_notification = None
        self.users_list = UserList("Users", on_change=self.user_table_ui.refresh)
        self.base_url = base_url

    async def delete_user(self, user_id: str) -> None:
        logger.info(f"Delete user_id: {user_id}")
        ui.notify(f"Deleting User: {user_id}")
        http_client: httpx.AsyncClient = httpx.AsyncClient()
        response: httpx.Response = await http_client.delete(f"{self.base_url}/v1/users/{user_id}")
        await http_client.aclose()
        if response.status_code == 200:
            ui.notify(f"User: {user_id} deleted", color="positive")
            await self.reload_users()
        else:
            ui.notify(f"Error while deleting user {user_id}", color="negative")

    async def reload_users(self) -> None:
        http_client: httpx.AsyncClient = httpx.AsyncClient()
        response: httpx.Response = await http_client.get(f"{self.base_url}/v1/users/")
        await http_client.aclose()
        if response.status_code == 200:
            self.users_list.users = []
            for user in response.json()["users"]:
                self.users_list.add(user)
            self.user_table_ui.refresh()

    async def on_delete_user_event(self, event: GenericEventArguments):
        user_id: str = event.args["row"]["key"]

        with ui.dialog() as dialog, ui.card():
            def handle_key(args: KeyEventArguments):
                if dialog.value and args.key.enter and not args.action.repeat:
                    dialog.submit("Yes")

            ui.keyboard(on_key=handle_key, ignore=[])

            with ui.row().classes("justify-center"):
                ui.label("Delete User").classes("font-medium")
            ui.separator()
            ui.label(f"Are you sure you want to delete user: {user_id}?")
            ui.separator()
            with ui.row().classes("justify-center w-full"):
                ui.button("Cancel", icon="cancel", on_click=lambda: dialog.close())
                ui.button("Delete", icon="delete", on_click=lambda: dialog.submit("Yes")).props("color=negative")
        result = await dialog
        if result == "Yes":
            await self.delete_user(user_id)

    @ui.refreshable
    def user_table_ui(self):
        if len(self.users_list.users) < 1:
            ui.label("No users!.").classes("mx-auto")
            return
        with ui.table(columns=self._columns, rows=self.users_list.data(), pagination=5).classes(
            "w-full bordered") as table:
            table.add_slot(
                "body-cell-action",
                """
                <q-td :props="props">
                    <q-btn @click="$parent.$emit('del', props)" icon="delete" flat dense color='red'/>
                </q-td>
            """,
            )
            # <q-btn @click="$parent.$emit('add', props)" icon="add" flat dense color='green'/>
            # <q-btn @click="$parent.$emit('edit', props)" icon="edit" flat dense color='blue'/>
            table.on("del", lambda event: self.on_delete_user_event(event=event))

    async def enroll_user(self, user_id: str):
        logger.info(f"Enrolling user_id: {user_id}")
        self.loading_notification = ui.notification(f"🕵️ Enrolling user: {user_id}", spinner=True, timeout=30)

        http_client: httpx.AsyncClient = httpx.AsyncClient()
        response: httpx.Response = await http_client.post(
            f"{self.base_url}/v1/users/enroll/", params={"user_id": user_id}, timeout=30
        )
        self.loading_notification.dismiss()
        await http_client.aclose()
        if response.status_code == 201:
            ui.notify(f"Enrolled user: {user_id}", color="positive")
            await self.reload_users()
        elif response.status_code == 406:
            status = response.json()["status"]
            ui.notify(f"{status} error while enrolling user {user_id}", color="negative")
        else:
            ui.notify(f"Error while enrolling user {user_id}", color="negative")

    async def enroll_user_clicked(self):
        with ui.dialog() as dialog, ui.card():
            def handle_key(args: KeyEventArguments):
                if dialog.value and args.key.enter and not args.action.repeat:
                    dialog.submit("Yes")

            ui.keyboard(on_key=handle_key, ignore=[])

            with ui.row().classes("justify-center"):
                ui.label("Enroll New User").classes("font-medium")
            ui.separator()
            new_user_id = ui.input(
                placeholder="User ID",
                # validation={'Too short': lambda value: len(value) >= 1}
            ).props("autofocus size=80 clearable")
            ui.space()
            with ui.row().classes("justify-center w-full"):
                ui.button("Cancel", icon="cancel", on_click=lambda: dialog.close())
                ui.button("Ok", icon="check", on_click=lambda: dialog.submit("Yes"))
        result = await dialog
        if result == "Yes":
            if new_user_id.value == "":
                ui.notify("Can't enroll user with empty user id")
            else:
                await self.enroll_user(new_user_id.value)

    async def enroll_image(self, user_id: str, e: events.UploadEventArguments):
        logger.info(f"Enrolling user_id: {user_id}")
        self.loading_notification = ui.notification(f"🖼️ Enrolling Image for: {user_id}", spinner=True, timeout=30)

        content = await e.file.read()
        files = {"EnrollImageFileUpload": (e.file.name, io.BytesIO(content))}
        http_client: httpx.AsyncClient = httpx.AsyncClient()
        response: httpx.Response = await http_client.post(
            f"{self.base_url}/v1/users/enroll-image/",
            params={"user_id": user_id},
            files=files,
            timeout=30,
        )
        self.loading_notification.dismiss()

        await http_client.aclose()
        if response.status_code == 201:
            ui.notify(f"Enrolled with image for user: {user_id}", color="positive")
            await self.reload_users()
        elif response.status_code == 406:
            status = response.json()["status"]
            ui.notify(
                f"{status} error while enrolling image for user {user_id}",
                color="negative",
            )
        else:
            ui.notify(f"Error while enrolling image for user {user_id}", color="negative")

    async def handle_upload(self, e: events.UploadEventArguments):
        with ui.dialog() as dialog, ui.card():
            def handle_key(args: KeyEventArguments):
                if dialog.value and args.key.enter and not args.action.repeat:
                    dialog.submit("Yes")

            ui.keyboard(on_key=handle_key, ignore=[])

            with ui.row().classes("justify-center"):
                ui.label("Enroll Image").classes("font-medium")
            ui.separator()
            with ui.row().classes("items-center max-w-full"):
                b64_bytes = base64.b64encode(await e.file.read())
                ui.image(f"data:{e.file.content_type};base64,{b64_bytes.decode()}").classes("w-40")
            new_user_id = ui.input(
                placeholder="User ID",
                # validation={'Too short': lambda value: len(value) >= 1}
            ).props("autofocus size=80 clearable")
            ui.space()
            with ui.row().classes("justify-center w-full"):
                ui.button("Cancel", icon="cancel", on_click=lambda: dialog.close())
                ui.button("Ok", icon="check", on_click=lambda: dialog.submit("Yes"))
        result = await dialog
        if result == "Yes":
            if new_user_id.value == "":
                ui.notify("Can't enroll user with empty user id")
            else:
                await self.enroll_image(new_user_id.value, e)

    def user_enrollment_ui(self):
        ui.button("Enroll", on_click=self.enroll_user_clicked).classes("max-w-full")
        ui.upload(on_upload=self.handle_upload, label="Enroll Image").classes("max-w-full").props(
            'accept=".png, image/*"'
        )
