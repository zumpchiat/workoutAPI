from typing import List

from sqlalchemy import UUID, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from contrib.models import BaseModel


class CentroTreinamentoModel(BaseModel):
    __tablename__ = "centro_treinamento"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)

    nome: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)

    endereco: Mapped[str] = mapped_column(String(60), nullable=False)
    proprietario: Mapped[str] = mapped_column(String(30), nullable=False)

    atleta: Mapped[List["AtletaModel"]] = relationship(
        back_populates="centro_treinamento"
    )
