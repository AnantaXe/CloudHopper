class DMSBulkLoadEngine:

    async def prepare(self, source, target) -> None:
        """Prepare the source and target for bulk load."""
        # Create/configure DMS replication task.
        pass

    async def start(self, source, target) -> None:
        """Start the bulk load process."""
        # Start full-load task.
        pass

    async def get_progress(self) -> float:

        return {
            "status": "running",
            "percent": 0
        }

    async def wait_until_complete(self) -> None:
        # Wait for the DMS task to complete.
        pass

    async def cancel(self) -> None:
        # Cancel the DMS task.
        pass