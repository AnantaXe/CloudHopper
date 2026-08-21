"""
Adapter factory for creating source/target/CDC/storage adapters
based on adapter type specified in sync job configuration.
"""

from __future__ import annotations

from typing import Any
from ..domain.models import AdapterType
from ..adapters.base import SourceAdapter, TargetAdapter, StorageAdapter, CDCAdapter
from ..adapters.aws_adapter import (
    AWSSourceAdapter,
    AWSTargetAdapter,
    AWSStorageAdapter,
    AWSCDCAdapter,
)
from ..configs.settings import SyncSettings


class AdapterFactory:
    """Factory for instantiating adapters based on adapter type."""

    def __init__(self, settings: SyncSettings):
        self.settings = settings

    def create_source_adapter(self, adapter_type: AdapterType) -> SourceAdapter:
        """Create a source adapter for the given adapter type."""
        if adapter_type == AdapterType.AWS:
            return AWSSourceAdapter()
        elif adapter_type == AdapterType.AZURE:
            # TODO: Implement AzureSourceAdapter
            raise NotImplementedError(f"Source adapter for {adapter_type} not yet implemented")
        elif adapter_type == AdapterType.GCP:
            # TODO: Implement GCPSourceAdapter
            raise NotImplementedError(f"Source adapter for {adapter_type} not yet implemented")
        elif adapter_type == AdapterType.ON_PREM:
            # TODO: Implement OnPremSourceAdapter
            raise NotImplementedError(f"Source adapter for {adapter_type} not yet implemented")
        else:
            raise ValueError(f"Unknown adapter type: {adapter_type}")

    def create_target_adapter(self, adapter_type: AdapterType) -> TargetAdapter:
        """Create a target adapter for the given adapter type."""
        if adapter_type == AdapterType.AWS:
            return AWSTargetAdapter()
        elif adapter_type == AdapterType.AZURE:
            # TODO: Implement AzureTargetAdapter
            raise NotImplementedError(f"Target adapter for {adapter_type} not yet implemented")
        elif adapter_type == AdapterType.GCP:
            # TODO: Implement GCPTargetAdapter
            raise NotImplementedError(f"Target adapter for {adapter_type} not yet implemented")
        elif adapter_type == AdapterType.ON_PREM:
            # TODO: Implement OnPremTargetAdapter
            raise NotImplementedError(f"Target adapter for {adapter_type} not yet implemented")
        else:
            raise ValueError(f"Unknown adapter type: {adapter_type}")

    def create_storage_adapter(self, adapter_type: AdapterType) -> StorageAdapter:
        """Create a storage adapter for checkpoint persistence."""
        if adapter_type == AdapterType.AWS:
            return AWSStorageAdapter()
        elif adapter_type == AdapterType.AZURE:
            # TODO: Implement AzureStorageAdapter
            raise NotImplementedError(f"Storage adapter for {adapter_type} not yet implemented")
        elif adapter_type == AdapterType.GCP:
            # TODO: Implement GCPStorageAdapter
            raise NotImplementedError(f"Storage adapter for {adapter_type} not yet implemented")
        elif adapter_type == AdapterType.ON_PREM:
            # TODO: Implement OnPremStorageAdapter
            raise NotImplementedError(f"Storage adapter for {adapter_type} not yet implemented")
        else:
            raise ValueError(f"Unknown adapter type: {adapter_type}")

    def create_cdc_adapter(self, adapter_type: AdapterType) -> CDCAdapter:
        """Create a CDC adapter for change data capture."""
        if adapter_type == AdapterType.AWS:
            return AWSCDCAdapter()
        elif adapter_type == AdapterType.AZURE:
            # TODO: Implement AzureCDCAdapter
            raise NotImplementedError(f"CDC adapter for {adapter_type} not yet implemented")
        elif adapter_type == AdapterType.GCP:
            # TODO: Implement GCPCDCAdapter
            raise NotImplementedError(f"CDC adapter for {adapter_type} not yet implemented")
        elif adapter_type == AdapterType.ON_PREM:
            # TODO: Implement OnPremCDCAdapter
            raise NotImplementedError(f"CDC adapter for {adapter_type} not yet implemented")
        else:
            raise ValueError(f"Unknown adapter type: {adapter_type}")

    def create_adapters(
        self,
        source_type: AdapterType,
        target_type: AdapterType,
    ) -> tuple[SourceAdapter, TargetAdapter, StorageAdapter, CDCAdapter]:
        """Create all adapters for a sync job."""
        source = self.create_source_adapter(source_type)
        target = self.create_target_adapter(target_type)
        storage = self.create_storage_adapter(source_type)  # Use source type for storage
        cdc = self.create_cdc_adapter(source_type)  # Use source type for CDC

        return source, target, storage, cdc
