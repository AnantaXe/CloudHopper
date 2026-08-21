"""
Integration examples and patterns for snapshot/CDC workers with Temporal.

This module demonstrates:
1. How to instantiate workers with adapters
2. How to use workers in Temporal activities
3. How to wire workers with Kafka producers/consumers
4. How to configure workers for different cloud platforms
"""

from __future__ import annotations

from typing import Any
import logging

from ..configs.settings import SyncSettings
from ..domain.models import SyncJobMetadata, AdapterType
from ..infrastructure.postgres.repository import PostgresMetadataRepository
from ..kafka.consumer import KafkaConsumerLayer
from ..kafka.producer import KafkaProducerLayer
from ..kafka.topics import KafkaTopic, SYNC_CDC_EVENTS
from ..workers.snapshot_worker import SnapshotWorker
from ..workers.cdc_worker import CDCWorker
from ..factories.worker_factory import WorkerFactory

logger = logging.getLogger(__name__)


class WorkerIntegration:
    """
    Integration layer for workers with Temporal activities.
    
    Usage in Temporal:
    
    @activity.defn
    async def execute_snapshot_activity(job_id: str, object_path: str, chunk_index: int) -> dict:
        integration = WorkerIntegration(settings, repository)
        return await integration.execute_snapshot_chunk(job_id, object_path, chunk_index)
    
    @activity.defn
    async def process_cdc_activity(job_id: str, event: dict) -> dict:
        integration = WorkerIntegration(settings, repository)
        return await integration.process_cdc_event(job_id, event)
    """

    def __init__(
        self,
        settings: SyncSettings,
        repository: PostgresMetadataRepository,
    ):
        self.settings = settings
        self.repository = repository
        self.worker_factory = WorkerFactory(settings, repository)

    async def execute_snapshot_chunk(
        self,
        job_id: str,
        object_path: str,
        chunk_index: int,
        chunk_size: int = 10000,
    ) -> dict[str, Any]:
        """
        Execute a snapshot chunk activity.
        
        Integration point for Temporal workflow:
        - Called by snapshot_workflow for each object/chunk
        - Returns chunk metadata for tracking progress
        """
        try:
            # Get job metadata from Postgres
            job_metadata = await self.repository.get_sync_job(job_id)
            if not job_metadata:
                raise ValueError(f"Job {job_id} not found")

            # Create snapshot worker with proper adapters
            kafka_producer = self._create_kafka_producer()
            snapshot_worker = self.worker_factory.create_snapshot_worker(
                source_type=job_metadata.source_adapter,
                target_type=job_metadata.target_adapter,
                kafka_producer=kafka_producer,
            )

            # Execute chunk
            result = await snapshot_worker.execute_snapshot_chunk(
                job_id=job_id,
                object_path=object_path,
                chunk_index=chunk_index,
                chunk_size=chunk_size,
            )

            logger.info(f"Snapshot chunk completed: {result}")
            return result

        except Exception as e:
            logger.error(f"Error executing snapshot chunk: {str(e)}", exc_info=True)
            raise

    async def process_cdc_event(
        self,
        job_id: str,
        event: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Process a CDC event activity.
        
        Integration point for Temporal workflow:
        - Called by cdc_workflow for each Kafka event
        - Returns event processing status
        """
        try:
            # Get job metadata
            job_metadata = await self.repository.get_sync_job(job_id)
            if not job_metadata:
                raise ValueError(f"Job {job_id} not found")

            # Create CDC worker
            kafka_consumer = self._create_kafka_consumer(job_id)
            kafka_producer = self._create_kafka_producer()
            cdc_worker = self.worker_factory.create_cdc_worker(
                source_type=job_metadata.source_adapter,
                target_type=job_metadata.target_adapter,
                kafka_consumer=kafka_consumer,
                kafka_producer=kafka_producer,
            )

            # Process event
            result = await cdc_worker.process_event(job_id, event)

            logger.info(f"CDC event processed: {result}")
            return result

        except Exception as e:
            logger.error(f"Error processing CDC event: {str(e)}", exc_info=True)
            raise

    async def replay_cdc_batch(
        self,
        job_id: str,
        event_batch: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """
        Replay a batch of CDC events (for recovery/conflict resolution).
        
        Integration point for Temporal workflow:
        - Called by recovery_workflow during conflict resolution
        - Ensures idempotent replay of events
        """
        try:
            job_metadata = await self.repository.get_sync_job(job_id)
            if not job_metadata:
                raise ValueError(f"Job {job_id} not found")

            kafka_consumer = self._create_kafka_consumer(job_id)
            kafka_producer = self._create_kafka_producer()
            cdc_worker = self.worker_factory.create_cdc_worker(
                source_type=job_metadata.source_adapter,
                target_type=job_metadata.target_adapter,
                kafka_consumer=kafka_consumer,
                kafka_producer=kafka_producer,
            )

            result = await cdc_worker.handle_replay(job_id, event_batch)

            logger.info(f"CDC replay completed: {result}")
            return result

        except Exception as e:
            logger.error(f"Error replaying CDC batch: {str(e)}", exc_info=True)
            raise

    def _create_kafka_producer(self) -> KafkaProducerLayer:
        """Create Kafka producer from settings."""
        config = {
            "bootstrap.servers": self.settings.kafka.bootstrap_servers,
            "security.protocol": self.settings.kafka.security_protocol,
            "client.id": f"{self.settings.kafka.client_id}-producer",
        }
        return KafkaProducerLayer(config)

    def _create_kafka_consumer(self, job_id: str) -> KafkaConsumerLayer:
        """Create Kafka consumer from settings."""
        config = {
            "bootstrap.servers": self.settings.kafka.bootstrap_servers,
            "security.protocol": self.settings.kafka.security_protocol,
            "group.id": f"{self.settings.kafka.group_id}-{job_id}",
            "client.id": f"{self.settings.kafka.client_id}-consumer",
            "auto.offset.reset": "earliest",
        }
        return KafkaConsumerLayer(config)


# REFERENCE: Integration with Temporal (for worker.py)
# ====================================================

TEMPORAL_INTEGRATION_EXAMPLE = '''
# In sync_subsystem/temporal/activities.py

from temporalio import activity
from ..infrastructure.postgres.repository import PostgresMetadataRepository
from ..configs.settings import SyncSettings
from .integration import WorkerIntegration

# Initialize global instances
settings = SyncSettings()
repository = PostgresMetadataRepository(settings)
integration = WorkerIntegration(settings, repository)


@activity.defn
async def execute_snapshot_chunk_activity(
    job_id: str,
    object_path: str,
    chunk_index: int,
    chunk_size: int = 10000,
) -> dict:
    """Temporal activity for snapshot chunk execution."""
    return await integration.execute_snapshot_chunk(
        job_id, object_path, chunk_index, chunk_size
    )


@activity.defn
async def process_cdc_event_activity(
    job_id: str,
    event: dict,
) -> dict:
    """Temporal activity for CDC event processing."""
    return await integration.process_cdc_event(job_id, event)


@activity.defn
async def replay_cdc_batch_activity(
    job_id: str,
    event_batch: list[dict],
) -> dict:
    """Temporal activity for CDC event replay."""
    return await integration.replay_cdc_batch(job_id, event_batch)
'''

# REFERENCE: Temporal Workflow Integration
# ==========================================

TEMPORAL_WORKFLOW_EXAMPLE = '''
# In sync_subsystem/temporal/workflows.py

from temporalio import workflow
from temporalio.common import RetryPolicy
from datetime import timedelta
from .activities import (
    execute_snapshot_chunk_activity,
    process_cdc_event_activity,
)


@workflow.defn
class SnapshotWorkflow:
    """Temporal workflow for snapshot phase."""

    @workflow.run
    async def run(
        self,
        job_id: str,
        object_paths: list[str],
        chunk_size: int = 10000,
    ) -> dict:
        """Execute snapshot for all objects and chunks."""
        results = []

        for object_path in object_paths:
            chunk_index = 0
            while True:
                try:
                    # Call snapshot activity
                    result = await workflow.execute_activity(
                        execute_snapshot_chunk_activity,
                        job_id,
                        object_path,
                        chunk_index,
                        chunk_size,
                        start_to_close_timeout=timedelta(minutes=30),
                        retry_policy=RetryPolicy(maximum_attempts=3),
                    )

                    results.append(result)

                    if result["status"] == "no_data":
                        break  # No more chunks for this object

                    chunk_index += 1

                except Exception as e:
                    # Handle activity failures
                    return {
                        "job_id": job_id,
                        "status": "failed",
                        "error": str(e),
                    }

        return {
            "job_id": job_id,
            "status": "completed",
            "chunks_processed": len(results),
        }


@workflow.defn
class CDCWorkflow:
    """Temporal workflow for CDC phase."""

    @workflow.run
    async def run(
        self,
        job_id: str,
        kafka_topic: str,
        max_events: int = 1000,
    ) -> dict:
        """Process CDC events from Kafka."""
        processed_count = 0

        # Poll Kafka for events and process them
        for event_num in range(max_events):
            # In practice, you'd poll Kafka here
            # For now, this is a placeholder
            event = {
                "id": f"event-{event_num}",
                "kafka_offset": event_num,
                "op": "INSERT",
            }

            try:
                result = await workflow.execute_activity(
                    process_cdc_event_activity,
                    job_id,
                    event,
                    start_to_close_timeout=timedelta(minutes=5),
                    retry_policy=RetryPolicy(maximum_attempts=3),
                )

                if result["status"] == "processed":
                    processed_count += 1

            except Exception as e:
                return {
                    "job_id": job_id,
                    "status": "failed",
                    "processed_count": processed_count,
                    "error": str(e),
                }

        return {
            "job_id": job_id,
            "status": "completed",
            "events_processed": processed_count,
        }
'''
