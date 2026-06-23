from __future__ import annotations

from typing import Any
import json
import logging
from datetime import datetime

from ..adapters.base import CDCAdapter, TargetAdapter
from ..infrastructure.postgres.repository import PostgresMetadataRepository
from ..infrastructure.debezium.event_processor import CDCEventProcessor
from ..kafka.consumer import KafkaConsumerLayer
from ..kafka.producer import KafkaProducerLayer
from ..kafka.topics import KafkaTopic

logger = logging.getLogger(__name__)


class CDCWorker:
    """
    Worker that orchestrates CDC (Change Data Capture) phase:
    1. Listens to Kafka CDC events
    2. Transforms and validates event ordering
    3. Applies changes to target adapter
    4. Tracks CDC offsets in repository
    5. Publishes CDC events for validation/conflict resolution
    """

    def __init__(
        self,
        cdc_adapter: CDCAdapter,
        target_adapter: TargetAdapter,
        repository: PostgresMetadataRepository,
        kafka_consumer: KafkaConsumerLayer,
        kafka_producer: KafkaProducerLayer,
    ):
        self.cdc_adapter = cdc_adapter
        self.target_adapter = target_adapter
        self.repository = repository
        self.kafka_consumer = kafka_consumer
        self.kafka_producer = kafka_producer
        self.event_processor = CDCEventProcessor()

    async def process_event(
        self,
        job_id: str,
        event: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Process a single CDC event:
        1. Transform event (Debezium format → standard format)
        2. Validate event ordering
        3. Apply to target adapter
        4. Track offset
        5. Publish to Kafka for downstream processing
        """
        try:
            event_id = event.get("id", "unknown")
            logger.info(f"Processing CDC event: job_id={job_id}, event_id={event_id}")

            # Step 1: Transform event from Debezium format
            transformed_event = await self.event_processor.transform_event(event)
            logger.debug(f"Transformed event: {transformed_event}")

            # Step 2: Validate ordering (LSN/timestamp)
            is_ordered = await self.event_processor.validate_ordering(transformed_event)
            if not is_ordered:
                logger.warning(f"Event ordering violation detected for event {event_id}")
                return {
                    "job_id": job_id,
                    "event_id": event_id,
                    "status": "ordering_violation",
                }

            # Step 3: Apply change to target adapter
            await self.target_adapter.apply_cdc_event(transformed_event)
            logger.info(f"Applied CDC event to target: {event_id}")

            # Step 4: Track CDC offset in Postgres
            offset_data = {
                "job_id": job_id,
                "event_id": event_id,
                "offset": event.get("kafka_offset", 0),
                "partition": event.get("kafka_partition", 0),
                "processed_at": datetime.utcnow().isoformat(),
            }
            # Note: You may need to add update_cdc_offset method to repository
            # await self.repository.update_cdc_offset(offset_data)

            # Step 5: Publish CDC event to Kafka for validation/conflict resolution
            event_payload = {
                "job_id": job_id,
                "event_id": event_id,
                "event_type": transformed_event.get("op", "unknown"),  # INSERT, UPDATE, DELETE
                "table": transformed_event.get("table"),
                "before": transformed_event.get("before"),
                "after": transformed_event.get("after"),
            }
            await self._publish_event(
                KafkaTopic.CDC_EVENTS,
                job_id,
                event_payload,
            )

            return {
                "job_id": job_id,
                "event_id": event_id,
                "status": "processed",
                "operation": transformed_event.get("op"),
            }

        except Exception as e:
            logger.error(
                f"Error processing CDC event: {str(e)}",
                exc_info=True,
            )
            return {
                "job_id": job_id,
                "event_id": event.get("id", "unknown"),
                "status": "failed",
                "error": str(e),
            }

    async def handle_replay(
        self,
        job_id: str,
        event_batch: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """
        Replay a batch of CDC events (used for recovery/conflict resolution):
        1. Process each event in batch order
        2. Ensure idempotency (detect and skip duplicates)
        3. Track batch progress
        4. Publish replay completion event
        """
        try:
            logger.info(f"Starting replay of {len(event_batch)} events for job_id={job_id}")

            processed_count = 0
            skipped_count = 0
            failed_count = 0

            for event in event_batch:
                try:
                    # Check for duplicate (idempotency key)
                    event_id = event.get("id")
                    is_duplicate = await self._is_duplicate_event(job_id, event_id)

                    if is_duplicate:
                        logger.debug(f"Skipping duplicate event: {event_id}")
                        skipped_count += 1
                        continue

                    # Process event
                    result = await self.process_event(job_id, event)

                    if result["status"] == "processed":
                        processed_count += 1
                    else:
                        failed_count += 1

                except Exception as e:
                    logger.error(f"Error processing event during replay: {str(e)}")
                    failed_count += 1

            # Publish replay completion
            replay_result = {
                "job_id": job_id,
                "replay_count": len(event_batch),
                "processed_count": processed_count,
                "skipped_count": skipped_count,
                "failed_count": failed_count,
                "status": "replay_completed",
            }
            await self._publish_event(
                KafkaTopic.RECOVERY_EVENTS,
                job_id,
                replay_result,
            )

            logger.info(f"Replay completed: {replay_result}")
            return replay_result

        except Exception as e:
            logger.error(f"Error handling replay: {str(e)}", exc_info=True)
            return {
                "job_id": job_id,
                "replay_count": len(event_batch),
                "status": "failed",
                "error": str(e),
            }

    async def _is_duplicate_event(
        self,
        job_id: str,
        event_id: str,
    ) -> bool:
        """
        Check if event has already been processed (idempotency check).
        You can implement this by querying Postgres or Redis.
        """
        # Placeholder: In production, check against a processed events table
        # or distributed cache like Redis
        return False

    async def _publish_event(
        self,
        topic: KafkaTopic,
        key: str,
        payload: dict[str, Any],
    ) -> None:
        """
        Publish CDC event to Kafka topic.
        """
        try:
            event_bytes = json.dumps(payload).encode("utf-8")
            self.kafka_producer.publish(topic.name, key, event_bytes)
        except Exception as e:
            logger.error(f"Error publishing event to Kafka: {str(e)}", exc_info=True)
