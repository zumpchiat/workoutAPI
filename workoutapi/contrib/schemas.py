from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field


class BaseSchema(BaseModel):
    class Config:
        extra = "forbid"
        from_attributes = True


class OutMixin(BaseSchema):
    id: Annotated[str, Field(description="Identificador")]
    created_at: Annotated[datetime, Field(description="Data de criação")]
