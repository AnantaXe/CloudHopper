from datetime import datetime
from pydantic import BaseModel, Field

from .enums import (
    MigrationType,
    MigrationStage,
    MigrationStrategy,
    MigrationStatus,
)

class DatabaseEndpoint(BaseModel):
    """Database endpoint model."""

    engine: str = Field(..., description="Database engine.")
    version: str = Field(..., description="Database version.")
    host: str = Field(..., description="Database host.")
    port: int = Field(..., description="Database port.")
    username: str = Field(..., description="Database username.")
    password: str = Field(..., description="Database password.")
    database_name: str = Field(..., description="Database name.")
    provider: str = Field(..., description="Database provider.")
    service_name: str = Field(..., description="Database service name.")

class DatabaseMigrationRequest(BaseModel):
    """Database migration request model."""

    source : DatabaseEndpoint = Field(..., description="Source database endpoint.")
    target : DatabaseEndpoint = Field(..., description="Target database endpoint.")
    migration_strategy: MigrationStrategy = Field(..., description="Migration strategy.")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp.")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp.")

class DatabaseAssessment(BaseModel):
    """Database assessment model."""

    engine: str = Field(..., description="Database engine.")
    version: str = Field(..., description="Database version.")
    database_size_gb: float = Field(..., description="Database size in GB.")

    schemas: int = Field(..., description="Database schema.")
    indexes: int = Field(..., description="Database indexes.")
    tables: int = Field(..., description="Database tables.")
    views: int = Field(..., description="Database views.")
    stored_procedures: int = Field(..., description="Database stored procedures.")
    functions: int = Field(..., description="Database functions.")
    triggers: int = Field(..., description="Database triggers.")
    foreign_keys: int = Field(..., description="Database foreign keys.")

    extensions: list[str] = Field(..., description="Database extensions.")

    avg_connections: int = Field(..., description="Average database connections.")
    peak_connections: int = Field(..., description="Peak database connections.")

    cpu_percent: float = Field(..., description="CPU usage percentage.")
    memory_percent: float = Field(..., description="Memory usage percentage.")
    iops: int = Field(..., description="Input/output operations per second.")


class CompatibilityReport(BaseModel):
    """Compatibility assessment model."""

    migration_type: MigrationType = Field(..., description="Migration type.")
    compatibility_score: float = Field(..., description="Compatibility score.")

    schema_compatible: bool = Field(..., description="Schema compatibility.")
    data_compatible: bool = Field(..., description="Data compatibility.")

    blocking_issues: list[str] = Field(..., description="List of blocking issues.", default_factory=list)
    warning_issues: list[str] = Field(..., description="List of warning issues.", default_factory=list)

    transformations_required: list[str] = Field(..., description="List of required transformations.", default_factory=list)


class TargetArchitecture(BaseModel):
    """Target architecture model."""

    provider: str = Field(..., description="Target database provider.")
    engine: str = Field(..., description="Target database engine.")
    version: str = Field(..., description="Target database version.")
    service_name: str = Field(..., description="Target database service name.")

    instance_class: str = Field(..., description="Target database instance class.")
    multi_az: bool = Field(..., default=True, description="Whether the target database is multi-AZ.")
    storage_gb: int = Field(..., description="Target database storage size in GB.")



class MigrationPlanStep(BaseModel):

    """Migration plan step model."""

    step_id: int = Field(..., description="Migration plan step ID.")
    name: str = Field(..., description="Migration plan step name.")
    stage: MigrationStage = Field(..., description="Migration plan step stage.")
    depends_on: list[int] = Field(..., description="List of step IDs this step depends on.", default_factory=list)

    required_approval: bool = Field(..., default=False, description="Whether this step requires approval.")


class MigrationPlan(BaseModel):
    """Migration plan model."""

    migration_id: str = Field(..., description="Migration plan ID.")
    migration_strategy: MigrationStrategy = Field(..., description="Migration strategy.")
    migration_type: MigrationType = Field(..., description="Migration type.")
    status: MigrationStatus = Field(..., description="Migration plan status.")

    steps: list[MigrationPlanStep] = Field(..., description="List of migration plan steps.", default_factory=list)

    rollback_enabled: bool = Field(..., default=True, description="Whether rollback is enabled for this migration plan.")
    created_at: datetime = Field(..., description="Migration plan creation timestamp.")
    updated_at: datetime = Field(..., description="Migration plan last update timestamp.")

class MigrationState(BaseModel):
    """Migration state model."""

    migration_id: str = Field(..., description="Migration ID.")
    current_stage: MigrationStage = Field(..., description="Current migration stage.")
    status: MigrationStatus = Field(..., description="Current migration status.")

    checkpoints: list[MigrationPlanStep] = Field(..., description="List of completed migration plan steps.", default_factory=list)
    progress_percent: float = Field(..., default=0.0, description="Migration progress percentage.")
    created_at: datetime = Field(..., description="Creation timestamp.")
    updated_at: datetime = Field(..., description="Last update timestamp.")