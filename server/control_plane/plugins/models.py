from pydantic import BaseModel

class PluginMetadata(BaseModel):

    name: str

    version: str

    signatures: str

    permissions: list[str]

    sandboxed: bool