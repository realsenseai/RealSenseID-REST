# -*- coding: utf-8 -*-
# Copyright (C) 2018-2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

import datetime
import multiprocessing
import sys
import uuid
from pathlib import Path
from typing import Any

import numpy as np
from loguru import logger
from qdrant_client import QdrantClient, models, AsyncQdrantClient

from . import rsid_py
from qdrant_client.conversions import common_types as types
from qdrant_client.http.models import Distance, PointStruct, VectorParams

from .host_db_base import HostDBBase
from ..core.config import get_app_settings


def _rfc3339_string():
    return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-4] + "Z"


RSID_NUM_OF_RECOGNITION_FEATURES = 512
DATABASE_LOCK = multiprocessing.Lock()


# Qdrant in local mode locks the DB files per client. Let's make every client close the connection
# after each call for the sample code to work properly. In production, you want a server deployment.
class AsyncClosableDBSession:
    def __init__(self, deb_file: str):
        self._db_file = str(Path(deb_file).resolve())

    async def __aenter__(self):
        DATABASE_LOCK.acquire()
        self.client = AsyncQdrantClient(path=self._db_file, force_disable_check_same_thread=True)
        return self.client

    async def __aexit__(self, exc_type, exc_value, exc_tb):
        await self.client.close()
        DATABASE_LOCK.release()


