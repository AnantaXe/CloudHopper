from pydantic import BaseModel, Field

class CanonicalColumn(BaseModel):
    """Canonical column model."""

    name: str
    source_type: str
    target_type: str
    normalized_type: str

class CanonicalTable(BaseModel):
    """Canonical table model."""

    name: str
    schema_name: str
    columns: list[CanonicalColumn] = Field(default_factory=list)

class CanonicalSchema(BaseModel):
    """Canonical schema model."""

    engine: str
    version: str
    tables: list[CanonicalTable] = Field(default_factory=list)