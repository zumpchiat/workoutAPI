from typing import Annotated, Optional

from pydantic import UUID4, Field

from contrib.schemas import BaseSchema


class CategoriaIn(BaseSchema):
    nome: Annotated[
        str, Field(description="Nome da categoria", example="Scale", max_length=10)
    ]


class CategoriaOut(CategoriaIn):
    id: Annotated[str, Field(description="Identificador da categoria")]
