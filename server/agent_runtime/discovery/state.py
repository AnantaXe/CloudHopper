from typing import TypedDict

class DiscoveryState(TypedDict):
    """
    The state of the discovery agent.
    """
    
    provider: str
    token_id: str
    plugin_validated: bool
    resources: list