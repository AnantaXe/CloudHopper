from __future__ import annotations

from confluent_kafka import Producer
from typing import Any


class KafkaProducerLayer:
    def __init__(self, config: dict[str, Any]) -> None:
        self.producer = Producer(config)

    def publish(self, topic: str, key: str, value: bytes, headers: dict[str, str] | None = None) -> None:
        self.producer.produce(topic, key=key.encode("utf-8"), value=value, headers=headers)
        self.producer.poll(0)

    def flush(self, timeout: float = 30.0) -> None:
        self.producer.flush(timeout)
