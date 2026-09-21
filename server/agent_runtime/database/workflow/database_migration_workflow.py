"""Developer Notes: Use Temporal activity retry policies and explicit compensation/rollback paths rather than letting exceptions simply terminate the workflow."""

from datetime import timedelta
from temporalio import workflow
from agent_runtime.database.activities.assessment import assess_database
from agent_runtime.database.activities.bulk_load import initial_bulk_load
from agent_runtime.database.activities.cdc import start_cdc
from agent_runtime.database.activities.cutover import cutover
from agent_runtime.database.activities.rollback import rollback
from agent_runtime.database.activities.compatibility import compatibility
from agent_runtime.database.activities.architecture_recommender import recommend_architect
from agent_runtime.database.activities.strategy import determine_strategy
from agent_runtime.database.activities.migration_plan import generate_mig_plan
from agent_runtime.database.activities.validate_migration import validate_mig_plan
from agent_runtime.database.activities.provision_target import provision_target_database
from agent_runtime.database.activities.request_approval import request_migration_approval
from agent_runtime.database.domain.model import DatabaseMigrationContext

@workflow.defn
class DatabaseMigrationWorkflow:

    """Database migration workflow definition."""

    @workflow.run
    async def run(self, context: DatabaseMigrationContext) -> None:
        """Run the database migration workflow."""
        request = context.request

        migration_id = context.migration_id

        assessment = await workflow.execute_activity(
            assess_database,
            request.source,
            start_to_close_timeout=timedelta(minutes=10),
        )

        compatibility_ = await workflow.execute_activity(
            compatibility,
            request.target,
            start_to_close_timeout=timedelta(minutes=5),
        )

        architecture = await workflow.execute_activity(
           recommend_architect,
           request,
           start_to_close_timeout=timedelta(minutes=5),
        )

        strategy = await workflow.execute_activity(
            determine_strategy,
            request,
            start_to_close_timeout=timedelta(minutes=2),
        )

        plan = await workflow.execute_activity(
            generate_mig_plan,
            request,
            start_to_close_timeout=timedelta(minutes=10),
        )

        await workflow.execute_activity(
            validate_mig_plan,
            request,
            start_to_close_timeout=timedelta(minutes=2),
        )

        await workflow.execute_activity(
            request_migration_approval,
            request,
            start_to_close_timeout=timedelta(minutes=2),
        )

        await workflow.execute_activity(
            provision_target_database,
            request,
            start_to_close_timeout=timedelta(minutes=30),
        )

        if compatibility.migration_type == "HOMOGENEOUS":
            await self._run_homogeneous(request, plan)
        else:
            await self._run_heterogeneous(request, plan)


        return {
            "status": "Migration workflow completed successfully",
            "migration_plan": request.migration_id
        }


    async def _run_homogeneous(self, request, plan) -> None:
        """Run the homogeneous migration workflow."""

        # migrate_schema -> initial_bulk_data_load -> start_cdc -> validate_migration -> request_cutover_approval -> cutover -> post_migration_verification

        request = request.request

        await workflow.execute_activity(
            "migrate_schema",
            args=[
                request,
                plan
            ],
            start_to_close_timeout=timedelta(hours=1),
        )

        await workflow.execute_activity(
            initial_bulk_load,
            args=[
                request,
                plan
            ],
            start_to_close_timeout=timedelta(hours=24),
        )

        await workflow.execute_activity(
            start_cdc,
            args=[
                request,
                plan
            ],
            start_to_close_timeout=timedelta(minutes=30),
        )

        await workflow.execute_activity(
            "validate_migration",
            args=[
                request,
                plan
            ],
            start_to_close_timeout=timedelta(hours=2),
        )

        await workflow.execute_activity(
            "request_cutover_approval",
            args=[
                request,
                plan
            ],
            start_to_close_timeout=timedelta(minutes=5),
        )

        await workflow.execute_activity(
            cutover,
            args=[
                request,
                plan
            ],
            start_to_close_timeout=timedelta(hours=1),
        )

        await workflow.execute_activity(
            "post_migration_verification",
            args=[
                request,
                plan  
            ], 
            start_to_close_timeout=timedelta(hours=2),
        )


    async def _run_heterogeneous(self, request, plan) -> None:
        """Run the heterogeneous migration workflow."""

        # extract_source_schema -> transform_schema -> apply_target_schema -> initial_bulk_data_load -> start_cdc -> validate_migration -> request_cutover_approval -> cutover -> post_migration_verification ->

        request = request.request

        await workflow.execute_activity(
            "extract_source_schema",
            args=[
                request,
                plan
            ],
            start_to_close_timeout=timedelta(hours=1),
        )

        await workflow.execute_activity(
            "transform_schema",
            args=[
                request,
                plan
            ],
            start_to_close_timeout=timedelta(hours=2),
        )

        await workflow.execute_activity(
            "apply_target_schema",
            args=[
                request,
                plan
            ],
            start_to_close_timeout=timedelta(hours=2),
        )

        await workflow.execute_activity(
            initial_bulk_load,
            args=[
                request,
                plan
            ],
            start_to_close_timeout=timedelta(hours=24),
        )

        await workflow.execute_activity(
            start_cdc,
            args=[
                request,
                plan
            ],
            start_to_close_timeout=timedelta(minutes=30),
        )

        await workflow.execute_activity(
            "validate_migration",
            args=[
                request,
                plan
            ],
            start_to_close_timeout=timedelta(hours=2),
        )

        await workflow.execute_activity(
            "request_cutover_approval",
            args=[
                request,
                plan
            ],
            start_to_close_timeout=timedelta(minutes=5),
        )

        await workflow.execute_activity(
            cutover,
            args=[
                request,
                plan
            ],
            start_to_close_timeout=timedelta(hours=1),
        )

        await workflow.execute_activity(
            "post_migration_verification",
            args=[
                request,
                plan  
            ], 
            start_to_close_timeout=timedelta(hours=2),
        )