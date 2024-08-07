"""
GraphQL type for DepositionAuthor

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
from validators.deposition_author import DepositionAuthorCreateInputValidator
from validators.deposition_author import DepositionAuthorUpdateInputValidator
from graphql_api.helpers.deposition_author import DepositionAuthorGroupByOptions, build_deposition_author_groupby_output
from platformics.graphql_api.core.relay_interface import EntityInterface
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


E = typing.TypeVar("E")
T = typing.TypeVar("T")

if TYPE_CHECKING:
    from graphql_api.types.deposition import DepositionOrderByClause, DepositionWhereClause, Deposition

    pass
else:
    DepositionWhereClause = "DepositionWhereClause"
    Deposition = "Deposition"
    DepositionOrderByClause = "DepositionOrderByClause"
    pass


"""
------------------------------------------------------------------------------
Dataloaders
------------------------------------------------------------------------------
These are batching functions for loading related objects to avoid N+1 queries.
"""


@strawberry.field
async def load_deposition_rows(
    root: "DepositionAuthor",
    info: Info,
    where: Annotated["DepositionWhereClause", strawberry.lazy("graphql_api.types.deposition")] | None = None,
    order_by: Optional[
        list[Annotated["DepositionOrderByClause", strawberry.lazy("graphql_api.types.deposition")]]
    ] = [],
) -> Optional[Annotated["Deposition", strawberry.lazy("graphql_api.types.deposition")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.DepositionAuthor)
    relationship = mapper.relationships["deposition"]
    return await dataloader.loader_for(relationship, where, order_by).load(root.deposition_id)  # type:ignore


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
class DepositionAuthorWhereClauseMutations(TypedDict):
    id: IntComparators | None


"""
Supported WHERE clause attributes
"""


@strawberry.input
class DepositionAuthorWhereClause(TypedDict):
    deposition: Optional[Annotated["DepositionWhereClause", strawberry.lazy("graphql_api.types.deposition")]] | None
    author_list_order: Optional[IntComparators] | None
    orcid: Optional[StrComparators] | None
    name: Optional[StrComparators] | None
    email: Optional[StrComparators] | None
    affiliation_name: Optional[StrComparators] | None
    affiliation_address: Optional[StrComparators] | None
    affiliation_identifier: Optional[StrComparators] | None
    corresponding_author_status: Optional[BoolComparators] | None
    primary_author_status: Optional[BoolComparators] | None
    id: Optional[IntComparators] | None


"""
Supported ORDER BY clause attributes
"""


@strawberry.input
class DepositionAuthorOrderByClause(TypedDict):
    deposition: Optional[Annotated["DepositionOrderByClause", strawberry.lazy("graphql_api.types.deposition")]] | None
    author_list_order: Optional[orderBy] | None
    orcid: Optional[orderBy] | None
    name: Optional[orderBy] | None
    email: Optional[orderBy] | None
    affiliation_name: Optional[orderBy] | None
    affiliation_address: Optional[orderBy] | None
    affiliation_identifier: Optional[orderBy] | None
    corresponding_author_status: Optional[orderBy] | None
    primary_author_status: Optional[orderBy] | None
    id: Optional[orderBy] | None


"""
Define DepositionAuthor type
"""


@strawberry.type
class DepositionAuthor(EntityInterface):
    deposition: Optional[Annotated["Deposition", strawberry.lazy("graphql_api.types.deposition")]] = (
        load_deposition_rows
    )  # type:ignore
    author_list_order: int
    orcid: Optional[str] = None
    name: str
    email: Optional[str] = None
    affiliation_name: Optional[str] = None
    affiliation_address: Optional[str] = None
    affiliation_identifier: Optional[str] = None
    corresponding_author_status: Optional[bool] = None
    primary_author_status: Optional[bool] = None
    id: int


"""
We need to add this to each Queryable type so that strawberry will accept either our
Strawberry type *or* a SQLAlchemy model instance as a valid response class from a resolver
"""
DepositionAuthor.__strawberry_definition__.is_type_of = (  # type: ignore
    lambda obj, info: type(obj) == db.DepositionAuthor or type(obj) == DepositionAuthor
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
class DepositionAuthorNumericalColumns:
    author_list_order: Optional[int] = None
    id: Optional[int] = None


"""
Define columns that support min/max aggregations
"""


@strawberry.type
class DepositionAuthorMinMaxColumns:
    author_list_order: Optional[int] = None
    orcid: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    affiliation_name: Optional[str] = None
    affiliation_address: Optional[str] = None
    affiliation_identifier: Optional[str] = None
    id: Optional[int] = None


"""
Define enum of all columns to support count and count(distinct) aggregations
"""


@strawberry.enum
class DepositionAuthorCountColumns(enum.Enum):
    deposition = "deposition"
    authorListOrder = "author_list_order"
    orcid = "orcid"
    name = "name"
    email = "email"
    affiliationName = "affiliation_name"
    affiliationAddress = "affiliation_address"
    affiliationIdentifier = "affiliation_identifier"
    correspondingAuthorStatus = "corresponding_author_status"
    primaryAuthorStatus = "primary_author_status"
    id = "id"


"""
All supported aggregation functions
"""


@strawberry.type
class DepositionAuthorAggregateFunctions:
    # This is a hack to accept "distinct" and "columns" as arguments to "count"
    @strawberry.field
    def count(
        self, distinct: Optional[bool] = False, columns: Optional[DepositionAuthorCountColumns] = None
    ) -> Optional[int]:
        # Count gets set with the proper value in the resolver, so we just return it here
        return self.count  # type: ignore

    sum: Optional[DepositionAuthorNumericalColumns] = None
    avg: Optional[DepositionAuthorNumericalColumns] = None
    stddev: Optional[DepositionAuthorNumericalColumns] = None
    variance: Optional[DepositionAuthorNumericalColumns] = None
    min: Optional[DepositionAuthorMinMaxColumns] = None
    max: Optional[DepositionAuthorMinMaxColumns] = None
    groupBy: Optional[DepositionAuthorGroupByOptions] = None


"""
Wrapper around DepositionAuthorAggregateFunctions
"""


@strawberry.type
class DepositionAuthorAggregate:
    aggregate: Optional[list[DepositionAuthorAggregateFunctions]] = None


"""
------------------------------------------------------------------------------
Mutation types
------------------------------------------------------------------------------
"""


@strawberry.input()
class DepositionAuthorCreateInput:
    deposition_id: Optional[strawberry.ID] = None
    author_list_order: int
    orcid: Optional[str] = None
    name: str
    email: Optional[str] = None
    affiliation_name: Optional[str] = None
    affiliation_address: Optional[str] = None
    affiliation_identifier: Optional[str] = None
    corresponding_author_status: Optional[bool] = None
    primary_author_status: Optional[bool] = None
    id: int


@strawberry.input()
class DepositionAuthorUpdateInput:
    deposition_id: Optional[strawberry.ID] = None
    author_list_order: Optional[int] = None
    orcid: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    affiliation_name: Optional[str] = None
    affiliation_address: Optional[str] = None
    affiliation_identifier: Optional[str] = None
    corresponding_author_status: Optional[bool] = None
    primary_author_status: Optional[bool] = None
    id: Optional[int] = None


"""
------------------------------------------------------------------------------
Utilities
------------------------------------------------------------------------------
"""


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_deposition_authors(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    authz_client: AuthzClient = Depends(get_authz_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[DepositionAuthorWhereClause] = None,
    order_by: Optional[list[DepositionAuthorOrderByClause]] = [],
    limit_offset: Optional[LimitOffsetClause] = None,
) -> typing.Sequence[DepositionAuthor]:
    """
    Resolve DepositionAuthor objects. Used for queries (see graphql_api/queries.py).
    """
    limit = limit_offset["limit"] if limit_offset and "limit" in limit_offset else None
    offset = limit_offset["offset"] if limit_offset and "offset" in limit_offset else None
    if offset and not limit:
        raise PlatformicsError("Cannot use offset without limit")
    return await get_db_rows(db.DepositionAuthor, session, authz_client, principal, where, order_by, AuthzAction.VIEW, limit, offset)  # type: ignore


def format_deposition_author_aggregate_output(
    query_results: Sequence[RowMapping] | RowMapping,
) -> DepositionAuthorAggregate:
    """
    Given a row from the DB containing the results of an aggregate query,
    format the results using the proper GraphQL types.
    """
    aggregate = []
    if not type(query_results) is list:
        query_results = [query_results]  # type: ignore
    for row in query_results:
        aggregate.append(format_deposition_author_aggregate_row(row))
    return DepositionAuthorAggregate(aggregate=aggregate)


def format_deposition_author_aggregate_row(row: RowMapping) -> DepositionAuthorAggregateFunctions:
    """
    Given a single row from the DB containing the results of an aggregate query,
    format the results using the proper GraphQL types.
    """
    output = DepositionAuthorAggregateFunctions()
    for key, value in row.items():
        # Key is either an aggregate function or a groupby key
        group_keys = key.split(".")
        aggregate = key.split("_", 1)
        if aggregate[0] not in aggregator_map.keys():
            # Turn list of groupby keys into nested objects
            if not getattr(output, "groupBy"):
                setattr(output, "groupBy", DepositionAuthorGroupByOptions())
            group = build_deposition_author_groupby_output(getattr(output, "groupBy"), group_keys, value)
            setattr(output, "groupBy", group)
        else:
            aggregate_name = aggregate[0]
            if aggregate_name == "count":
                output.count = value
            else:
                aggregator_fn, col_name = aggregate[0], aggregate[1]
                if not getattr(output, aggregator_fn):
                    if aggregate_name in ["min", "max"]:
                        setattr(output, aggregator_fn, DepositionAuthorMinMaxColumns())
                    else:
                        setattr(output, aggregator_fn, DepositionAuthorNumericalColumns())
                setattr(getattr(output, aggregator_fn), col_name, value)
    return output


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_deposition_authors_aggregate(
    info: Info,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    authz_client: AuthzClient = Depends(get_authz_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[DepositionAuthorWhereClause] = None,
    # TODO: add support for groupby, limit/offset
) -> DepositionAuthorAggregate:
    """
    Aggregate values for DepositionAuthor objects. Used for queries (see graphql_api/queries.py).
    """
    # Get the selected aggregate functions and columns to operate on, and groupby options if any were provided.
    # TODO: not sure why selected_fields is a list
    selections = info.selected_fields[0].selections[0].selections
    aggregate_selections = [selection for selection in selections if getattr(selection, "name") != "groupBy"]
    groupby_selections = [selection for selection in selections if getattr(selection, "name") == "groupBy"]
    groupby_selections = groupby_selections[0].selections if groupby_selections else []

    if not aggregate_selections:
        raise PlatformicsError("No aggregate functions selected")

    rows = await get_aggregate_db_rows(db.DepositionAuthor, session, authz_client, principal, where, aggregate_selections, [], groupby_selections)  # type: ignore
    aggregate_output = format_deposition_author_aggregate_output(rows)
    return aggregate_output


@strawberry.mutation(extensions=[DependencyExtension()])
async def create_deposition_author(
    input: DepositionAuthorCreateInput,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    authz_client: AuthzClient = Depends(get_authz_client),
    principal: Principal = Depends(require_auth_principal),
    is_system_user: bool = Depends(is_system_user),
) -> db.DepositionAuthor:
    """
    Create a new DepositionAuthor object. Used for mutations (see graphql_api/mutations.py).
    """
    validated = DepositionAuthorCreateInputValidator(**input.__dict__)
    params = validated.model_dump()

    # Validate that the user can read all of the entities they're linking to.

    # Validate that the user can read all of the entities they're linking to.
    # Check that deposition relationship is accessible.
    if validated.deposition_id:
        deposition = await get_db_rows(
            db.Deposition,
            session,
            authz_client,
            principal,
            {"id": {"_eq": validated.deposition_id}},
            [],
            AuthzAction.VIEW,
        )
        if not deposition:
            raise PlatformicsError("Unauthorized: deposition does not exist")

    # Save to DB
    params["owner_user_id"] = int(principal.id)
    new_entity = db.DepositionAuthor(**params)

    # Are we actually allowed to create this entity?
    if not authz_client.can_create(new_entity, principal):
        raise PlatformicsError("Unauthorized: Cannot create entity")

    session.add(new_entity)
    await session.commit()
    return new_entity


@strawberry.mutation(extensions=[DependencyExtension()])
async def update_deposition_author(
    input: DepositionAuthorUpdateInput,
    where: DepositionAuthorWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    authz_client: AuthzClient = Depends(get_authz_client),
    principal: Principal = Depends(require_auth_principal),
    is_system_user: bool = Depends(is_system_user),
) -> Sequence[db.DepositionAuthor]:
    """
    Update DepositionAuthor objects. Used for mutations (see graphql_api/mutations.py).
    """
    validated = DepositionAuthorUpdateInputValidator(**input.__dict__)
    params = validated.model_dump()

    # Need at least one thing to update
    num_params = len([x for x in params if params[x] is not None])
    if num_params == 0:
        raise PlatformicsError("No fields to update")

    # Validate that the user can read all of the entities they're linking to.
    # Check that deposition relationship is accessible.
    if validated.deposition_id:
        deposition = await get_db_rows(
            db.Deposition,
            session,
            authz_client,
            principal,
            {"id": {"_eq": validated.deposition_id}},
            [],
            AuthzAction.VIEW,
        )
        if not deposition:
            raise PlatformicsError("Unauthorized: deposition does not exist")
        params["deposition"] = deposition[0]
        del params["deposition_id"]

    # Fetch entities for update, if we have access to them
    entities = await get_db_rows(db.DepositionAuthor, session, authz_client, principal, where, [], AuthzAction.UPDATE)
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
async def delete_deposition_author(
    where: DepositionAuthorWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    authz_client: AuthzClient = Depends(get_authz_client),
    principal: Principal = Depends(require_auth_principal),
) -> Sequence[db.DepositionAuthor]:
    """
    Delete DepositionAuthor objects. Used for mutations (see graphql_api/mutations.py).
    """
    # Fetch entities for deletion, if we have access to them
    entities = await get_db_rows(db.DepositionAuthor, session, authz_client, principal, where, [], AuthzAction.DELETE)
    if len(entities) == 0:
        raise PlatformicsError("Unauthorized: Cannot delete entities")

    # Update DB
    for entity in entities:
        await session.delete(entity)
    await session.commit()
    return entities
