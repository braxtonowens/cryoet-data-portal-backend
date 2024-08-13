"""
GraphQL type for PerSectionAlignmentParameters

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/graphql_api/types/class_name.py.j2 instead.
"""

# ruff: noqa: E501 Line too long


import datetime
import enum
import typing
from typing import TYPE_CHECKING, Annotated, Optional, Sequence

import database.models as db
import strawberry
from fastapi import Depends
from graphql_api.helpers.per_section_alignment_parameters import (
    PerSectionAlignmentParametersGroupByOptions,
    build_per_section_alignment_parameters_groupby_output,
)
from platformics.graphql_api.core.deps import get_authz_client, get_db_session, is_system_user, require_auth_principal
from platformics.graphql_api.core.errors import PlatformicsError
from platformics.graphql_api.core.query_builder import get_aggregate_db_rows, get_db_rows
from platformics.graphql_api.core.query_input_types import (
    FloatComparators,
    IntComparators,
    aggregator_map,
    orderBy,
)
from platformics.graphql_api.core.relay_interface import EntityInterface
from platformics.graphql_api.core.strawberry_extensions import DependencyExtension
from platformics.security.authorization import AuthzAction, AuthzClient, Principal
from sqlalchemy import inspect
from sqlalchemy.engine.row import RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.types import Info
from support.limit_offset import LimitOffsetClause
from typing_extensions import TypedDict
from validators.per_section_alignment_parameters import (
    PerSectionAlignmentParametersCreateInputValidator,
    PerSectionAlignmentParametersUpdateInputValidator,
)

E = typing.TypeVar("E")
T = typing.TypeVar("T")

if TYPE_CHECKING:
    from graphql_api.types.alignment import Alignment, AlignmentOrderByClause, AlignmentWhereClause

    pass
else:
    AlignmentWhereClause = "AlignmentWhereClause"
    Alignment = "Alignment"
    AlignmentOrderByClause = "AlignmentOrderByClause"
    pass


"""
------------------------------------------------------------------------------
Dataloaders
------------------------------------------------------------------------------
These are batching functions for loading related objects to avoid N+1 queries.
"""


