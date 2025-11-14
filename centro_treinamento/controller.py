from uuid import uuid4

from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy.future import select

from atleta.models import AtletaModel
from centro_treinamento.models import CentroTreinamentoModel
from centro_treinamento.schemas import CentroTreinamentoIn, CentroTreinamentoOut
from contrib.dependencies import DatabaseDependency

router = APIRouter()


@router.post(
    "/",
    summary="Criar um novo Centro de treinamento",
    status_code=status.HTTP_201_CREATED,
    response_model=CentroTreinamentoOut,
)
async def post(
    db_session: DatabaseDependency,
    centro_treinamento_in: CentroTreinamentoIn = Body(...),
) -> CentroTreinamentoOut:

    centro_treinamento_nome = centro_treinamento_in.nome

    ct_nome = (
        (
            await db_session.execute(
                select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome)
            )
        )
        .scalars()
        .first()
    )

    if ct_nome:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f"Centro de Terinamento {centro_treinamento_nome} já existe.",
        )

    centro_treinamento_out = CentroTreinamentoOut(
        id=str(uuid4()), **centro_treinamento_in.model_dump()
    )
    centro_treinamento_model = CentroTreinamentoModel(
        **centro_treinamento_out.model_dump()
    )

    db_session.add(centro_treinamento_model)
    await db_session.commit()

    return centro_treinamento_out


@router.get(
    "/",
    summary="Consulta todos os centros de treinamento",
    status_code=status.HTTP_200_OK,
    response_model=list[CentroTreinamentoOut],
)
async def get_all(db_session: DatabaseDependency) -> list[CentroTreinamentoOut]:
    centro_treinamentos: list[CentroTreinamentoOut] = (
        (await db_session.execute(select(CentroTreinamentoModel))).scalars().all()
    )
    return centro_treinamentos


@router.get(
    "/{id}",
    summary="Consulta centro de treinamento por id",
    response_model=CentroTreinamentoOut,
)
async def get_one(id: str, db_session: DatabaseDependency) -> CentroTreinamentoOut:
    centro_treinamento: CentroTreinamentoOut = (
        (await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id)))
        .scalars()
        .first()
    )

    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ops!!! centro de treinamento com {id} não encontrado!",
        )

    return centro_treinamento
