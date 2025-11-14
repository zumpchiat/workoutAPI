from datetime import datetime
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy.future import select

from atleta.models import AtletaModel
from atleta.schemas import AtletaBasic, AtletaIn, AtletaOut, AtletaUpdate
from categorias.models import CategoriaModel
from centro_treinamento.models import CentroTreinamentoModel
from contrib.dependencies import DatabaseDependency

router = APIRouter()


@router.post(
    "/",
    summary="Cria um atleta",
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut,
)
async def create_atleta(
    db_session: DatabaseDependency, atleta_in: AtletaIn = Body(...)
) -> AtletaOut:
    categoria_nome = atleta_in.categoria.nome
    atleta_cpf = atleta_in.cpf
    centro_treinamento_nome = atleta_in.centro_treinamento.nome

    categoria = (
        (
            await db_session.execute(
                select(CategoriaModel).filter_by(nome=categoria_nome)
            )
        )
        .scalars()
        .first()
    )

    atleta = (
        (await db_session.execute(select(AtletaModel).filter_by(cpf=atleta_cpf)))
        .scalars()
        .first()
    )

    if atleta:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f"Já existe um atleta cadastrado com o cpf: {atleta_cpf}",
        )

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ops!! A categoria não existe!!",
        )

    centro_treinamento = (
        (
            await db_session.execute(
                select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome)
            )
        )
        .scalars()
        .first()
    )

    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ops!! O centro de treinamento não existe!!",
        )

    try:
        atleta_out = AtletaOut(
            id=str(uuid4()), created_at=datetime.now(), **atleta_in.model_dump()
        )

        atleta_model = AtletaModel(
            **atleta_out.model_dump(exclude=["categoria", "centro_treinamento"])
        )
        atleta_model.categoria_id = categoria.id
        atleta_model.centro_treinamento_id = centro_treinamento.id

        db_session.add(atleta_model)
        await db_session.commit()

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao salvar Atleta",
        )

    return atleta_out


@router.get(
    "/",
    summary="Consulta todos os Atletas ou Filtra por nome ou cpf",
    status_code=status.HTTP_200_OK,
    response_model=list[AtletaBasic],
)
async def get_all(
    db_session: DatabaseDependency,
    nome: Optional[str] = None,
    cpf: Optional[str] = None,
) -> list[AtletaBasic]:

    query = select(AtletaModel)

    if nome:
        query = query.filter(AtletaModel.nome.ilike(f"%{nome}%"))

    if cpf:
        query = query.filter(AtletaModel.cpf == cpf)

    if (nome) and (cpf):
        query = query.filter(AtletaModel.cpf == cpf)

    atletas: list[AtletaModel] = (await db_session.execute(query)).scalars().all()

    if not atletas:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail="OPS!!! Atleta não encontrado!",
        )

    return atletas


@router.get(
    "/{id}",
    summary="Consulta Atleta por id ",
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def get_one(id: str, db_session: DatabaseDependency) -> AtletaOut:

    atleta: AtletaOut = (
        (await db_session.execute(select(AtletaModel).filter_by(id=id)))
        .scalars()
        .first()
    )

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ops!!! Atleta {id} não encontrado!",
        )

    return atleta


@router.patch(
    "/{id}",
    summary="Atualiza dados do Atleta",
    status_code=status.HTTP_200_OK,
    response_model=AtletaUpdate,
)
async def update(
    id: str, db_session: DatabaseDependency, atleta_up: AtletaUpdate = Body(...)
) -> AtletaUpdate:
    atleta: AtletaUpdate = (
        (await db_session.execute(select(AtletaModel).filter_by(id=id)))
        .scalars()
        .first()
    )

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ops!! Atleta {id} não existe",
        )

    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
        setattr(atleta, key, value)

    await db_session.commit()
    await db_session.refresh(atleta)

    return AtletaUpdate.model_validate(atleta)


@router.delete("/{id}", summary="Remove Atleta", status_code=status.HTTP_204_NO_CONTENT)
async def remove(id: str, db_session: DatabaseDependency) -> None:
    atleta: AtletaIn = (
        (await db_session.execute(select(AtletaModel).filter_by(id=id)))
        .scalars()
        .first()
    )

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Atleta não existe com id {id}",
        )

    await db_session.delete(atleta)
    await db_session.commit()
