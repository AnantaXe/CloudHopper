"""Developer Notes: The strategy agent should be designed to make decisions based on the compatibility report, assessment, application dependencies, business criticality and other relevant factors. It should be able to handle different migration scenarios and provide appropriate strategies for each case."""

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