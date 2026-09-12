from abc import ABC, abstractmethod
from agent_runtime.database.domain.model import (
    DatabaseAssessment,
    DatabaseEndpoint,
)

class DatabaseProvider(ABC):
    """Abstract base class for database providers."""

    @abstractmethod
    async def assess_database(self, endpoint: DatabaseEndpoint) -> DatabaseAssessment:
        """Assess the database and return a DatabaseAssessment object."""
        pass

    @abstractmethod
    async def test_connection(self, endpoint: DatabaseEndpoint) -> bool:
        """Test the database connection and return True if successful, False otherwise."""
        pass

    @abstractmethod
    async def discover_databases(self, token_id: str) -> list[DatabaseEndpoint]:
        """Discover databases and return a list of DatabaseEndpoint objects."""
        pass

    @abstractmethod
    async def get_schema(self, endpoint: DatabaseEndpoint) -> dict:
        """Get the database schema and return it as a dictionary."""
        pass

    @abstractmethod
    async def get_replication_position(self, endpoint: DatabaseEndpoint) -> str:
        """Get the replication position of the database and return it as a string."""
        pass

    @abstractmethod
    async def freeze_writes(self, endpoint: DatabaseEndpoint) -> bool:
        """Freeze writes to the database and return True if successful, False otherwise."""
        pass

    @abstractmethod
    async def unfreeze_writes(self, endpoint: DatabaseEndpoint) -> bool:
        """Unfreeze writes to the database and return True if successful, False otherwise."""
        pass

    @abstractmethod
    async def health_check(self, endpoint: DatabaseEndpoint) -> bool:
        """Perform a health check on the database and return True if healthy, False otherwise."""
        pass
