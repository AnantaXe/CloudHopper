from __future__ import annotations

from confluent_kafka import Consumer, KafkaException
from typing import Any


class KafkaConsumerLayer:
    def __init__(self, config: dict[str, Any]) -> None:
        self.consumer = Consumer(config)

    def subscribe(self, topics: list[str]) -> None:
        self.consumer.subscribe(topics)

    def poll(self, timeout: float = 1.0) -> Any:
        msg = self.consumer.poll(timeout)
        if msg is None:
            return None
        if msg.error():
            raise KafkaException(msg.error())
        return msg

    def commit(self, msg: Any) -> None:
        self.consumer.commit(msg)

    def close(self) -> None:
        self.consumer.close()
