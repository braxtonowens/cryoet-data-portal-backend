"""
GraphQL type for Annotation

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
from graphql_api.helpers.annotation import AnnotationGroupByOptions, build_annotation_groupby_output
from graphql_api.types.annotation_author import AnnotationAuthorAggregate, format_annotation_author_aggregate_output
from graphql_api.types.annotation_shape import AnnotationShapeAggregate, format_annotation_shape_aggregate_output
from platformics.graphql_api.core.deps import get_authz_client, get_db_session, is_system_user, require_auth_principal
from platformics.graphql_api.core.errors import PlatformicsError
from platformics.graphql_api.core.query_builder import get_aggregate_db_rows, get_db_rows
from platformics.graphql_api.core.query_input_types import (
    BoolComparators,
    DatetimeComparators,
    EnumComparators,
    FloatComparators,
    IntComparators,
    StrComparators,
    aggregator_map,
    orderBy,
)
from platformics.graphql_api.core.relay_interface import EntityInterface
from platformics.graphql_api.core.strawberry_extensions import DependencyExtension
from platformics.security.authorization import AuthzAction, AuthzClient, Principal
from sqlalchemy import inspect
from sqlalchemy.engine.row import RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry import relay
from strawberry.types import Info
from support.enums import annotation_method_type_enum
from support.limit_offset import LimitOffsetClause
from typing_extensions import TypedDict
from validators.annotation import AnnotationCreateInputValidator, AnnotationUpdateInputValidator

E = typing.TypeVar("E")
T = typing.TypeVar("T")

if TYPE_CHECKING:
    from graphql_api.types.annotation_author import (
        AnnotationAuthor,
        AnnotationAuthorOrderByClause,
        AnnotationAuthorWhereClause,
    )
    from graphql_api.types.annotation_shape import (
        AnnotationShape,
        AnnotationShapeOrderByClause,
        AnnotationShapeWhereClause,
    )
    from graphql_api.types.deposition import Deposition, DepositionOrderByClause, DepositionWhereClause
    from graphql_api.types.run import Run, RunOrderByClause, RunWhereClause

    pass
else:
    RunWhereClause = "RunWhereClause"
    Run = "Run"
    RunOrderByClause = "RunOrderByClause"
    AnnotationShapeWhereClause = "AnnotationShapeWhereClause"
    AnnotationShape = "AnnotationShape"
    AnnotationShapeOrderByClause = "AnnotationShapeOrderByClause"
    AnnotationAuthorWhereClause = "AnnotationAuthorWhereClause"
    AnnotationAuthor = "AnnotationAuthor"
    AnnotationAuthorOrderByClause = "AnnotationAuthorOrderByClause"
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
async def load_run_rows(
    root: "Annotation",
    info: Info,
    where: Annotated["RunWhereClause", strawberry.lazy("graphql_api.types.run")] | None = None,
    order_by: Optional[list[Annotated["RunOrderByClause", strawberry.lazy("graphql_api.types.run")]]] = [],
) -> Optional[Annotated["Run", strawberry.lazy("graphql_api.types.run")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Annotation)
    relationship = mapper.relationships["run"]
    return await dataloader.loader_for(relationship, where, order_by).load(root.run_id)  # type:ignore


@relay.connection(
    relay.ListConnection[
        Annotated["AnnotationShape", strawberry.lazy("graphql_api.types.annotation_shape")]
    ],  # type:ignore
)
async def load_annotation_shape_rows(
    root: "Annotation",
    info: Info,
    where: Annotated["AnnotationShapeWhereClause", strawberry.lazy("graphql_api.types.annotation_shape")] | None = None,
    order_by: Optional[
        list[Annotated["AnnotationShapeOrderByClause", strawberry.lazy("graphql_api.types.annotation_shape")]]
    ] = [],
) -> Sequence[Annotated["AnnotationShape", strawberry.lazy("graphql_api.types.annotation_shape")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Annotation)
    relationship = mapper.relationships["annotation_shapes"]
    return await dataloader.loader_for(relationship, where, order_by).load(root.id)  # type:ignore


@strawberry.field
async def load_annotation_shape_aggregate_rows(
    root: "Annotation",
    info: Info,
    where: Annotated["AnnotationShapeWhereClause", strawberry.lazy("graphql_api.types.annotation_shape")] | None = None,
) -> Optional[Annotated["AnnotationShapeAggregate", strawberry.lazy("graphql_api.types.annotation_shape")]]:
    selections = info.selected_fields[0].selections[0].selections
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Annotation)
    relationship = mapper.relationships["annotation_shapes"]
    rows = await dataloader.aggregate_loader_for(relationship, where, selections).load(root.id)  # type:ignore
    aggregate_output = format_annotation_shape_aggregate_output(rows)
    return aggregate_output


@relay.connection(
    relay.ListConnection[
        Annotated["AnnotationAuthor", strawberry.lazy("graphql_api.types.annotation_author")]
    ],  # type:ignore
)
async def load_annotation_author_rows(
    root: "Annotation",
    info: Info,
    where: (
        Annotated["AnnotationAuthorWhereClause", strawberry.lazy("graphql_api.types.annotation_author")] | None
    ) = None,
    order_by: Optional[
        list[Annotated["AnnotationAuthorOrderByClause", strawberry.lazy("graphql_api.types.annotation_author")]]
    ] = [],
) -> Sequence[Annotated["AnnotationAuthor", strawberry.lazy("graphql_api.types.annotation_author")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Annotation)
    relationship = mapper.relationships["authors"]
    return await dataloader.loader_for(relationship, where, order_by).load(root.id)  # type:ignore


@strawberry.field
async def load_annotation_author_aggregate_rows(
    root: "Annotation",
    info: Info,
    where: (
        Annotated["AnnotationAuthorWhereClause", strawberry.lazy("graphql_api.types.annotation_author")] | None
    ) = None,
) -> Optional[Annotated["AnnotationAuthorAggregate", strawberry.lazy("graphql_api.types.annotation_author")]]:
    selections = info.selected_fields[0].selections[0].selections
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Annotation)
    relationship = mapper.relationships["authors"]
    rows = await dataloader.aggregate_loader_for(relationship, where, selections).load(root.id)  # type:ignore
    aggregate_output = format_annotation_author_aggregate_output(rows)
    return aggregate_output


@strawberry.field
async def load_deposition_rows(
    root: "Annotation",
    info: Info,
    where: Annotated["DepositionWhereClause", strawberry.lazy("graphql_api.types.deposition")] | None = None,
    order_by: Optional[
        list[Annotated["DepositionOrderByClause", strawberry.lazy("graphql_api.types.deposition")]]
    ] = [],
) -> Optional[Annotated["Deposition", strawberry.lazy("graphql_api.types.deposition")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Annotation)
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
class AnnotationWhereClauseMutations(TypedDict):
    id: IntComparators | None


"""
Supported WHERE clause attributes
"""


@strawberry.input
class AnnotationWhereClause(TypedDict):
    run: Optional[Annotated["RunWhereClause", strawberry.lazy("graphql_api.types.run")]] | None
    annotation_shapes: (
        Optional[Annotated["AnnotationShapeWhereClause", strawberry.lazy("graphql_api.types.annotation_shape")]] | None
    )
    authors: (
        Optional[Annotated["AnnotationAuthorWhereClause", strawberry.lazy("graphql_api.types.annotation_author")]]
        | None
    )
    deposition: Optional[Annotated["DepositionWhereClause", strawberry.lazy("graphql_api.types.deposition")]] | None
    s3_metadata_path: Optional[StrComparators] | None
    https_metadata_path: Optional[StrComparators] | None
    annotation_publication: Optional[StrComparators] | None
    annotation_method: Optional[StrComparators] | None
    ground_truth_status: Optional[BoolComparators] | None
    object_id: Optional[StrComparators] | None
    object_name: Optional[StrComparators] | None
    object_description: Optional[StrComparators] | None
    object_state: Optional[StrComparators] | None
    object_count: Optional[IntComparators] | None
    confidence_precision: Optional[FloatComparators] | None
    confidence_recall: Optional[FloatComparators] | None
    ground_truth_used: Optional[StrComparators] | None
    annotation_software: Optional[StrComparators] | None
    is_curator_recommended: Optional[BoolComparators] | None
    method_type: Optional[EnumComparators[annotation_method_type_enum]] | None
    deposition_date: Optional[DatetimeComparators] | None
    release_date: Optional[DatetimeComparators] | None
    last_modified_date: Optional[DatetimeComparators] | None
    id: Optional[IntComparators] | None


"""
Supported ORDER BY clause attributes
"""


@strawberry.input
class AnnotationOrderByClause(TypedDict):
    run: Optional[Annotated["RunOrderByClause", strawberry.lazy("graphql_api.types.run")]] | None
    deposition: Optional[Annotated["DepositionOrderByClause", strawberry.lazy("graphql_api.types.deposition")]] | None
    s3_metadata_path: Optional[orderBy] | None
    https_metadata_path: Optional[orderBy] | None
    annotation_publication: Optional[orderBy] | None
    annotation_method: Optional[orderBy] | None
    ground_truth_status: Optional[orderBy] | None
    object_id: Optional[orderBy] | None
    object_name: Optional[orderBy] | None
    object_description: Optional[orderBy] | None
    object_state: Optional[orderBy] | None
    object_count: Optional[orderBy] | None
    confidence_precision: Optional[orderBy] | None
    confidence_recall: Optional[orderBy] | None
    ground_truth_used: Optional[orderBy] | None
    annotation_software: Optional[orderBy] | None
    is_curator_recommended: Optional[orderBy] | None
    method_type: Optional[orderBy] | None
    deposition_date: Optional[orderBy] | None
    release_date: Optional[orderBy] | None
    last_modified_date: Optional[orderBy] | None
    id: Optional[orderBy] | None


"""
Define Annotation type
"""


@strawberry.type(description="Metadata about an annotation for a run")
class Annotation(EntityInterface):
    run: Optional[Annotated["Run", strawberry.lazy("graphql_api.types.run")]] = load_run_rows  # type:ignore
    annotation_shapes: Sequence[Annotated["AnnotationShape", strawberry.lazy("graphql_api.types.annotation_shape")]] = (
        load_annotation_shape_rows
    )  # type:ignore
    annotation_shapes_aggregate: Optional[
        Annotated["AnnotationShapeAggregate", strawberry.lazy("graphql_api.types.annotation_shape")]
    ] = load_annotation_shape_aggregate_rows  # type:ignore
    authors: Sequence[Annotated["AnnotationAuthor", strawberry.lazy("graphql_api.types.annotation_author")]] = (
        load_annotation_author_rows
    )  # type:ignore
    authors_aggregate: Optional[
        Annotated["AnnotationAuthorAggregate", strawberry.lazy("graphql_api.types.annotation_author")]
    ] = load_annotation_author_aggregate_rows  # type:ignore
    deposition: Optional[Annotated["Deposition", strawberry.lazy("graphql_api.types.deposition")]] = (
        load_deposition_rows
    )  # type:ignore
    s3_metadata_path: str = strawberry.field(description="Path to the file in s3")
    https_metadata_path: str = strawberry.field(description="Path to the file as an https url")
    annotation_publication: Optional[str] = strawberry.field(
        description="List of publication IDs (EMPIAR, EMDB, DOI) that describe this annotation method. Comma separated.",
        default=None,
    )
    annotation_method: str = strawberry.field(
        description="Describe how the annotation is made (e.g. Manual, crYoLO, Positive Unlabeled Learning, template matching)",
    )
    ground_truth_status: Optional[bool] = strawberry.field(
        description="Whether an annotation is considered ground truth, as determined by the annotator.",
        default=None,
    )
    object_id: str = strawberry.field(
        description="Gene Ontology Cellular Component identifier for the annotation object",
    )
    object_name: str = strawberry.field(
        description="Name of the object being annotated (e.g. ribosome, nuclear pore complex, actin filament, membrane)",
    )
    object_description: Optional[str] = strawberry.field(
        description="A textual description of the annotation object, can be a longer description to include additional information not covered by the Annotation object name and state.",
        default=None,
    )
    object_state: Optional[str] = strawberry.field(
        description="Molecule state annotated (e.g. open, closed)",
        default=None,
    )
    object_count: Optional[int] = strawberry.field(description="Number of objects identified", default=None)
    confidence_precision: Optional[float] = strawberry.field(
        description="Describe the confidence level of the annotation. Precision is defined as the % of annotation objects being true positive",
        default=None,
    )
    confidence_recall: Optional[float] = strawberry.field(
        description="Describe the confidence level of the annotation. Recall is defined as the % of true positives being annotated correctly",
        default=None,
    )
    ground_truth_used: Optional[str] = strawberry.field(
        description="Annotation filename used as ground truth for precision and recall",
        default=None,
    )
    annotation_software: Optional[str] = strawberry.field(
        description="Software used for generating this annotation",
        default=None,
    )
    is_curator_recommended: Optional[bool] = strawberry.field(
        description="This annotation is recommended by the curator to be preferred for this object type.",
        default=None,
    )
    method_type: annotation_method_type_enum = strawberry.field(
        description="Classification of the annotation method based on supervision.",
    )
    deposition_date: datetime.datetime = strawberry.field(
        description="The date a data item was received by the cryoET data portal.",
    )
    release_date: datetime.datetime = strawberry.field(
        description="The date a data item was received by the cryoET data portal.",
    )
    last_modified_date: datetime.datetime = strawberry.field(
        description="The date a piece of data was last modified on the cryoET data portal.",
    )
    id: int = strawberry.field(description="An identifier to refer to a specific instance of this type")


"""
We need to add this to each Queryable type so that strawberry will accept either our
Strawberry type *or* a SQLAlchemy model instance as a valid response class from a resolver
"""
Annotation.__strawberry_definition__.is_type_of = (  # type: ignore
    lambda obj, info: type(obj) == db.Annotation or type(obj) == Annotation
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
class AnnotationNumericalColumns:
    object_count: Optional[int] = None
    confidence_precision: Optional[float] = None
    confidence_recall: Optional[float] = None
    id: Optional[int] = None


"""
Define columns that support min/max aggregations
"""


@strawberry.type
class AnnotationMinMaxColumns:
    s3_metadata_path: Optional[str] = None
    https_metadata_path: Optional[str] = None
    annotation_publication: Optional[str] = None
    annotation_method: Optional[str] = None
    object_id: Optional[str] = None
    object_name: Optional[str] = None
    object_description: Optional[str] = None
    object_state: Optional[str] = None
    object_count: Optional[int] = None
    confidence_precision: Optional[float] = None
    confidence_recall: Optional[float] = None
    ground_truth_used: Optional[str] = None
    annotation_software: Optional[str] = None
    deposition_date: Optional[datetime.datetime] = None
    release_date: Optional[datetime.datetime] = None
    last_modified_date: Optional[datetime.datetime] = None
    id: Optional[int] = None


"""
Define enum of all columns to support count and count(distinct) aggregations
"""


@strawberry.enum
class AnnotationCountColumns(enum.Enum):
    run = "run"
    annotationShapes = "annotation_shapes"
    authors = "authors"
    deposition = "deposition"
    s3MetadataPath = "s3_metadata_path"
    httpsMetadataPath = "https_metadata_path"
    annotationPublication = "annotation_publication"
    annotationMethod = "annotation_method"
    groundTruthStatus = "ground_truth_status"
    objectId = "object_id"
    objectName = "object_name"
    objectDescription = "object_description"
    objectState = "object_state"
    objectCount = "object_count"
    confidencePrecision = "confidence_precision"
    confidenceRecall = "confidence_recall"
    groundTruthUsed = "ground_truth_used"
    annotationSoftware = "annotation_software"
    isCuratorRecommended = "is_curator_recommended"
    methodType = "method_type"
    depositionDate = "deposition_date"
    releaseDate = "release_date"
    lastModifiedDate = "last_modified_date"
    id = "id"


"""
All supported aggregation functions
"""


@strawberry.type
class AnnotationAggregateFunctions:
    # This is a hack to accept "distinct" and "columns" as arguments to "count"
    @strawberry.field
    def count(
        self,
        distinct: Optional[bool] = False,
        columns: Optional[AnnotationCountColumns] = None,
    ) -> Optional[int]:
        # Count gets set with the proper value in the resolver, so we just return it here
        return self.count  # type: ignore

    sum: Optional[AnnotationNumericalColumns] = None
    avg: Optional[AnnotationNumericalColumns] = None
    stddev: Optional[AnnotationNumericalColumns] = None
    variance: Optional[AnnotationNumericalColumns] = None
    min: Optional[AnnotationMinMaxColumns] = None
    max: Optional[AnnotationMinMaxColumns] = None
    groupBy: Optional[AnnotationGroupByOptions] = None


"""
Wrapper around AnnotationAggregateFunctions
"""


@strawberry.type
class AnnotationAggregate:
    aggregate: Optional[list[AnnotationAggregateFunctions]] = None


"""
------------------------------------------------------------------------------
Mutation types
------------------------------------------------------------------------------
"""


@strawberry.input()
class AnnotationCreateInput:
    run_id: Optional[strawberry.ID] = strawberry.field(description=None, default=None)
    deposition_id: Optional[strawberry.ID] = strawberry.field(description=None, default=None)
    s3_metadata_path: str = strawberry.field(description="Path to the file in s3")
    https_metadata_path: str = strawberry.field(description="Path to the file as an https url")
    annotation_publication: Optional[str] = strawberry.field(
        description="List of publication IDs (EMPIAR, EMDB, DOI) that describe this annotation method. Comma separated.",
        default=None,
    )
    annotation_method: str = strawberry.field(
        description="Describe how the annotation is made (e.g. Manual, crYoLO, Positive Unlabeled Learning, template matching)",
    )
    ground_truth_status: Optional[bool] = strawberry.field(
        description="Whether an annotation is considered ground truth, as determined by the annotator.",
        default=None,
    )
    object_id: str = strawberry.field(
        description="Gene Ontology Cellular Component identifier for the annotation object",
    )
    object_name: str = strawberry.field(
        description="Name of the object being annotated (e.g. ribosome, nuclear pore complex, actin filament, membrane)",
    )
    object_description: Optional[str] = strawberry.field(
        description="A textual description of the annotation object, can be a longer description to include additional information not covered by the Annotation object name and state.",
        default=None,
    )
    object_state: Optional[str] = strawberry.field(
        description="Molecule state annotated (e.g. open, closed)",
        default=None,
    )
    object_count: Optional[int] = strawberry.field(description="Number of objects identified", default=None)
    confidence_precision: Optional[float] = strawberry.field(
        description="Describe the confidence level of the annotation. Precision is defined as the % of annotation objects being true positive",
        default=None,
    )
    confidence_recall: Optional[float] = strawberry.field(
        description="Describe the confidence level of the annotation. Recall is defined as the % of true positives being annotated correctly",
        default=None,
    )
    ground_truth_used: Optional[str] = strawberry.field(
        description="Annotation filename used as ground truth for precision and recall",
        default=None,
    )
    annotation_software: Optional[str] = strawberry.field(
        description="Software used for generating this annotation",
        default=None,
    )
    is_curator_recommended: Optional[bool] = strawberry.field(
        description="This annotation is recommended by the curator to be preferred for this object type.",
        default=None,
    )
    method_type: annotation_method_type_enum = strawberry.field(
        description="Classification of the annotation method based on supervision.",
    )
    deposition_date: datetime.datetime = strawberry.field(
        description="The date a data item was received by the cryoET data portal.",
    )
    release_date: datetime.datetime = strawberry.field(
        description="The date a data item was received by the cryoET data portal.",
    )
    last_modified_date: datetime.datetime = strawberry.field(
        description="The date a piece of data was last modified on the cryoET data portal.",
    )
    id: int = strawberry.field(description="An identifier to refer to a specific instance of this type")


@strawberry.input()
class AnnotationUpdateInput:
    run_id: Optional[strawberry.ID] = strawberry.field(description=None, default=None)
    deposition_id: Optional[strawberry.ID] = strawberry.field(description=None, default=None)
    s3_metadata_path: Optional[str] = strawberry.field(description="Path to the file in s3")
    https_metadata_path: Optional[str] = strawberry.field(description="Path to the file as an https url")
    annotation_publication: Optional[str] = strawberry.field(
        description="List of publication IDs (EMPIAR, EMDB, DOI) that describe this annotation method. Comma separated.",
        default=None,
    )
    annotation_method: Optional[str] = strawberry.field(
        description="Describe how the annotation is made (e.g. Manual, crYoLO, Positive Unlabeled Learning, template matching)",
    )
    ground_truth_status: Optional[bool] = strawberry.field(
        description="Whether an annotation is considered ground truth, as determined by the annotator.",
        default=None,
    )
    object_id: Optional[str] = strawberry.field(
        description="Gene Ontology Cellular Component identifier for the annotation object",
    )
    object_name: Optional[str] = strawberry.field(
        description="Name of the object being annotated (e.g. ribosome, nuclear pore complex, actin filament, membrane)",
    )
    object_description: Optional[str] = strawberry.field(
        description="A textual description of the annotation object, can be a longer description to include additional information not covered by the Annotation object name and state.",
        default=None,
    )
    object_state: Optional[str] = strawberry.field(
        description="Molecule state annotated (e.g. open, closed)",
        default=None,
    )
    object_count: Optional[int] = strawberry.field(description="Number of objects identified", default=None)
    confidence_precision: Optional[float] = strawberry.field(
        description="Describe the confidence level of the annotation. Precision is defined as the % of annotation objects being true positive",
        default=None,
    )
    confidence_recall: Optional[float] = strawberry.field(
        description="Describe the confidence level of the annotation. Recall is defined as the % of true positives being annotated correctly",
        default=None,
    )
    ground_truth_used: Optional[str] = strawberry.field(
        description="Annotation filename used as ground truth for precision and recall",
        default=None,
    )
    annotation_software: Optional[str] = strawberry.field(
        description="Software used for generating this annotation",
        default=None,
    )
    is_curator_recommended: Optional[bool] = strawberry.field(
        description="This annotation is recommended by the curator to be preferred for this object type.",
        default=None,
    )
    method_type: Optional[annotation_method_type_enum] = strawberry.field(
        description="Classification of the annotation method based on supervision.",
    )
    deposition_date: Optional[datetime.datetime] = strawberry.field(
        description="The date a data item was received by the cryoET data portal.",
    )
    release_date: Optional[datetime.datetime] = strawberry.field(
        description="The date a data item was received by the cryoET data portal.",
    )
    last_modified_date: Optional[datetime.datetime] = strawberry.field(
        description="The date a piece of data was last modified on the cryoET data portal.",
    )
    id: Optional[int] = strawberry.field(description="An identifier to refer to a specific instance of this type")


"""
------------------------------------------------------------------------------
Utilities
------------------------------------------------------------------------------
"""


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_annotations(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    authz_client: AuthzClient = Depends(get_authz_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[AnnotationWhereClause] = None,
    order_by: Optional[list[AnnotationOrderByClause]] = [],
    limit_offset: Optional[LimitOffsetClause] = None,
) -> typing.Sequence[Annotation]:
    """
    Resolve Annotation objects. Used for queries (see graphql_api/queries.py).
    """
    limit = limit_offset["limit"] if limit_offset and "limit" in limit_offset else None
    offset = limit_offset["offset"] if limit_offset and "offset" in limit_offset else None
    if offset and not limit:
        raise PlatformicsError("Cannot use offset without limit")
    return await get_db_rows(db.Annotation, session, authz_client, principal, where, order_by, AuthzAction.VIEW, limit, offset)  # type: ignore


def format_annotation_aggregate_output(query_results: Sequence[RowMapping] | RowMapping) -> AnnotationAggregate:
    """
    Given a row from the DB containing the results of an aggregate query,
    format the results using the proper GraphQL types.
    """
    aggregate = []
    if type(query_results) is not list:
        query_results = [query_results]  # type: ignore
    for row in query_results:
        aggregate.append(format_annotation_aggregate_row(row))
    return AnnotationAggregate(aggregate=aggregate)


def format_annotation_aggregate_row(row: RowMapping) -> AnnotationAggregateFunctions:
    """
    Given a single row from the DB containing the results of an aggregate query,
    format the results using the proper GraphQL types.
    """
    output = AnnotationAggregateFunctions()
    for key, value in row.items():
        # Key is either an aggregate function or a groupby key
        group_keys = key.split(".")
        aggregate = key.split("_", 1)
        if aggregate[0] not in aggregator_map.keys():
            # Turn list of groupby keys into nested objects
            if not output.groupBy:
                output.groupBy = AnnotationGroupByOptions()
            group = build_annotation_groupby_output(output.groupBy, group_keys, value)
            output.groupBy = group
        else:
            aggregate_name = aggregate[0]
            if aggregate_name == "count":
                output.count = value
            else:
                aggregator_fn, col_name = aggregate[0], aggregate[1]
                if not getattr(output, aggregator_fn):
                    if aggregate_name in ["min", "max"]:
                        setattr(output, aggregator_fn, AnnotationMinMaxColumns())
                    else:
                        setattr(output, aggregator_fn, AnnotationNumericalColumns())
                setattr(getattr(output, aggregator_fn), col_name, value)
    return output


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_annotations_aggregate(
    info: Info,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    authz_client: AuthzClient = Depends(get_authz_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[AnnotationWhereClause] = None,
    # TODO: add support for groupby, limit/offset
) -> AnnotationAggregate:
    """
    Aggregate values for Annotation objects. Used for queries (see graphql_api/queries.py).
    """
    # Get the selected aggregate functions and columns to operate on, and groupby options if any were provided.
    # TODO: not sure why selected_fields is a list
    selections = info.selected_fields[0].selections[0].selections
    aggregate_selections = [selection for selection in selections if selection.name != "groupBy"]
    groupby_selections = [selection for selection in selections if selection.name == "groupBy"]
    groupby_selections = groupby_selections[0].selections if groupby_selections else []

    if not aggregate_selections:
        raise PlatformicsError("No aggregate functions selected")

    rows = await get_aggregate_db_rows(db.Annotation, session, authz_client, principal, where, aggregate_selections, [], groupby_selections)  # type: ignore
    aggregate_output = format_annotation_aggregate_output(rows)
    return aggregate_output


@strawberry.mutation(extensions=[DependencyExtension()])
async def create_annotation(
    input: AnnotationCreateInput,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    authz_client: AuthzClient = Depends(get_authz_client),
    principal: Principal = Depends(require_auth_principal),
    is_system_user: bool = Depends(is_system_user),
) -> db.Annotation:
    """
    Create a new Annotation object. Used for mutations (see graphql_api/mutations.py).
    """
    validated = AnnotationCreateInputValidator(**input.__dict__)
    params = validated.model_dump()

    # Validate that the user can read all of the entities they're linking to.

    # Validate that the user can read all of the entities they're linking to.
    # Check that run relationship is accessible.
    if validated.run_id:
        run = await get_db_rows(
            db.Run,
            session,
            authz_client,
            principal,
            {"id": {"_eq": validated.run_id}},
            [],
            AuthzAction.VIEW,
        )
        if not run:
            raise PlatformicsError("Unauthorized: run does not exist")
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
    new_entity = db.Annotation(**params)

    # Are we actually allowed to create this entity?
    if not authz_client.can_create(new_entity, principal):
        raise PlatformicsError("Unauthorized: Cannot create entity")

    session.add(new_entity)
    await session.commit()
    return new_entity


@strawberry.mutation(extensions=[DependencyExtension()])
async def update_annotation(
    input: AnnotationUpdateInput,
    where: AnnotationWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    authz_client: AuthzClient = Depends(get_authz_client),
    principal: Principal = Depends(require_auth_principal),
    is_system_user: bool = Depends(is_system_user),
) -> Sequence[db.Annotation]:
    """
    Update Annotation objects. Used for mutations (see graphql_api/mutations.py).
    """
    validated = AnnotationUpdateInputValidator(**input.__dict__)
    params = validated.model_dump()

    # Need at least one thing to update
    num_params = len([x for x in params if params[x] is not None])
    if num_params == 0:
        raise PlatformicsError("No fields to update")

    # Validate that the user can read all of the entities they're linking to.
    # Check that run relationship is accessible.
    if validated.run_id:
        run = await get_db_rows(
            db.Run,
            session,
            authz_client,
            principal,
            {"id": {"_eq": validated.run_id}},
            [],
            AuthzAction.VIEW,
        )
        if not run:
            raise PlatformicsError("Unauthorized: run does not exist")
        params["run"] = run[0]
        del params["run_id"]
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
    entities = await get_db_rows(db.Annotation, session, authz_client, principal, where, [], AuthzAction.UPDATE)
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
async def delete_annotation(
    where: AnnotationWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    authz_client: AuthzClient = Depends(get_authz_client),
    principal: Principal = Depends(require_auth_principal),
) -> Sequence[db.Annotation]:
    """
    Delete Annotation objects. Used for mutations (see graphql_api/mutations.py).
    """
    # Fetch entities for deletion, if we have access to them
    entities = await get_db_rows(db.Annotation, session, authz_client, principal, where, [], AuthzAction.DELETE)
    if len(entities) == 0:
        raise PlatformicsError("Unauthorized: Cannot delete entities")

    # Update DB
    for entity in entities:
        await session.delete(entity)
    await session.commit()
    return entities
