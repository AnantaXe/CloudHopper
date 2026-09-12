from providers.database.registry import registry

from agent_runtime.database.domain.model import (
    DatabaseAssessment,
    DatabaseEndpoint,
)


async def assess_database(endpoint: DatabaseEndpoint) -> DatabaseAssessment:
    """Assess the database using the appropriate provider based on the engine."""

    try:
        provider = registry.get_provider(endpoint.engine)
        connection_successful = await provider.test_connection(endpoint)
        if not connection_successful:
            raise ConnectionError(f"Failed to connect to the database at {endpoint.host}:{endpoint.port}")
        return await provider.assess_database(endpoint)
    except ValueError as e:
        # Handle the case where no provider is registered for the given engine
        raise ValueError(f"Error assessing database: {e}")
    except ConnectionError as e:
        # Handle connection errors
        raise ConnectionError(f"Error assessing database: {e}")

    
