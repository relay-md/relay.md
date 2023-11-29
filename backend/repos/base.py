# -*- coding: utf-8 -*-
import abc
from typing import List, TypeVar, Union
from uuid import UUID

from sqlalchemy import select

from ..database import Session

# Type of the underlying ORM model
T = TypeVar("T")

# Type of the
M = TypeVar("M")


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, **kwargs) -> T:
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_id(self, id: UUID) -> T:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self, key: str, value: T) -> List[T]:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, item: M) -> T:
        raise NotImplementedError


class DatabaseAbstractRepository(AbstractRepository):
    ORM_Model: T

    def __init__(self, db: Session):
        self._db = db

    def create(self, item: T) -> T:
        self._db.add(item)
        self._db.commit()
        self._db.refresh(item)
        return item

    def create_from_kwargs(self, **kwargs) -> T:
        new = self.ORM_Model(**kwargs)
        self._db.add(new)
        self._db.commit()
        self._db.refresh(new)
        return new

    def get_by_id(self, id: Union[UUID, str]) -> T:
        if isinstance(id, str):
            return self._db.get(self.ORM_Model, UUID(id))
        return self._db.get(self.ORM_Model, id)

    def get_by_kwargs(self, **kwargs) -> T:
        return self._db.scalar(select(self.ORM_Model).filter_by(**kwargs))

    def list(self, key: str, value: T) -> List[T]:
        return self._db.scalars(select(self.ORM_Model).filter_by(**{key: value}))

    def update(self, item: T, **kwargs) -> T:
        raise NotImplementedError

    def delete_by_id(self, item: T) -> None:
        self._db.delete(item)
        self._db.commit()
