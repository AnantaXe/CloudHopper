from __future__ import annotations

from ..configs.settings import SyncSettings
from ..infrastructure.postgres.repository import PostgresMetadataRepository
from ..application.services.sync_control_plane import SyncControlPlaneService
from ..application.services.validation_service import DataValidationService
from ..application.services.reconciliation_service import ReconciliationService
from ..application.services.decision_engine import AgentDecisionEngine

settings = SyncSettings()
repository = PostgresMetadataRepository(settings.postgres)

sync_control_plane_service = SyncControlPlaneService(settings, repository)
validation_service = DataValidationService(repository)
reconciliation_service = ReconciliationService(repository)
decision_engine = AgentDecisionEngine(repository)
