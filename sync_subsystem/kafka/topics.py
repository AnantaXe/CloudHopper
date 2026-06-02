from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class KafkaTopic:
    name: str
    partitions: int = 16
    replication_factor: int = 3
    compacted: bool = False


SYNC_SNAPSHOT_STARTED = KafkaTopic(name="sync.snapshot.started", partitions=8, replication_factor=3)
SYNC_SNAPSHOT_COMPLETED = KafkaTopic(name="sync.snapshot.completed", partitions=8, replication_factor=3)
SYNC_CDC_EVENTS = KafkaTopic(name="sync.cdc.events", partitions=32, replication_factor=3)
SYNC_VALIDATION_EVENTS = KafkaTopic(name="sync.validation.events", partitions=8, replication_factor=3)
SYNC_CONFLICT_EVENTS = KafkaTopic(name="sync.conflict.events", partitions=4, replication_factor=3)
SYNC_RECOVERY_EVENTS = KafkaTopic(name="sync.recovery.events", partitions=4, replication_factor=3)
SYNC_AUDIT_EVENTS = KafkaTopic(name="sync.audit.events", partitions=4, replication_factor=3, compacted=True)
SYNC_CUTOVER_EVENTS = KafkaTopic(name="sync.cutover.events", partitions=4, replication_factor=3)


RETRY_SUFFIX = ".retry"
DLQ_SUFFIX = ".dlq"


def topic_name(topic: KafkaTopic) -> str:
    return topic.name
