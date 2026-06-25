from pydantic import BaseModel


class AgentEvent(BaseModel):

    agent: str

    event_type: str

    message: str