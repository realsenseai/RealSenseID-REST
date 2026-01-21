# -*- coding: utf-8 -*-
# Copyright (C) 2018-2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppEnvTypes(Enum):
    prod: str = "prod"
    stage: str = "stg"
    dev: str = "dev"
    test: str = "test"


class ApplicationDBTypes(Enum):
    device: str = "device"
    host: str = "host"


class HostModeAuthTypes(Enum):
    hybrid: str = "hybrid"
    device: str = "device"


class StreamEncodingStypes(Enum):
    jpeg: str = "jpeg"
    webp: str = "webp"


class BaseAppSettings(BaseSettings, validate_assignment=True):
    app_env: AppEnvTypes = AppEnvTypes.prod
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
