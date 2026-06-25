from pydantic import BaseModel
from typing import List

class WorkflowResult(BaseModel):
    workflow_id: str
    plan: List[str]
    status: str