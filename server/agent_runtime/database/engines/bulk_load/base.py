from abc import ABC, abstractmethod

class BulkLoadEngine(ABC):
    """Abstract base class for bulk load engines."""

    @abstractmethod
    async def prepare(self, source, target) -> None:
        """Prepare the source and target for bulk load."""
        pass

    @abstractmethod
    async def start(self, source, target) -> None:
        """Start the bulk load process."""
        pass

    @abstractmethod
    async def get_progress(self) -> float:
        """Get the progress of the bulk load process."""
        pass

    @abstractmethod
    async def wait_until_complete(self) -> None:
        """Wait until the bulk load process is complete."""
        pass

    @abstractmethod
    async def cancel(self) -> None:
        """Cancel the bulk load process."""
        pass