class HostDBLocalFile(HostDBBase):
    client: QdrantClient | None

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.db_file = str(get_app_settings().db_file)
        self.collections_name: str = "RealsenseID_FacePrints"
        client: QdrantClient | None = None
        try:
            client = QdrantClient(path=self.db_file)
            client.create_collection(
                collection_name=self.collections_name,
                vectors_config=VectorParams(size=RSID_NUM_OF_RECOGNITION_FEATURES, distance=Distance.COSINE),
            )
        except ValueError:
            pass
        # In server deployment, you want to enable indexing:
        # try:
        #    client.create_payload_index(
        #        collection_name=self.collections_name,
        #        field_name="user_id",
        #        field_schema="keyword",
        #    )
        # except Exception:
        #    pass
        if client is not None:
            client.close()

    # Production notes: client should use a server and should be a member variable (self.client) so that
    # it can be reused.

    async def add_faceprints(self, user_id: str, faceprints: rsid_py.Faceprints) -> None:
        async with AsyncClosableDBSession(self.db_file) as client:
            collection_info = await client.get_collection(collection_name=self.collections_name)
            logger.info(f"Before: Collection: {self.collections_name} - {collection_info.points_count} records.")

            vector = faceprints.enroll_descriptor[:RSID_NUM_OF_RECOGNITION_FEATURES]
            await client.upsert(
                collection_name=self.collections_name,
                wait=True,
                points=[
                    PointStruct(
                        id=str(uuid.uuid4()),
                        vector=vector,
                        payload={
                            "user_id": user_id,
                            "flags": faceprints.flags,
                            "version": faceprints.version,
                            "features_type": faceprints.features_type,
                            "adaptive_descriptor_nomask": faceprints.adaptive_descriptor_nomask,
                            "adaptive_descriptor_withmask": faceprints.adaptive_descriptor_withmask,
                            "enroll_descriptor": faceprints.enroll_descriptor,
                            "created_at": _rfc3339_string()
                        },
                    )
                ],
            )
            collection_info = await client.get_collection(collection_name=self.collections_name)
            logger.info(f"After: Collection: {self.collections_name} - {collection_info.points_count} records.")

    async def update_faceprints(self, user_id: str, faceprints: rsid_py.Faceprints) -> None:
        async with AsyncClosableDBSession(self.db_file) as client:
            collection_info = await client.get_collection(collection_name=self.collections_name)
            logger.info(
                f"update_faceprints: > Collection: {self.collections_name} - {collection_info.points_count} records."
            )

            records = await self._validate_single_user(client, user_id)
            point_id = records[0].id

            vector = faceprints.enroll_descriptor[:RSID_NUM_OF_RECOGNITION_FEATURES]
            await client.batch_update_points(
                collection_name=self.collections_name,
                wait=True,
                update_operations=[
                    models.UpdateVectorsOperation(
                        update_vectors=models.UpdateVectors(
                            points=[
                                models.PointVectors(
                                    id=point_id,
                                    vector=vector,
                                )
                            ]
                        )
                    ),
                    # Don't use overwrite_payload to maintain `created_at`
                    models.SetPayloadOperation(
                        set_payload=models.SetPayload(
                            payload={
                                "flags": faceprints.flags,
                                "version": faceprints.version,
                                "features_type": faceprints.features_type,
                                "adaptive_descriptor_nomask": faceprints.adaptive_descriptor_nomask,
                                "adaptive_descriptor_withmask": faceprints.adaptive_descriptor_withmask,
                                "enroll_descriptor": faceprints.enroll_descriptor,
                                "updated_at": _rfc3339_string()
                            },
                            points=[point_id],
                        )
                    ),
                ],
            )
            collection_info = await client.get_collection(collection_name=self.collections_name)
            logger.info(
                f"update_faceprints: < Collection: {self.collections_name} - {collection_info.points_count} records."
            )

    async def get_user_ids(self) -> list[str]:
        records: list[types.Record]
        async with AsyncClosableDBSession(self.db_file) as client:
            collection_info = await client.get_collection(collection_name=self.collections_name)
            logger.info(f"Collection: {self.collections_name} - {collection_info.points_count} records.")
            records, _ = await client.scroll(limit=sys.maxsize, collection_name=self.collections_name)
        users = []
        for record in records:
            users.append(record.payload["user_id"])
        return users

    async def get_all_faceprints(self) -> list:
        records: list[types.Record]
        async with AsyncClosableDBSession(self.db_file) as client:
            collection_info = await client.get_collection(collection_name=self.collections_name)
            logger.info(f"Collection: {self.collections_name} - {collection_info.points_count} records.")
            records, _ = await client.scroll(limit=sys.maxsize, collection_name=self.collections_name)
        result = []
        for record in records:
            result.append(record.payload)
        return result

    async def get_faceprints(self, extracted_faceprints: rsid_py.ExtractedFaceprintsElement) -> list:
        records: list[types.ScoredPoint]
        async with AsyncClosableDBSession(self.db_file) as client:
            collection_info = await client.get_collection(collection_name=self.collections_name)
            logger.info(f"Collection: {self.collections_name} - {collection_info.points_count} records.")
            vector = extracted_faceprints.features[:RSID_NUM_OF_RECOGNITION_FEATURES]
            vector = np.array(vector, dtype=float)
            records = await client.search(
                collection_name=self.collections_name,
                search_params=models.SearchParams(hnsw_ef=128, exact=False),
                query_vector=vector,
                limit=get_app_settings().host_mode_hybrid_max_results,
                score_threshold=get_app_settings().host_mode_hybrid_score_threshold,
            )
        result = []
        for record in records:
            result.append(record.payload)
        return result

    async def delete_user(self, user_id: str) -> None:
        async with AsyncClosableDBSession(self.db_file) as client:
            records = await self._validate_single_user(client, user_id)
            point_id = records[0].id
            await client.delete(
                collection_name=self.collections_name,
                points_selector=[point_id],
                wait=True,
            )
            collection_info = await client.get_collection(collection_name=self.collections_name)
            logger.info(f"Collection: {self.collections_name} - {collection_info.points_count} records.")

    async def _validate_single_user(self, client, user_id):
        records, _ = await client.scroll(
            collection_name=self.collections_name,
            scroll_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="user_id",
                        match=models.MatchValue(
                            value=user_id,
                        ),
                    )
                ]
            ),
            limit=2,
        )
        if len(records) > 1:
            logger.error(records)
            raise RuntimeError(f"DB integrity error. More than one record found with this user_id {user_id}!")
        if len(records) == 0:
            logger.error(records)
            raise RuntimeError(f"No records were found with this user_id {user_id}!")
        return records

    async def delete_all_users(self) -> None:
        # TODO: Implement
        # delete_collection
        raise RuntimeError("Not implemented in host mode")
