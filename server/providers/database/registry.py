from providers.database.base import DatabaseProvider
from providers.database.postgresql.connector import PostgreSQLProvider

class DatabaseProviderRegistry:

    def __init__(self):
        self._providers: dict[str, DatabaseProvider] = {}

    def register(self, engine: str, provider: DatabaseProvider):
        """Register a new database provider."""

        self._providers[engine.lower()] = provider

    def get_provider(self, engine: str) -> DatabaseProvider:
        """Get a database provider by engine name."""

        try:
            return self._providers[engine.lower()]
        except KeyError:
            raise ValueError(f"No provider registered for engine: {engine}")



registry = DatabaseProviderRegistry()
registry.register("postgresql", PostgreSQLProvider())

# registry.register("mysql", MySQLProvider())
# registry.register("mssql", MSSQLProvider())
# registry.register("oracle", OracleProvider())
# registry.register("mongodb", MongoDBProvider())