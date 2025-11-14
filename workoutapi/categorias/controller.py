from uuid import uuid4

from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy.future import select

from workoutapi.atleta.models import AtletaModel
from workoutapi.categorias.models import CategoriaModel
from workoutapi.categorias.schemas import CategoriaIn, CategoriaOut
from workoutapi.contrib.dependencies import DatabaseDependency

router = APIRouter()


@router.post(
    "/",
    summary="Cria uma Categoria",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoriaOut,
)
async def create_category(
    db_session: DatabaseDependency, categoria_in: CategoriaIn = Body(...)
) -> CategoriaOut:
    categoria_out = CategoriaOut(id=str(uuid4()), **categoria_in.model_dump())
    categoria_model = CategoriaModel(**categoria_out.model_dump())
    categoria_nome = categoria_in.nome

    cat_nome = (
        (
            await db_session.execute(
                select(CategoriaModel).filter_by(nome=categoria_nome)
            )
        )
        .scalars()
        .first()
    )

    if cat_nome:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f"A categoria {categoria_nome} já existe!",
        )

    db_session.add(categoria_model)
    await db_session.commit()

    return categoria_out


@router.get(
    "/",
    summary="Consulta todas as categorias",
    status_code=status.HTTP_200_OK,
    response_model=list[CategoriaOut],
)
async def get_all(db_session: DatabaseDependency) -> list[CategoriaOut]:
    categorias: list[CategoriaOut] = (
        (await db_session.execute(select(CategoriaModel))).scalars().all()
    )

    return categorias


@router.get(
    "/{id}",
    summary="Consulta uma Categoria pelo id",
    status_code=status.HTTP_200_OK,
    response_model=CategoriaOut,
)
async def get_one(id: str, db_session: DatabaseDependency) -> CategoriaOut:
    categoria: CategoriaOut = (
        (await db_session.execute(select(CategoriaModel).filter_by(id=id)))
        .scalars()
        .first()
    )

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoria não encontrada no id: {id}",
        )

    return categoria
