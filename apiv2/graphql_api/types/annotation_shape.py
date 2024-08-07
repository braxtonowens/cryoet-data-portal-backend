"""
GraphQL type for AnnotationShape

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/graphql_api/types/class_name.py.j2 instead.
"""

# ruff: noqa: E501 Line too long


import typing
from typing import TYPE_CHECKING, Annotated, Any, Optional, Sequence, Callable, List

import platformics.database.models as base_db
import database.models as db
import strawberry
import datetime
from platformics.graphql_api.core.query_builder import get_db_rows, get_aggregate_db_rows
from validators.annotation_shape import AnnotationShapeCreateInputValidator
from validators.annotation_shape import AnnotationShapeUpdateInputValidator
from graphql_api.helpers.annotation_shape import AnnotationShapeGroupByOptions, build_annotation_shape_groupby_output
from platformics.graphql_api.core.relay_interface import EntityInterface
from graphql_api.types.annotation_file import AnnotationFileAggregate, format_annotation_file_aggregate_output
from fastapi import Depends
from platformics.graphql_api.core.errors import PlatformicsError
from platformics.graphql_api.core.deps import get_authz_client, get_db_session, require_auth_principal, is_system_user
from platformics.graphql_api.core.query_input_types import (
    aggregator_map,
    orderBy,
    EnumComparators,
    DatetimeComparators,
    IntComparators,
    FloatComparators,
    StrComparators,
    UUIDComparators,
    BoolComparators,
)
from platformics.graphql_api.core.strawberry_extensions import DependencyExtension
from platformics.security.authorization import AuthzAction, AuthzClient, Principal
from sqlalchemy import inspect
from sqlalchemy.engine.row import RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry import relay
from strawberry.types import Info
from support.limit_offset import LimitOffsetClause
from typing_extensions import TypedDict
import enum
from support.enums import annotation_file_shape_type_enum


E = typing.TypeVar("E")
T = typing.TypeVar("T")

if TYPE_CHECKING:
    from graphql_api.types.annotation import AnnotationOrderByClause, AnnotationWhereClause, Annotation
    from graphql_api.types.annotation_file import AnnotationFileOrderByClause, AnnotationFileWhereClause, AnnotationFile

    pass
else:
    AnnotationWhereClause = "AnnotationWhereClause"
    Annotation = "Annotation"
    AnnotationOrderByClause = "AnnotationOrderByClause"
    AnnotationFileWhereClause = "AnnotationFileWhereClause"
    AnnotationFile = "AnnotationFile"
    AnnotationFileOrderByClause = "AnnotationFileOrderByClause"
    pass


"""
------------------------------------------------------------------------------
Dataloaders
------------------------------------------------------------------------------
These are batching functions for loading related objects to avoid N+1 queries.
"""