@strawberry.field
async def load_alignment_rows(
    root: "PerSectionAlignmentParameters",
    info: Info,
    where: Annotated["AlignmentWhereClause", strawberry.lazy("graphql_api.types.alignment")] | None = None,
    order_by: Optional[list[Annotated["AlignmentOrderByClause", strawberry.lazy("graphql_api.types.alignment")]]] = [],
) -> Optional[Annotated["Alignment", strawberry.lazy("graphql_api.types.alignment")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.PerSectionAlignmentParameters)
    relationship = mapper.relationships["alignment"]
    return await dataloader.loader_for(relationship, where, order_by).load(root.alignment_id)  # type:ignore


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
class PerSectionAlignmentParametersWhereClauseMutations(TypedDict):
    id: IntComparators | None


"""
Supported WHERE clause attributes
"""


@strawberry.input
class PerSectionAlignmentParametersWhereClause(TypedDict):
    alignment: Optional[Annotated["AlignmentWhereClause", strawberry.lazy("graphql_api.types.alignment")]] | None
    z_index: Optional[IntComparators] | None
    x_offset: Optional[FloatComparators] | None
    y_offset: Optional[FloatComparators] | None
    in_plane_rotation: Optional[FloatComparators] | None
    beam_tilt: Optional[FloatComparators] | None
    tilt_angle: Optional[FloatComparators] | None
    id: Optional[IntComparators] | None


"""
Supported ORDER BY clause attributes
"""


@strawberry.input
class PerSectionAlignmentParametersOrderByClause(TypedDict):
    alignment: Optional[Annotated["AlignmentOrderByClause", strawberry.lazy("graphql_api.types.alignment")]] | None
    z_index: Optional[orderBy] | None
    x_offset: Optional[orderBy] | None
    y_offset: Optional[orderBy] | None
    in_plane_rotation: Optional[orderBy] | None
    beam_tilt: Optional[orderBy] | None
    tilt_angle: Optional[orderBy] | None
    id: Optional[orderBy] | None


"""
Define PerSectionAlignmentParameters type
"""


@strawberry.type(description="Map alignment parameters to tilt series frames")
class PerSectionAlignmentParameters(EntityInterface):
    alignment: Optional[Annotated["Alignment", strawberry.lazy("graphql_api.types.alignment")]] = (
        load_alignment_rows
    )  # type:ignore
    z_index: int = strawberry.field(description="z-index of the frame in the tiltseries")
    x_offset: Optional[float] = strawberry.field(
        description="In-plane X-shift of the projection in angstrom",
        default=None,
    )
    y_offset: Optional[float] = strawberry.field(
        description="In-plane Y-shift of the projection in angstrom",
        default=None,
    )
    in_plane_rotation: Optional[float] = strawberry.field(
        description="In-plane rotation of the projection in degrees",
        default=None,
    )
    beam_tilt: Optional[float] = strawberry.field(description="Beam tilt during projection in degrees", default=None)
    tilt_angle: Optional[float] = strawberry.field(description="Tilt angle of the projection in degrees", default=None)
    id: int = strawberry.field(description="An identifier to refer to a specific instance of this type")


"""
We need to add this to each Queryable type so that strawberry will accept either our
Strawberry type *or* a SQLAlchemy model instance as a valid response class from a resolver
"""
PerSectionAlignmentParameters.__strawberry_definition__.is_type_of = (  # type: ignore
    lambda obj, info: type(obj) == db.PerSectionAlignmentParameters or type(obj) == PerSectionAlignmentParameters
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
class PerSectionAlignmentParametersNumericalColumns:
    z_index: Optional[int] = None
    x_offset: Optional[float] = None
    y_offset: Optional[float] = None
    in_plane_rotation: Optional[float] = None
    beam_tilt: Optional[float] = None
    tilt_angle: Optional[float] = None
    id: Optional[int] = None


"""
Define columns that support min/max aggregations
"""


@strawberry.type
class PerSectionAlignmentParametersMinMaxColumns:
    z_index: Optional[int] = None
    x_offset: Optional[float] = None
    y_offset: Optional[float] = None
    in_plane_rotation: Optional[float] = None
    beam_tilt: Optional[float] = None
    tilt_angle: Optional[float] = None
    id: Optional[int] = None


"""
Define enum of all columns to support count and count(distinct) aggregations
"""


@strawberry.enum
class PerSectionAlignmentParametersCountColumns(enum.Enum):
    alignment = "alignment"
    zIndex = "z_index"
    xOffset = "x_offset"
    yOffset = "y_offset"
    inPlaneRotation = "in_plane_rotation"
    beamTilt = "beam_tilt"
    tiltAngle = "tilt_angle"
    id = "id"


"""
All supported aggregation functions
"""


@strawberry.type
class PerSectionAlignmentParametersAggregateFunctions:
    # This is a hack to accept "distinct" and "columns" as arguments to "count"
    @strawberry.field
    def count(
        self,
        distinct: Optional[bool] = False,
        columns: Optional[PerSectionAlignmentParametersCountColumns] = None,
    ) -> Optional[int]:
        # Count gets set with the proper value in the resolver, so we just return it here
        return self.count  # type: ignore

    sum: Optional[PerSectionAlignmentParametersNumericalColumns] = None
    avg: Optional[PerSectionAlignmentParametersNumericalColumns] = None
    stddev: Optional[PerSectionAlignmentParametersNumericalColumns] = None
    variance: Optional[PerSectionAlignmentParametersNumericalColumns] = None
    min: Optional[PerSectionAlignmentParametersMinMaxColumns] = None
    max: Optional[PerSectionAlignmentParametersMinMaxColumns] = None
    groupBy: Optional[PerSectionAlignmentParametersGroupByOptions] = None


"""
Wrapper around PerSectionAlignmentParametersAggregateFunctions
"""


@strawberry.type
class PerSectionAlignmentParametersAggregate:
    aggregate: Optional[list[PerSectionAlignmentParametersAggregateFunctions]] = None


"""
------------------------------------------------------------------------------
Mutation types
------------------------------------------------------------------------------
"""


@strawberry.input()
class PerSectionAlignmentParametersCreateInput:
    alignment_id: strawberry.ID = strawberry.field(description="Tiltseries Alignment")
    z_index: int = strawberry.field(description="z-index of the frame in the tiltseries")
    x_offset: Optional[float] = strawberry.field(
        description="In-plane X-shift of the projection in angstrom",
        default=None,
    )
    y_offset: Optional[float] = strawberry.field(
        description="In-plane Y-shift of the projection in angstrom",
        default=None,
    )
    in_plane_rotation: Optional[float] = strawberry.field(
        description="In-plane rotation of the projection in degrees",
        default=None,
    )
    beam_tilt: Optional[float] = strawberry.field(description="Beam tilt during projection in degrees", default=None)
    tilt_angle: Optional[float] = strawberry.field(description="Tilt angle of the projection in degrees", default=None)
    id: int = strawberry.field(description="An identifier to refer to a specific instance of this type")


@strawberry.input()
class PerSectionAlignmentParametersUpdateInput:
    alignment_id: Optional[strawberry.ID] = strawberry.field(description="Tiltseries Alignment")
    z_index: Optional[int] = strawberry.field(description="z-index of the frame in the tiltseries")
    x_offset: Optional[float] = strawberry.field(
        description="In-plane X-shift of the projection in angstrom",
        default=None,
    )
    y_offset: Optional[float] = strawberry.field(
        description="In-plane Y-shift of the projection in angstrom",
        default=None,
    )
    in_plane_rotation: Optional[float] = strawberry.field(
        description="In-plane rotation of the projection in degrees",
        default=None,
    )
    beam_tilt: Optional[float] = strawberry.field(description="Beam tilt during projection in degrees", default=None)
    tilt_angle: Optional[float] = strawberry.field(description="Tilt angle of the projection in degrees", default=None)
    id: Optional[int] = strawberry.field(description="An identifier to refer to a specific instance of this type")


"""
------------------------------------------------------------------------------
Utilities
------------------------------------------------------------------------------
"""


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_per_section_alignment_parameters(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    authz_client: AuthzClient = Depends(get_authz_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[PerSectionAlignmentParametersWhereClause] = None,
    order_by: Optional[list[PerSectionAlignmentParametersOrderByClause]] = [],
    limit_offset: Optional[LimitOffsetClause] = None,
) -> typing.Sequence[PerSectionAlignmentParameters]:
    """
    Resolve PerSectionAlignmentParameters objects. Used for queries (see graphql_api/queries.py).
    """
    limit = limit_offset["limit"] if limit_offset and "limit" in limit_offset else None
    offset = limit_offset["offset"] if limit_offset and "offset" in limit_offset else None
    if offset and not limit:
        raise PlatformicsError("Cannot use offset without limit")
    return await get_db_rows(db.PerSectionAlignmentParameters, session, authz_client, principal, where, order_by, AuthzAction.VIEW, limit, offset)  # type: ignore


def format_per_section_alignment_parameters_aggregate_output(
    query_results: Sequence[RowMapping] | RowMapping,
) -> PerSectionAlignmentParametersAggregate:
    """
    Given a row from the DB containing the results of an aggregate query,
    format the results using the proper GraphQL types.
    """
    aggregate = []
    if type(query_results) is not list:
        query_results = [query_results]  # type: ignore
    for row in query_results:
        aggregate.append(format_per_section_alignment_parameters_aggregate_row(row))
    return PerSectionAlignmentParametersAggregate(aggregate=aggregate)


def format_per_section_alignment_parameters_aggregate_row(
    row: RowMapping,
) -> PerSectionAlignmentParametersAggregateFunctions:
    """
    Given a single row from the DB containing the results of an aggregate query,
    format the results using the proper GraphQL types.
    """
    output = PerSectionAlignmentParametersAggregateFunctions()
    for key, value in row.items():
        # Key is either an aggregate function or a groupby key
        group_keys = key.split(".")
        aggregate = key.split("_", 1)
        if aggregate[0] not in aggregator_map.keys():
            # Turn list of groupby keys into nested objects
            if not output.groupBy:
                output.groupBy = PerSectionAlignmentParametersGroupByOptions()
            group = build_per_section_alignment_parameters_groupby_output(output.groupBy, group_keys, value)
            output.groupBy = group
        else:
            aggregate_name = aggregate[0]
            if aggregate_name == "count":
                output.count = value
            else:
                aggregator_fn, col_name = aggregate[0], aggregate[1]
                if not getattr(output, aggregator_fn):
                    if aggregate_name in ["min", "max"]:
                        setattr(output, aggregator_fn, PerSectionAlignmentParametersMinMaxColumns())
                    else:
                        setattr(output, aggregator_fn, PerSectionAlignmentParametersNumericalColumns())
                setattr(getattr(output, aggregator_fn), col_name, value)
    return output


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_per_section_alignment_parameters_aggregate(
    info: Info,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    authz_client: AuthzClient = Depends(get_authz_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[PerSectionAlignmentParametersWhereClause] = None,
    # TODO: add support for groupby, limit/offset
) -> PerSectionAlignmentParametersAggregate:
    """
    Aggregate values for PerSectionAlignmentParameters objects. Used for queries (see graphql_api/queries.py).
    """
    # Get the selected aggregate functions and columns to operate on, and groupby options if any were provided.
    # TODO: not sure why selected_fields is a list
    selections = info.selected_fields[0].selections[0].selections
    aggregate_selections = [selection for selection in selections if selection.name != "groupBy"]
    groupby_selections = [selection for selection in selections if selection.name == "groupBy"]
    groupby_selections = groupby_selections[0].selections if groupby_selections else []

    if not aggregate_selections:
        raise PlatformicsError("No aggregate functions selected")

    rows = await get_aggregate_db_rows(db.PerSectionAlignmentParameters, session, authz_client, principal, where, aggregate_selections, [], groupby_selections)  # type: ignore
    aggregate_output = format_per_section_alignment_parameters_aggregate_output(rows)
    return aggregate_output


@strawberry.mutation(extensions=[DependencyExtension()])
async def create_per_section_alignment_parameters(
    input: PerSectionAlignmentParametersCreateInput,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    authz_client: AuthzClient = Depends(get_authz_client),
    principal: Principal = Depends(require_auth_principal),
    is_system_user: bool = Depends(is_system_user),
) -> db.PerSectionAlignmentParameters:
    """
    Create a new PerSectionAlignmentParameters object. Used for mutations (see graphql_api/mutations.py).
    """
    validated = PerSectionAlignmentParametersCreateInputValidator(**input.__dict__)
    params = validated.model_dump()

    # Validate that the user can read all of the entities they're linking to.

    # Validate that the user can read all of the entities they're linking to.
    # Check that alignment relationship is accessible.
    if validated.alignment_id:
        alignment = await get_db_rows(
            db.Alignment,
            session,
            authz_client,
            principal,
            {"id": {"_eq": validated.alignment_id}},
            [],
            AuthzAction.VIEW,
        )
        if not alignment:
            raise PlatformicsError("Unauthorized: alignment does not exist")

    # Save to DB
    params["owner_user_id"] = int(principal.id)
    new_entity = db.PerSectionAlignmentParameters(**params)

    # Are we actually allowed to create this entity?
    if not authz_client.can_create(new_entity, principal):
        raise PlatformicsError("Unauthorized: Cannot create entity")

    session.add(new_entity)
    await session.commit()
    return new_entity


@strawberry.mutation(extensions=[DependencyExtension()])
async def update_per_section_alignment_parameters(
    input: PerSectionAlignmentParametersUpdateInput,
    where: PerSectionAlignmentParametersWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    authz_client: AuthzClient = Depends(get_authz_client),
    principal: Principal = Depends(require_auth_principal),
    is_system_user: bool = Depends(is_system_user),
) -> Sequence[db.PerSectionAlignmentParameters]:
    """
    Update PerSectionAlignmentParameters objects. Used for mutations (see graphql_api/mutations.py).
    """
    validated = PerSectionAlignmentParametersUpdateInputValidator(**input.__dict__)
    params = validated.model_dump()

    # Need at least one thing to update
    num_params = len([x for x in params if params[x] is not None])
    if num_params == 0:
        raise PlatformicsError("No fields to update")

    # Validate that the user can read all of the entities they're linking to.
    # Check that alignment relationship is accessible.
    if validated.alignment_id:
        alignment = await get_db_rows(
            db.Alignment,
            session,
            authz_client,
            principal,
            {"id": {"_eq": validated.alignment_id}},
            [],
            AuthzAction.VIEW,
        )
        if not alignment:
            raise PlatformicsError("Unauthorized: alignment does not exist")
        params["alignment"] = alignment[0]
        del params["alignment_id"]

    # Fetch entities for update, if we have access to them
    entities = await get_db_rows(
        db.PerSectionAlignmentParameters,
        session,
        authz_client,
        principal,
        where,
        [],
        AuthzAction.UPDATE,
    )
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
async def delete_per_section_alignment_parameters(
    where: PerSectionAlignmentParametersWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    authz_client: AuthzClient = Depends(get_authz_client),
    principal: Principal = Depends(require_auth_principal),
) -> Sequence[db.PerSectionAlignmentParameters]:
    """
    Delete PerSectionAlignmentParameters objects. Used for mutations (see graphql_api/mutations.py).
    """
    # Fetch entities for deletion, if we have access to them
    entities = await get_db_rows(
        db.PerSectionAlignmentParameters,
        session,
        authz_client,
        principal,
        where,
        [],
        AuthzAction.DELETE,
    )
    if len(entities) == 0:
        raise PlatformicsError("Unauthorized: Cannot delete entities")

    # Update DB
    for entity in entities:
        await session.delete(entity)
    await session.commit()
    return entities
