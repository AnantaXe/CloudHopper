from abc import ABC, abstractmethod

class HeterogeneousSchemaMigrationEngine(ABC):
    """Abstract base class for heterogeneous schema migration engines."""

    @abstractmethod
    async def migrate(self, source, target) -> None:

        target_schema = self.transform(source_model=source)

        await self.apply(target=target, schema=target_schema)

    @abstractmethod
    async def assess(self, source) -> None:
        pass

    @abstractmethod
    async def transform(self, source_model) -> None:
        return source_model  # Default implementation returns the source model unchanged

    @abstractmethod
    def validate(self, source, target) -> None:
        pass

    @abstractmethod
    def rollback(self, source, target) -> None:
        pass

    @abstractmethod
    async def apply(self, target, schema) -> None:
        """Apply the migration to the target database."""
        pass