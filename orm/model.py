from pydantic import BaseModel
from typing import Optional, Iterable, Dict, List

from orm import db


class Model(BaseModel):

    __db_table__: str

    def __init_subclass__(cls, **kwargs) -> None:
        cls.objects: 'QuerySet' = QuerySet(cls)
        return super().__init_subclass__(**kwargs)

    @property
    def objects(self) -> 'QuerySet':
        return self.objects

    @classmethod
    def from_tuple(cls, t: tuple) -> 'Model':
        return cls(**dict(zip(cls.model_fields.keys(), t)))


class QueryBuilder:

    def __init__(self, model: Model, query: Optional[str] = None) -> None:
        self._query = query
        self._model = model

    def select(self, fields: List[str]) -> str:
        return f'SELECT {self._iterable_to_string(fields)} FROM {self._model.__db_table__};'

    def insert(self, kwargs: Dict) -> str:
        fields = self._iterable_to_string(kwargs.keys())
        values = self._iterable_to_string(self._process_values(kwargs.values()))
        return f'INSERT INTO {self._model.__db_table__} ({fields}) VALUES ({values}) RETURNING *;'

    def _process_values(self, values: Iterable) -> List:
        return [f"'{v}'" if isinstance(v, str) else v for v in values]

    def _iterable_to_string(self, iterable: Iterable) -> str:
        return ', '.join(str(x) for x in iterable)


class QuerySet:

    def __init__(self, model: Model) -> None:
        self._query_builder = QueryBuilder(model)
        self.model = model

    def all(self) -> List[Model]:
        return [
            self.model.from_tuple(item)
            for item in db.execute(self._query_builder.select(self.model.model_fields.keys())).fetchall()
        ]

    def create(self, **kwargs: Dict) -> Model:
        return self.model.from_tuple(db.execute(self._query_builder.insert(kwargs)).fetchone())
