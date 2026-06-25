from typing import TypedDict


class IntentResult(TypedDict):

    workflow: str

    provider: str


async def classify_intent(
    goal: str
):

    goal = goal.lower()

    if "aws" in goal:

        return {
            "workflow": "DISCOVERY",
            "provider": "aws"
        }

    return {
        "workflow": "UNKNOWN",
        "provider": ""
    }