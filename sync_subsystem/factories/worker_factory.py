"""
Worker factory for creating snapshot and CDC workers with proper
dependency injection and adapter wiring.
"""

from __future__ import annotations

from typing import Any
from ..workers.snapshot_worker import SnapshotWorker
from ..workers.cdc_worker import CDCWorker
from ..infrastructure.postgres.repository import PostgresMetadataRepository
from ..kafka.consumer import KafkaConsumerLayer
from ..kafka.producer import KafkaProducerLayer
from ..configs.settings import SyncSettings
from .adapter_factory import AdapterFactory
from ..domain.models import AdapterType


class WorkerFactory:
    """Factory for creating workers with wired dependencies."""

    def __init__(
        self,
        settings: SyncSettings,
        repository: PostgresMetadataRepository,
    ):
        self.settings = settings
        self.repository = repository
        self.adapter_factory = AdapterFactory(settings)

    def create_snapshot_worker(
        self,
        source_type: AdapterType,
        target_type: AdapterType,
        kafka_producer: KafkaProducerLayer | None = None,
    ) -> SnapshotWorker:
        \"\"\"Create a snapshot worker with source and target adapters.\"\"\"
        source_adapter = self.adapter_factory.create_source_adapter(source_type)
        target_adapter = self.adapter_factory.create_target_adapter(target_type)
        storage_adapter = self.adapter_factory.create_storage_adapter(source_type)

        return SnapshotWorker(
            source_adapter=source_adapter,
            target_adapter=target_adapter,
            storage_adapter=storage_adapter,
            repository=self.repository,
            kafka_producer=kafka_producer,
        )

    def create_cdc_worker(
        self,
        source_type: AdapterType,
        target_type: AdapterType,
        kafka_consumer: KafkaConsumerLayer,
        kafka_producer: KafkaProducerLayer,
    ) -> CDCWorker:
        \"\"\"Create a CDC worker with source and target adapters.\"\"\"
        cdc_adapter = self.adapter_factory.create_cdc_adapter(source_type)
        target_adapter = self.adapter_factory.create_target_adapter(target_type)

        return CDCWorker(
            cdc_adapter=cdc_adapter,
            target_adapter=target_adapter,
            repository=self.repository,
            kafka_consumer=kafka_consumer,
            kafka_producer=kafka_producer,
        )

    def create_all_workers(
        self,
        source_type: AdapterType,
        target_type: AdapterType,
        kafka_consumer: KafkaConsumerLayer,
        kafka_producer: KafkaProducerLayer,
    ) -> dict[str, SnapshotWorker | CDCWorker]:
        \"\"\"Create both snapshot and CDC workers for a sync job.\"\"\"
        return {
            "snapshot": self.create_snapshot_worker(
                source_type=source_type,
                target_type=target_type,
                kafka_producer=kafka_producer,
            ),
            "cdc": self.create_cdc_worker(
                source_type=source_type,
                target_type=target_type,
                kafka_consumer=kafka_consumer,
                kafka_producer=kafka_producer,
            ),
        }
