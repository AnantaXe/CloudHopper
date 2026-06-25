from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class AgentBase(ABC):
    """Base interface for autonomous sync decision agents."""

    @abstractmethod
    def reason(self, context: dict[str, Any]) -> dict[str, Any]:
        """Explain why the agent made a decision."""
        raise NotImplementedError

    @abstractmethod
    def plan(self, context: dict[str, Any]) -> dict[str, Any]:
        """Generate an execution plan based on the observed state."""
        raise NotImplementedError

    @abstractmethod
    def execute(self, plan: dict[str, Any]) -> dict[str, Any]:
        """Apply the decision plan to the underlying subsystem."""
        raise NotImplementedError

    @abstractmethod
    def evaluate(self, result: dict[str, Any]) -> dict[str, Any]:
        """Score the result and adjust future policy."""
        raise NotImplementedError
