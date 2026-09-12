from fastapi import FastAPI
from shared.config.settings import *
from control_plane.api.discovery_api import (
    router as discovery_router
)

from control_plane.api.workflow_api import (
    router as workflow_router
)

from control_plane.api.auth_api import (
    router as auth_router
)

app = FastAPI(
    title="CloudHopper Control Plane API",
    description="API for managing cloud resources and workflows",
    version="1.0.0"
)

app.include_router(
    discovery_router,
)
app.include_router(
    workflow_router,
)
app.include_router(
    auth_router,
)