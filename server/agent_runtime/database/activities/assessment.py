from providers.database.registry import registry
from temporalio import activity
from agent_runtime.database.domain.model import (
    DatabaseAssessment,
    DatabaseEndpoint,
)

@activity.defn
async def assess_database(endpoint: DatabaseEndpoint) -> DatabaseAssessment:
    """Assess the database using the appropriate provider based on the engine."""


    try:
        activity.logger.info(f"Assessing database at {endpoint.host}:{endpoint.port} using engine {endpoint.engine}")
        provider = registry.get_provider(endpoint.engine)
        activity.logger.info(f"Using provider: {provider.__class__.__name__} for engine: {endpoint.engine}")
        # activity.logger.info(f"Testing connection to database at {endpoint.host}:{endpoint.port}")
        # connection_successful = await provider.test_connection(endpoint)
        # if not connection_successful:
        #     activity.logger.error(f"Failed to connect to the database at {endpoint.host}:{endpoint.port}")
        #     raise ConnectionError(f"Failed to connect to the database at {endpoint.host}:{endpoint.port}")
        # activity.logger.info(f"Connection successful to database at {endpoint.host}:{endpoint.port}. Proceeding with assessment.")
        return await provider.assess_database(endpoint)
    except ValueError as e:
        # Handle the case where no provider is registered for the given engine
        activity.logger.error(f"No provider registered for engine: {endpoint.engine}. Error: {e}")
        raise ValueError(f"Error assessing database: {e}")
    except ConnectionError as e:
        # Handle connection errors
        activity.logger.error(f"Connection error while assessing database at {endpoint.host}:{endpoint.port}. Error: {e}")
        raise ConnectionError(f"Error assessing database: {e}")

    
