# -*- coding: utf-8 -*-
# Copyright (C) 2018-2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

from dataclasses import dataclass
from typing import Callable

import httpx


@dataclass
class InfoManager:
    firmware_version: str | None
    serial_number: str | None
    on_change: Callable

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self.firmware_version = None
        self.serial_number = None
        self.http_client: httpx.AsyncClient = httpx.AsyncClient()

    async def load_info(self) -> None:
        response: httpx.Response = await self.http_client.get(f"{self.base_url}/v1/device/device-info/")
        if response.status_code == 200:
            self.serial_number = response.json()["serial_number"]
            self.firmware_version = response.json()["firmware_version"]
            self.on_change()
