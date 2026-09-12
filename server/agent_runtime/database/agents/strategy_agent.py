from database.domain.enums import (
    MigrationType,
    MigrationStrategy,
)

from database.domain.model import (
    CompatibilityReport,
)

class StrategyAgent:

    async def determine_strategy(self, compatibility_report: CompatibilityReport) -> MigrationStrategy:
        """Determine the migration strategy based on the compatibility report."""

        if compatibility_report.migration_type == MigrationType.HOMOGENEOUS:
            return MigrationStrategy.REPLATFORM

        return MigrationStrategy.REFACTOR