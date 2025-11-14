from typing import Annotated

from pydantic import Field

from workoutapi.contrib.schemas import BaseSchema


class CentroTreinamento(BaseSchema):
    nome: Annotated[
        str, Field(description="Nome do CT", examples="Team FTEM", max_length=20)
    ]
