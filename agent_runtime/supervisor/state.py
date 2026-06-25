from typing import TypedDict


class SupervisorState(TypedDict):

    provider: str

    goal: str

    plan: list[str]

    resources: list