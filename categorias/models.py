from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from contrib.models import BaseModel


class CategoriaModel(BaseModel):
    __tablename__ = "categorias"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    nome: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    atleta: Mapped["AtletaModel"] = relationship(back_populates="categoria")
