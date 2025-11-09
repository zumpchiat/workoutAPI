from typing import Annotated

from pydantic import Field

from contrib.schemas import BaseSchema


class CentroTreinamento(BaseSchema):
    nome: Annotated[
        str, Field(description="Nome do CT", examples="Team FTEM", max_length=20)
    ]
    endereco: Annotated[
        str, Field(description="Endereço", examples="Rua XPTO, 88", max_length=60)
    ]
    proprietario: Annotated[
        str, Field(description="Proprietário", examples="João Silva", max_length=30)
    ]