@strawberry.field
async def load_annotation_rows(
    root: "AnnotationShape",
    info: Info,
    where: Annotated["AnnotationWhereClause", strawberry.lazy("graphql_api.types.annotation")] | None = None,
    order_by: Optional[
        list[Annotated["AnnotationOrderByClause", strawberry.lazy("graphql_api.types.annotation")]]
    ] = [],
) -> Optional[Annotated["Annotation", strawberry.lazy("graphql_api.types.annotation")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.AnnotationShape)
    relationship = mapper.relationships["annotation"]
    return await dataloader.loader_for(relationship, where, order_by).load(root.annotation_id)  # type:ignore


@relay.connection(
    relay.ListConnection[
        Annotated["AnnotationFile", strawberry.lazy("graphql_api.types.annotation_file")]
    ]  # type:ignore
)
async def load_annotation_file_rows(
    root: "AnnotationShape",
    info: Info,
    where: Annotated["AnnotationFileWhereClause", strawberry.lazy("graphql_api.types.annotation_file")] | None = None,
    order_by: Optional[
        list[Annotated["AnnotationFileOrderByClause", strawberry.lazy("graphql_api.types.annotation_file")]]
    ] = [],
) -> Sequence[Annotated["AnnotationFile", strawberry.lazy("graphql_api.types.annotation_file")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.AnnotationShape)
    relationship = mapper.relationships["annotation_files"]
    return await dataloader.loader_for(relationship, where, order_by).load(root.id)  # type:ignore


@strawberry.field
async def load_annotation_file_aggregate_rows(
    root: "AnnotationShape",
    info: Info,
    where: Annotated["AnnotationFileWhereClause", strawberry.lazy("graphql_api.types.annotation_file")] | None = None,
) -> Optional[Annotated["AnnotationFileAggregate", strawberry.lazy("graphql_api.types.annotation_file")]]:
    selections = info.selected_fields[0].selections[0].selections
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.AnnotationShape)
    relationship = mapper.relationships["annotation_files"]
    rows = await dataloader.aggregate_loader_for(relationship, where, selections).load(root.id)  # type:ignore
    aggregate_output = format_annotation_file_aggregate_output(rows)
    return aggregate_output


"""
------------------------------------------------------------------------------
Define Strawberry GQL types
------------------------------------------------------------------------------
"""

"""
Only let users specify IDs in WHERE clause when mutating data (for safety).
We can extend that list as we gather more use cases from the FE team.
"""


@strawberry.input
class AnnotationShapeWhereClauseMutations(TypedDict):
    id: IntComparators | None


"""
Supported WHERE clause attributes
"""


@strawberry.input
class AnnotationShapeWhereClause(TypedDict):
    annotation: Optional[Annotated["AnnotationWhereClause", strawberry.lazy("graphql_api.types.annotation")]] | None
    annotation_files: (
        Optional[Annotated["AnnotationFileWhereClause", strawberry.lazy("graphql_api.types.annotation_file")]] | None
    )
    shape_type: Optional[EnumComparators[annotation_file_shape_type_enum]] | None
    id: Optional[IntComparators] | None


"""
Supported ORDER BY clause attributes
"""


@strawberry.input
class AnnotationShapeOrderByClause(TypedDict):
    annotation: Optional[Annotated["AnnotationOrderByClause", strawberry.lazy("graphql_api.types.annotation")]] | None
    shape_type: Optional[orderBy] | None
    id: Optional[orderBy] | None


"""
Define AnnotationShape type
"""


@strawberry.type
class AnnotationShape(EntityInterface):
    annotation: Optional[Annotated["Annotation", strawberry.lazy("graphql_api.types.annotation")]] = (
        load_annotation_rows
    )  # type:ignore
    annotation_files: Sequence[Annotated["AnnotationFile", strawberry.lazy("graphql_api.types.annotation_file")]] = (
        load_annotation_file_rows
    )  # type:ignore
    annotation_files_aggregate: Optional[
        Annotated["AnnotationFileAggregate", strawberry.lazy("graphql_api.types.annotation_file")]
    ] = load_annotation_file_aggregate_rows  # type:ignore
    shape_type: Optional[annotation_file_shape_type_enum] = None
    id: int


"""
We need to add this to each Queryable type so that strawberry will accept either our
Strawberry type *or* a SQLAlchemy model instance as a valid response class from a resolver
"""
AnnotationShape.__strawberry_definition__.is_type_of = (  # type: ignore
    lambda obj, info: type(obj) == db.AnnotationShape or type(obj) == AnnotationShape
)

"""
------------------------------------------------------------------------------
Aggregation types
------------------------------------------------------------------------------
"""
"""
Define columns that support numerical aggregations
"""


@strawberry.type
class AnnotationShapeNumericalColumns:
    id: Optional[int] = None


"""
Define columns that support min/max aggregations
"""


@strawberry.type
class AnnotationShapeMinMaxColumns:
    id: Optional[int] = None


"""
Define enum of all columns to support count and count(distinct) aggregations
"""


@strawberry.enum
class AnnotationShapeCountColumns(enum.Enum):
    annotation = "annotation"
    annotationFiles = "annotation_files"
    shapeType = "shape_type"
    id = "id"


"""
All supported aggregation functions
"""


@strawberry.type
class AnnotationShapeAggregateFunctions:
    # This is a hack to accept "distinct" and "columns" as arguments to "count"
    @strawberry.field
    def count(
        self, distinct: Optional[bool] = False, columns: Optional[AnnotationShapeCountColumns] = None
    ) -> Optional[int]:
        # Count gets set with the proper value in the resolver, so we just return it here
        return self.count  # type: ignore

    sum: Optional[AnnotationShapeNumericalColumns] = None
    avg: Optional[AnnotationShapeNumericalColumns] = None
    stddev: Optional[AnnotationShapeNumericalColumns] = None
    variance: Optional[AnnotationShapeNumericalColumns] = None
    min: Optional[AnnotationShapeMinMaxColumns] = None
    max: Optional[AnnotationShapeMinMaxColumns] = None
    groupBy: Optional[AnnotationShapeGroupByOptions] = None


"""
Wrapper around AnnotationShapeAggregateFunctions
"""


@strawberry.type
class AnnotationShapeAggregate:
    aggregate: Optional[list[AnnotationShapeAggregateFunctions]] = None


"""
------------------------------------------------------------------------------
Mutation types
------------------------------------------------------------------------------
"""


@strawberry.input()
class AnnotationShapeCreateInput:
    annotation_id: Optional[strawberry.ID] = None
    shape_type: Optional[annotation_file_shape_type_enum] = None
    id: int


@strawberry.input()
class AnnotationShapeUpdateInput:
    annotation_id: Optional[strawberry.ID] = None
    shape_type: Optional[annotation_file_shape_type_enum] = None
    id: Optional[int] = None


"""
------------------------------------------------------------------------------
Utilities
------------------------------------------------------------------------------
"""


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_annotation_shapes(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    authz_client: AuthzClient = Depends(get_authz_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[AnnotationShapeWhereClause] = None,
    order_by: Optional[list[AnnotationShapeOrderByClause]] = [],
    limit_offset: Optional[LimitOffsetClause] = None,
) -> typing.Sequence[AnnotationShape]:
    """
    Resolve AnnotationShape objects. Used for queries (see graphql_api/queries.py).
    """
    limit = limit_offset["limit"] if limit_offset and "limit" in limit_offset else None
    offset = limit_offset["offset"] if limit_offset and "offset" in limit_offset else None
    if offset and not limit:
        raise PlatformicsError("Cannot use offset without limit")
    return await get_db_rows(db.AnnotationShape, session, authz_client, principal, where, order_by, AuthzAction.VIEW, limit, offset)  # type: ignore


def format_annotation_shape_aggregate_output(
    query_results: Sequence[RowMapping] | RowMapping,
) -> AnnotationShapeAggregate:
    """
    Given a row from the DB containing the results of an aggregate query,
    format the results using the proper GraphQL types.
    """
    aggregate = []
    if not type(query_results) is list:
        query_results = [query_results]  # type: ignore
    for row in query_results:
        aggregate.append(format_annotation_shape_aggregate_row(row))
    return AnnotationShapeAggregate(aggregate=aggregate)


def format_annotation_shape_aggregate_row(row: RowMapping) -> AnnotationShapeAggregateFunctions:
    """
    Given a single row from the DB containing the results of an aggregate query,
    format the results using the proper GraphQL types.
    """
    output = AnnotationShapeAggregateFunctions()
    for key, value in row.items():
        # Key is either an aggregate function or a groupby key
        group_keys = key.split(".")
        aggregate = key.split("_", 1)
        if aggregate[0] not in aggregator_map.keys():
            # Turn list of groupby keys into nested objects
            if not getattr(output, "groupBy"):
                setattr(output, "groupBy", AnnotationShapeGroupByOptions())
            group = build_annotation_shape_groupby_output(getattr(output, "groupBy"), group_keys, value)
            setattr(output, "groupBy", group)
        else:
            aggregate_name = aggregate[0]
            if aggregate_name == "count":
                output.count = value
            else:
                aggregator_fn, col_name = aggregate[0], aggregate[1]
                if not getattr(output, aggregator_fn):
                    if aggregate_name in ["min", "max"]:
                        setattr(output, aggregator_fn, AnnotationShapeMinMaxColumns())
                    else:
                        setattr(output, aggregator_fn, AnnotationShapeNumericalColumns())
                setattr(getattr(output, aggregator_fn), col_name, value)
    return output


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_annotation_shapes_aggregate(
    info: Info,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    authz_client: AuthzClient = Depends(get_authz_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[AnnotationShapeWhereClause] = None,
    # TODO: add support for groupby, limit/offset
) -> AnnotationShapeAggregate:
    """
    Aggregate values for AnnotationShape objects. Used for queries (see graphql_api/queries.py).
    """
    # Get the selected aggregate functions and columns to operate on, and groupby options if any were provided.
    # TODO: not sure why selected_fields is a list
    selections = info.selected_fields[0].selections[0].selections
    aggregate_selections = [selection for selection in selections if getattr(selection, "name") != "groupBy"]
    groupby_selections = [selection for selection in selections if getattr(selection, "name") == "groupBy"]
    groupby_selections = groupby_selections[0].selections if groupby_selections else []

    if not aggregate_selections:
        raise PlatformicsError("No aggregate functions selected")

    rows = await get_aggregate_db_rows(db.AnnotationShape, session, authz_client, principal, where, aggregate_selections, [], groupby_selections)  # type: ignore
    aggregate_output = format_annotation_shape_aggregate_output(rows)
    return aggregate_output


@strawberry.mutation(extensions=[DependencyExtension()])
async def create_annotation_shape(
    input: AnnotationShapeCreateInput,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    authz_client: AuthzClient = Depends(get_authz_client),
    principal: Principal = Depends(require_auth_principal),
    is_system_user: bool = Depends(is_system_user),
) -> db.AnnotationShape:
    """
    Create a new AnnotationShape object. Used for mutations (see graphql_api/mutations.py).
    """
    validated = AnnotationShapeCreateInputValidator(**input.__dict__)
    params = validated.model_dump()

    # Validate that the user can read all of the entities they're linking to.

    # Validate that the user can read all of the entities they're linking to.
    # Check that annotation relationship is accessible.
    if validated.annotation_id:
        annotation = await get_db_rows(
            db.Annotation,
            session,
            authz_client,
            principal,
            {"id": {"_eq": validated.annotation_id}},
            [],
            AuthzAction.VIEW,
        )
        if not annotation:
            raise PlatformicsError("Unauthorized: annotation does not exist")

    # Save to DB
    params["owner_user_id"] = int(principal.id)
    new_entity = db.AnnotationShape(**params)

    # Are we actually allowed to create this entity?
    if not authz_client.can_create(new_entity, principal):
        raise PlatformicsError("Unauthorized: Cannot create entity")

    session.add(new_entity)
    await session.commit()
    return new_entity


@strawberry.mutation(extensions=[DependencyExtension()])
async def update_annotation_shape(
    input: AnnotationShapeUpdateInput,
    where: AnnotationShapeWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    authz_client: AuthzClient = Depends(get_authz_client),
    principal: Principal = Depends(require_auth_principal),
    is_system_user: bool = Depends(is_system_user),
) -> Sequence[db.AnnotationShape]:
    """
    Update AnnotationShape objects. Used for mutations (see graphql_api/mutations.py).
    """
    validated = AnnotationShapeUpdateInputValidator(**input.__dict__)
    params = validated.model_dump()

    # Need at least one thing to update
    num_params = len([x for x in params if params[x] is not None])
    if num_params == 0:
        raise PlatformicsError("No fields to update")

    # Validate that the user can read all of the entities they're linking to.
    # Check that annotation relationship is accessible.
    if validated.annotation_id:
        annotation = await get_db_rows(
            db.Annotation,
            session,
            authz_client,
            principal,
            {"id": {"_eq": validated.annotation_id}},
            [],
            AuthzAction.VIEW,
        )
        if not annotation:
            raise PlatformicsError("Unauthorized: annotation does not exist")
        params["annotation"] = annotation[0]
        del params["annotation_id"]

    # Fetch entities for update, if we have access to them
    entities = await get_db_rows(db.AnnotationShape, session, authz_client, principal, where, [], AuthzAction.UPDATE)
    if len(entities) == 0:
        raise PlatformicsError("Unauthorized: Cannot update entities")

    # Update DB
    updated_at = datetime.datetime.now()
    for entity in entities:
        entity.updated_at = updated_at
        for key in params:
            if params[key] is not None:
                setattr(entity, key, params[key])

    if not authz_client.can_update(entity, principal):
        raise PlatformicsError("Unauthorized: Cannot access new collection")

    await session.commit()
    return entities


@strawberry.mutation(extensions=[DependencyExtension()])
async def delete_annotation_shape(
    where: AnnotationShapeWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    authz_client: AuthzClient = Depends(get_authz_client),
    principal: Principal = Depends(require_auth_principal),
) -> Sequence[db.AnnotationShape]:
    """
    Delete AnnotationShape objects. Used for mutations (see graphql_api/mutations.py).
    """
    # Fetch entities for deletion, if we have access to them
    entities = await get_db_rows(db.AnnotationShape, session, authz_client, principal, where, [], AuthzAction.DELETE)
    if len(entities) == 0:
        raise PlatformicsError("Unauthorized: Cannot delete entities")

    # Update DB
    for entity in entities:
        await session.delete(entity)
    await session.commit()
    return entities
