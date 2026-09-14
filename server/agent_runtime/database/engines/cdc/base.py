from abc import ABC, abstractmethod


class CDCProvider(ABC):
    """Abstract base class for Change Data Capture (CDC) providers."""


    @abstractmethod
    async def prepare(self, source, target) -> None:
        """Prepare the source and target for CDC."""
        pass

    @abstractmethod
    async def start(self) -> None:
        """Start the CDC process."""
        pass

    @abstractmethod
    async def stop(self) -> None:
        """Stop the CDC process."""
        pass

    @abstractmethod
    async def get_changes(self) -> list:
        """Get the changes captured by the CDC process."""
        pass

    @abstractmethod
    async def get_lag(self) -> float:
        """Get the lag of the CDC process."""
        pass

    @abstractmethod
    async def get_checkpoint(self) -> dict:
        """Get the checkpoint of the CDC process."""
        pass