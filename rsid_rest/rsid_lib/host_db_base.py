# -*- coding: utf-8 -*-
# Copyright (C) 2018-2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

from abc import abstractmethod
from typing import Any

from . import rsid_py


class HostDBBase:
    def __init__(self, **kwargs: Any):
        pass

    @abstractmethod
    async def add_faceprints(self, user_id: str, faceprints: rsid_py.Faceprints) -> None:
        ...

    @abstractmethod
    async def update_faceprints(self, user_id: str, faceprints: rsid_py.Faceprints) -> None:
        ...

    @abstractmethod
    async def get_user_ids(self) -> list[str]:
        ...

    @abstractmethod
    async def get_all_faceprints(self) -> list:
        ...

    @abstractmethod
    async def get_faceprints(self, extracted_faceprints: rsid_py.ExtractedFaceprintsElement) -> list:
        ...

    @abstractmethod
    async def delete_user(self, user_id: str) -> None:
        ...

    @abstractmethod
    async def delete_all_users(self) -> None:
        ...
