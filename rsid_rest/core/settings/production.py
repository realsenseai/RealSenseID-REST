# -*- coding: utf-8 -*-
# Copyright (C) 2018-2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

from pathlib import Path
from typing import Annotated

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from rsid_rest.core.settings.app import AppSettings
from rsid_rest.core.settings.base import ApplicationDBTypes, HostModeAuthTypes, StreamEncodingStypes


class ProdAppSettings(AppSettings, validate_assignment=True):
    model_config = SettingsConfigDict(env_file=".env")

    # Device discovery and serial port configuration
    auto_detect: bool = True
    com_port: str | None = None
    preview_camera_number: int = -1  # -1 = auto-detect

    # DB mode
    db_mode: ApplicationDBTypes = ApplicationDBTypes.host

    # DB Host mode configuration
    db_file: Path | None = "vectors.db"
    host_mode_auth_type: HostModeAuthTypes = HostModeAuthTypes.hybrid

    # Hybrid mode settings
    """" Maximum number of faceprints to be sent to device after vector db search """
    host_mode_hybrid_max_results: int | None = 10
    """" Vector DB threshold for searching. """
    host_mode_hybrid_score_threshold: float | None = 0.2

    # Preview and streaming configuration
    preview_jpeg_quality: Annotated[int, Field(ge=1, le=100)] = 85  # 1 - 100
    """ JPEG performance is better with TurboJPEG than WebP with OpenCV """
    preview_stream_type: StreamEncodingStypes = StreamEncodingStypes.jpeg
    preview_webp_quality: Annotated[int, Field(ge=1, le=100)] = 85  # 1 - 100
