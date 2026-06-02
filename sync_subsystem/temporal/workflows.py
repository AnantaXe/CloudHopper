from __future__ import annotations

from datetime import timedelta

# NOTE: install temporalio to use these workflow definitions
try:
    from temporalio import workflow
except ImportError:  # pragma: no cover
    class _WorkflowProxy:
        @staticmethod
        def defn(cls):
            return cls

        @staticmethod
        def run(fn):
            return fn

        @staticmethod
        def signal(fn):
            return fn

        @staticmethod
        def query(fn):
            return fn

        logger = None
        Versioning = type("Versioning", (), {"get_version": staticmethod(lambda *args, **kwargs: 1)})
        info = type("Info", (), {"task_queue": "cloudhopper-sync-worker"})
        @staticmethod
        async def execute_child_workflow(*args, **kwargs):
            return None
        @staticmethod
        async def sleep(duration):
            return None
        @staticmethod
        async def wait_signal(name):
            return None

    workflow = _WorkflowProxy()


@workflow.defn
class SnapshotWorkflow:
    @workflow.run
    async def run(self, job_id: str, plan: dict[str, object]) -> dict[str, object]:
        workflow.logger.info("Starting SnapshotWorkflow", job_id=job_id)
        workflow.Versioning.get_version("snapshot-workflow", default=1)

        await workflow.execute_child_workflow(
            SnapshotWorkflow,
            job_id,
            plan,
            id=f"snapshot-{job_id}",
            task_queue=workflow.info.task_queue,
        )

        return {
            "job_id": job_id,
            "status": "snapshot_started",
            "plan": plan,
        }

    @workflow.signal
    async def pause(self) -> None:
        workflow.logger.info("SnapshotWorkflow pause signal received")

    @workflow.query
    def status(self) -> str:
        return "running"


@workflow.defn
class CDCWorkflow:
    @workflow.run
    async def run(self, job_id: str, config: dict[str, object]) -> dict[str, object]:
        workflow.logger.info("Starting CDCWorkflow", job_id=job_id)
        workflow.Versioning.get_version("cdc-workflow", default=1)
        await workflow.sleep(timedelta(seconds=30))
        return {
            "job_id": job_id,
            "status": "cdc_started",
            "config": config,
        }

    @workflow.signal
    async def reconfigure(self, config: dict[str, object]) -> None:
        workflow.logger.info("CDCWorkflow reconfigure signal received", config=config)


@workflow.defn
class ValidationWorkflow:
    @workflow.run
    async def run(self, job_id: str, validation_spec: dict[str, object]) -> dict[str, object]:
        workflow.logger.info("Starting ValidationWorkflow", job_id=job_id)
        workflow.Versioning.get_version("validation-workflow", default=1)
        await workflow.sleep(timedelta(seconds=5))
        return {
            "job_id": job_id,
            "status": "validation_completed",
            "validation_spec": validation_spec,
        }


@workflow.defn
class ConflictResolutionWorkflow:
    @workflow.run
    async def run(self, job_id: str, conflicts: list[dict[str, object]]) -> dict[str, object]:
        workflow.logger.info("Starting ConflictResolutionWorkflow", job_id=job_id)
        workflow.Versioning.get_version("conflict-resolution-workflow", default=1)
        return {
            "job_id": job_id,
            "status": "conflict_resolution_completed",
            "resolved": len(conflicts),
        }


@workflow.defn
class CutoverWorkflow:
    @workflow.run
    async def run(self, job_id: str, readiness: dict[str, object]) -> dict[str, object]:
        workflow.logger.info("Starting CutoverWorkflow", job_id=job_id)
        workflow.Versioning.get_version("cutover-workflow", default=1)
        await workflow.wait_signal("approve_cutover")
        return {
            "job_id": job_id,
            "status": "cutover_approved",
            "readiness": readiness,
        }


@workflow.defn
class RecoveryWorkflow:
    @workflow.run
    async def run(self, job_id: str, recovery_spec: dict[str, object]) -> dict[str, object]:
        workflow.logger.info("Starting RecoveryWorkflow", job_id=job_id)
        workflow.Versioning.get_version("recovery-workflow", default=1)
        await workflow.sleep(timedelta(seconds=10))
        return {
            "job_id": job_id,
            "status": "recovery_completed",
            "recovery_spec": recovery_spec,
        }
