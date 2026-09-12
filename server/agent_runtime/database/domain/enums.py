from enums import StrEnum

class MigrationType(StrEnum):
    """Migration type enum."""

    HOMOGENEOUS = "homogeneous"
    HETEROGENEOUS = "heterogeneous"

class MigrationStage(StrEnum):
    """Migration stage enum."""

    ASSESSMENT = "assessment"
    COMPATIBILITY = "compatibility"
    ARCHITECTURE = "architecture"
    STRATEGY = "strategy"
    PLANNING = "planning"
    PROVISIONING = "provisioning"
    SCHEMA_MIGRATION = "schema_migration"
    BULK_LOAD = "bulk_load"
    CDC = "cdc"
    VALIDATION = "validation"
    CUTOVER = "cutover"
    POST_VERIFICATION = "post_verification"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLBACK = "rollback"


class MigrationStrategy(StrEnum):
    """Migration strategy enum."""

    REHOST = "rehost"
    REPLATFORM = "replatform"
    REFACTOR = "refactor"
    RETAIN = "retain"
    REBUILD = "rebuild"
    REPLACE = "replace"
    RETIRE = "retire"
    REPURCHASE = "repurchase"

class MigrationStatus(StrEnum):
    """Migration status enum."""

    PENDING = "pending"
    RUNNING = "running"
    ROLLED_BACK = "rolled_back"
    COMPLETED = "completed"
    FAILED = "failed"
    WAITING_APPROVAL = "waiting_approval"
    PAUSED = "paused"

