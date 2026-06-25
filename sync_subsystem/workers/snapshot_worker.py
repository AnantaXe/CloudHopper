from __future__ import annotations

from typing import Any
import json
import logging

from ..adapters.base import SourceAdapter, TargetAdapter, StorageAdapter
from ..infrastructure.postgres.repository import PostgresMetadataRepository
from ..domain.models import SyncCheckpoint
from ..kafka.producer import KafkaProducerLayer
from ..kafka.topics import KafkaTopic

logger = logging.getLogger(__name__)


class SnapshotWorker:
    """
    Worker that orchestrates snapshot phase:
    1. Reads chunks from source adapter
    2. Applies chunks to target adapter
    3. Persists checkpoints to storage adapter
    4. Tracks progress in Postgres repository
    5. Publishes events to Kafka
    """

    def __init__(
        self,
        source_adapter: SourceAdapter,
        target_adapter: TargetAdapter,
        storage_adapter: StorageAdapter,
        repository: PostgresMetadataRepository,
        kafka_producer: KafkaProducerLayer | None = None,
    ):
        self.source_adapter = source_adapter
        self.target_adapter = target_adapter
        self.storage_adapter = storage_adapter
        self.repository = repository
        self.kafka_producer = kafka_producer

    async def execute_snapshot_chunk(
        self,
        job_id: str,
        object_path: str,
        chunk_index: int,
        chunk_size: int,
    ) -> dict[str, Any]:
        """
        Execute a single snapshot chunk:
        1. Read records from source
        2. Apply to target
        3. Persist checkpoint
        """
        try:
            logger.info(
                f"Starting snapshot chunk: job_id={job_id}, object_path={object_path}, "
                f"chunk_index={chunk_index}, chunk_size={chunk_size}"
            )

            # Step 1: Read snapshot chunk from source adapter
            records = await self.source_adapter.read_snapshot(object_path, chunk_size)
            record_count = len(records)

            if not records:
                logger.warning(f"No records read for chunk {chunk_index} from {object_path}")
                return {
                    "job_id": job_id,
                    "object_path": object_path,
                    "chunk_index": chunk_index,
                    "record_count": 0,
                    "status": "no_data",
                }

            # Step 2: Apply records to target adapter in batch
            await self.target_adapter.apply_snapshot_batch(records)
            logger.info(f"Applied {record_count} records to target")

            # Step 3: Build checkpoint
            checkpoint_data = {
                "job_id": job_id,
                "object_path": object_path,
                "chunk_index": chunk_index,
                "record_count": record_count,
                "last_key": records[-1] if records else None,
            }

            # Step 4: Persist checkpoint to storage
            await self.storage_adapter.checkpoint(job_id, checkpoint_data)
            logger.info(f"Checkpoint persisted for chunk {chunk_index}")

            # Step 5: Update Postgres metadata
            checkpoint_model = SyncCheckpoint(
                job_id=job_id,
                object_path=object_path,
                completed_chunks=chunk_index + 1,
                last_processed_key=str(records[-1]) if records else None,
            )
            # Note: You may need to add this method to the repository
            # await self.repository.update_checkpoint(checkpoint_model)

            # Step 6: Publish event to Kafka (optional)
            if self.kafka_producer:
                event_payload = {
                    "job_id": job_id,
                    "event_type": "snapshot_chunk_completed",
                    "chunk_index": chunk_index,
                    "record_count": record_count,
                }
                await self._publish_event(
                    KafkaTopic.SNAPSHOT_COMPLETED,
                    job_id,
                    event_payload,
                )

            return {
                "job_id": job_id,
                "object_path": object_path,
                "chunk_index": chunk_index,
                "record_count": record_count,
                "status": "completed",
            }

        except Exception as e:
            logger.error(
                f"Error executing snapshot chunk: {str(e)}",
                exc_info=True,
            )
            return {
                "job_id": job_id,
                "object_path": object_path,
                "chunk_index": chunk_index,
                "status": "failed",
                "error": str(e),
            }

    async def resume_snapshot(
        self,
        job_id: str,
        checkpoint: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Resume snapshot from a checkpoint.
        Reads the checkpoint and continues from the last processed position.
        """
        try:
            logger.info(f"Resuming snapshot for job_id={job_id} from checkpoint={checkpoint}")

            # Read stored checkpoint
            stored_checkpoint = await self.storage_adapter.read_checkpoint(job_id)
            if not stored_checkpoint:
                logger.warning(f"No checkpoint found for job {job_id}")
                return {
                    "job_id": job_id,
                    "status": "no_checkpoint",
                }

            # Continue from where we left off
            last_chunk_index = stored_checkpoint.get("chunk_index", -1)
            object_path = stored_checkpoint.get("object_path")

            logger.info(
                f"Resuming from chunk_index={last_chunk_index}, object_path={object_path}"
            )

            return {
                "job_id": job_id,
                "resume_from_chunk": last_chunk_index,
                "object_path": object_path,
                "status": "resumed",
            }

        except Exception as e:
            logger.error(f"Error resuming snapshot: {str(e)}", exc_info=True)
            return {
                "job_id": job_id,
                "status": "failed",
                "error": str(e),
            }

    async def _publish_event(
        self,
        topic: KafkaTopic,
        key: str,
        payload: dict[str, Any],
    ) -> None:
        """
        Publish event to Kafka topic.
        """
        if not self.kafka_producer:
            return
        try:
            event_bytes = json.dumps(payload).encode("utf-8")
            self.kafka_producer.publish(topic.name, key, event_bytes)
        except Exception as e:
            logger.error(f"Error publishing event to Kafka: {str(e)}", exc_info=True)
