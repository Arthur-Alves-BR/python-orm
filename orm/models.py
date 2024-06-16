import psycopg

from pydantic import BaseModel
from typing import Optional, List


class Database:

    def __init__(self) -> None:
        self._connection = None

    def connect(self, database: str, user: str, password: str, host: str, port: int = 5432) -> None:
        if not self._connection:
            self._connection = psycopg.connect(
                password=password,
                dbname=database,
                user=user,
                host=host,
                port=port,
            )

    def execute(self, command: str):
        return self._connection.execute(command)


db = Database()
db.connect(database='teste_arthur', user='postgres', password='fractal', host='10.5.0.1')


class QueryBuilder:

    def __init__(self, query: Optional[str] = None) -> None:
        self._query = query

    def select(self, model: 'Model', fields: List[str]) -> str:
        return f'SELECT {",".join(fields)} FROM {model.__db_table__}'


class QuerySet:

    def __init__(self, model: 'Model') -> None:
        self.model = model

    def all(self):
        return [
            self.model.from_tuple(item)
            for item in db.execute(QueryBuilder().select(self.model, self.model.model_fields.keys())).fetchall()
        ]


class Model(BaseModel):

    __db_table__: str

    def __init_subclass__(cls, **kwargs):
        cls.objects = QuerySet(cls)
        return super().__init_subclass__(**kwargs)

    @classmethod
    def from_tuple(cls, t: tuple) -> 'Model':
        return cls(**dict(zip(cls.model_fields.keys(), t)))
