# Projeto

## WorkoutAPI

Projeto de API para competição de crossfit chamada WorkoutAPI.

![alt text](image-1.png)

## Modelagem de entidade e relacionamento - MER

![alt text](image.png)

## Stack da API

- FastAPI
- MySQL
- Docker

## API

Para subir a API, execute:

- Renomei env.local para .env
- Edite o arquivo com as informações do seu banco de dados

```bash
#cd workoutapi
#alembic upgrade head
#fastapi dev main.py
```

e acesse: http://127.0.0.1:8000/docs

# Referências

FastAPI: https://fastapi.tiangolo.com/

Pydantic: https://docs.pydantic.dev/latest/

SQLAlchemy: https://docs.sqlalchemy.org/en/20/

Alembic: https://alembic.sqlalchemy.org/en/latest/

Fastapi-pagination: https://uriyyo-fastapi-pagination.netlify.app/

python-decouple https://pypi.org/project/python-decouple/
