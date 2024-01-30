# -*- coding: utf-8 -*-
import logging
from typing import Generic, Optional, TypeVar, Union
from uuid import UUID

from sqlalchemy import ScalarResult, func, select
from sqlalchemy.exc import IntegrityError

from ..database import Session

log = logging.getLogger(__name__)

# Type of the underlying ORM model
T = TypeVar("T")

# Type of the
M = TypeVar("M")


class DatabaseAbstractRepository(Generic[T]):
    ORM_Model: T

    def __traceback(self):
        import traceback

        log.error(traceback.format_exc())

    def __init__(self, db: Session):
        self._db = db

    def create(self, item: T) -> T:
        try:
            self._db.add(item)
            self._db.commit()
        except IntegrityError:
            self.__traceback()
            raise Exception(
                "Database complained. Probably a uniqueness constraint is violated by your request!"
            )
        self._db.refresh(item)
        return item

    def create_from_kwargs(self, **kwargs) -> object:
        new = self.ORM_Model(**kwargs)  # type: ignore
        try:
            self._db.add(new)
            self._db.commit()
        except IntegrityError:
            self.__traceback()
            raise Exception(
                "Database complained. Probably a uniqueness constraint is violated by your request!"
            )
        self._db.refresh(new)
        return new

    def get_by_id(self, id: Union[UUID, str]) -> Optional[T]:
        if isinstance(id, str):
            return self._db.get(self.ORM_Model, UUID(id))
        return self._db.get(self.ORM_Model, id)

    def get_by_kwargs(self, **kwargs) -> T:
        return self._db.scalar(select(self.ORM_Model).filter_by(**kwargs))

    def list(self, **kwargs) -> ScalarResult[T]:
        return self._db.scalars(select(self.ORM_Model).filter_by(**kwargs))

    def filter(self, *args) -> ScalarResult[T]:
        return self._db.scalars(select(self.ORM_Model).filter(*args))

    def update(self, item: T, **kwargs) -> T:
        for key, value in kwargs.items():
            if not hasattr(item, key):
                raise ValueError(
                    f"Item of type {item.__class__.__name__} has no attribute {key}"
                )
            setattr(item, key, value)
        try:
            self._db.commit()
        except IntegrityError:
            self.__traceback()
            raise Exception(
                "Database complained. Probably a uniqueness constraint is violated by your request!"
            )
        return item

    def delete(self, item: T) -> None:
        if not item:
            return
        try:
            self._db.delete(item)
            self._db.commit()
        except IntegrityError:
            self.__traceback()
            raise Exception(
                "Database complained. Probably a uniqueness constraint is violated by your request!"
            )

    def count(self, **kwargs):
        return self._db.scalar(
            select(func.count(self.ORM_Model.id)).filter_by(**kwargs)
        )
