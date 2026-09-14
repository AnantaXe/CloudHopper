from fastapi import FastAPI
from shared.config.settings import *
# from server.control_plane.api.discovery_api import (
#     router as discovery_router
# )

# from control_plane.api.workflow_api import (
#     router as workflow_router
# )

# from control_plane.api.auth_api import (
#     router as auth_router
# )

from control_plane.api.routes.database_migration import (
    router as database_migration_router
)

CONTROL_PLANE_HOST = "localhost"
CONTROL_PLANE_PORT = 8006

app = FastAPI(
    title="CloudHopper Control Plane API",
    description="API for managing cloud resources and workflows",
    version="1.0.0"
)

# app.include_router(
#     discovery_router,
# )
# app.include_router(
#     workflow_router,
# )
# app.include_router(
#     auth_router,
# )
app.include_router(
    database_migration_router,
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=CONTROL_PLANE_HOST, port=CONTROL_PLANE_PORT, reload=True)