from typing import Any, Tuple, Type, TypeVar
from fastapi import HTTPException, status
from psycopg2.errors import ForeignKeyViolation  # type: ignore
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import Query, Session
from sqlalchemy.sql.functions import coalesce

SqlAlchemyModel = TypeVar("SqlAlchemyModel")


def create(session: Session, model: SqlAlchemyModel) -> SqlAlchemyModel:
    try:
        session.add(model)
        session.flush()
    except IntegrityError as e:
        handle_db_error(session, model, e)  # type: ignore

    return model


def get_all(
    session: Session,
    model: Type[SqlAlchemyModel],
    page: int,
    page_size: int,
    filters: list,
) -> Tuple[list[SqlAlchemyModel], int]:
    query: Query = session.query(model)

    if hasattr(model, "updated_at"):
        query = query.order_by(desc(coalesce(model.updated_at, model.created_at)))  # type: ignore
    elif hasattr(model, "created_at"):
        query = query.order_by(desc(model.created_at))  # type: ignore

    query = query.filter(*filters)

    total = query.count()
    query = query.offset((page - 1) * page_size)
    query = query.limit(page_size)

    return query.all(), total


def get_by_attribute(
    session: Session,
    model: Type[SqlAlchemyModel],
    attribute_name: str,
    attribute_value: Any,
    *,
    filters: list = [],
) -> SqlAlchemyModel:
    entity = (
        session.query(model)  # type: ignore # CrudModel must be a SQLAlchemy model
        .filter(getattr(model, attribute_name) == attribute_value, *filters)
        .first()
    )
    if entity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model.__tablename__[:-1]} not found".capitalize(),  # type: ignore
        )

    return entity


def update(session: Session, model: Type[SqlAlchemyModel], id: str, **kwargs) -> None:
    try:
        entity_update_status = (
            session.query(model).filter(getattr(model, "id") == id).update(kwargs)  # type: ignore
        )

        if entity_update_status == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{model.__tablename__[:-1]} not found".capitalize(),  # type: ignore
            )
    except IntegrityError as e:
        handle_db_error(session, model, e)  # type: ignore


def delete(session: Session, model: Type[SqlAlchemyModel], id: int) -> None:
    entity = get_by_attribute(session, model, "id", id)
    session.delete(entity)


def handle_db_error(
    session: Session, model: Type[SqlAlchemyModel], exception: Exception
) -> None:
    session.rollback()

    if isinstance(exception, ForeignKeyViolation):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Related resource(s) not found",
        )

    if isinstance(exception, OperationalError):
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail="Database connection timeout.",
        )

    if isinstance(exception, IntegrityError):
        unique_attrs = [
            column.name
            for column in model.__table__.columns  # type: ignore
            if column.unique
        ]
        violated_unique_attrs = []
        for attr in unique_attrs:
            if (
                session.query(model.__class__)  # type: ignore
                .filter(getattr(model.__class__, attr) == getattr(model, attr))
                .first()
                is not None
            ):
                violated_unique_attrs.append(attr)

        if violated_unique_attrs:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"{model.__tablename__[:-1]} already exists with these values: {', '.join(violated_unique_attrs)}".capitalize(),  # type: ignore
            )

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="An unknown database error occurred.",
    )
