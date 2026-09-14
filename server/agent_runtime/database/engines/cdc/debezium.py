from abc import ABC, abstractmethod

class DebeziumCDCProvider(ABC):
    """Abstract base class for Debezium Change Data Capture (CDC) providers."""

    @abstractmethod
    async def prepare(self, source, target) -> None:
        """Prepare the source and target for Debezium CDC."""
        pass

    @abstractmethod
    async def start(self) -> None:
        """Start the Debezium CDC process."""
        pass

    @abstractmethod
    async def stop(self) -> None:
        """Stop the Debezium CDC process."""
        pass

    @abstractmethod
    async def get_changes(self) -> list:
        """Get the changes captured by the Debezium CDC process."""
        pass

    @abstractmethod
    async def get_lag(self) -> float:
        """Get the lag of the Debezium CDC process."""
        return 0.0  # Default implementation returns 0.0 lag

    @abstractmethod
    async def get_checkpoint(self) -> str:
        """Get the checkpoint of the Debezium CDC process."""
        return "source_position"  # Default implementation returns a placeholder source position