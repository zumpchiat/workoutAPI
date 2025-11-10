from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from contrib.models import BaseModel


class AtletaModel(BaseModel):
    __tablename__ = "atletas"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    nome: Mapped[str] = mapped_column(String(50), nullable=False)
    cpf: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)
    idade: Mapped[int] = mapped_column(Integer, nullable=False)
    peso: Mapped[float] = mapped_column(Float, nullable=False)
    altura: Mapped[float] = mapped_column(Float, nullable=False)
    sexo: Mapped[str] = mapped_column(String(1), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    categoria: Mapped["CategoriaModel"] = relationship(
        back_populates="atleta", lazy="selectin"
    )
    categoria_id: Mapped[str] = mapped_column(ForeignKey("categorias.id"))

    centro_treinamento: Mapped["CentroTreinamentoModel"] = relationship(
        back_populates="atletas", lazy="selectin"
    )
    centro_treinamento_id: Mapped[str] = mapped_column(
        ForeignKey("centro_treinamento.id")
    )
