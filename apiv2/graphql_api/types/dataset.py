"""
GraphQL type for Dataset

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
from graphql_api.helpers.dataset import DatasetGroupByOptions, build_dataset_groupby_output
from graphql_api.types.dataset_author import DatasetAuthorAggregate, format_dataset_author_aggregate_output
from graphql_api.types.dataset_funding import DatasetFundingAggregate, format_dataset_funding_aggregate_output
from graphql_api.types.run import RunAggregate, format_run_aggregate_output
from platformics.graphql_api.core.deps import get_authz_client, get_db_session, is_system_user, require_auth_principal
from platformics.graphql_api.core.errors import PlatformicsError
from platformics.graphql_api.core.query_builder import get_aggregate_db_rows, get_db_rows
from platformics.graphql_api.core.query_input_types import (
    DatetimeComparators,
    EnumComparators,
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
from support.enums import sample_type_enum
from support.limit_offset import LimitOffsetClause
from typing_extensions import TypedDict
from validators.dataset import DatasetCreateInputValidator, DatasetUpdateInputValidator

E = typing.TypeVar("E")
T = typing.TypeVar("T")

if TYPE_CHECKING:
    from graphql_api.types.dataset_author import DatasetAuthor, DatasetAuthorOrderByClause, DatasetAuthorWhereClause
    from graphql_api.types.dataset_funding import DatasetFunding, DatasetFundingOrderByClause, DatasetFundingWhereClause
    from graphql_api.types.deposition import Deposition, DepositionOrderByClause, DepositionWhereClause
    from graphql_api.types.run import Run, RunOrderByClause, RunWhereClause

    pass
else:
    DepositionWhereClause = "DepositionWhereClause"
    Deposition = "Deposition"
    DepositionOrderByClause = "DepositionOrderByClause"
    DatasetFundingWhereClause = "DatasetFundingWhereClause"
    DatasetFunding = "DatasetFunding"
    DatasetFundingOrderByClause = "DatasetFundingOrderByClause"
    DatasetAuthorWhereClause = "DatasetAuthorWhereClause"
    DatasetAuthor = "DatasetAuthor"
    DatasetAuthorOrderByClause = "DatasetAuthorOrderByClause"
    RunWhereClause = "RunWhereClause"
    Run = "Run"
    RunOrderByClause = "RunOrderByClause"
    pass


"""
------------------------------------------------------------------------------
Dataloaders
------------------------------------------------------------------------------
These are batching functions for loading related objects to avoid N+1 queries.
"""


@strawberry.field
async def load_deposition_rows(
    root: "Dataset",
    info: Info,
    where: Annotated["DepositionWhereClause", strawberry.lazy("graphql_api.types.deposition")] | None = None,
    order_by: Optional[
        list[Annotated["DepositionOrderByClause", strawberry.lazy("graphql_api.types.deposition")]]
    ] = [],
) -> Optional[Annotated["Deposition", strawberry.lazy("graphql_api.types.deposition")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Dataset)
    relationship = mapper.relationships["deposition"]
    return await dataloader.loader_for(relationship, where, order_by).load(root.deposition_id)  # type:ignore


@relay.connection(
    relay.ListConnection[
        Annotated["DatasetFunding", strawberry.lazy("graphql_api.types.dataset_funding")]
    ],  # type:ignore
)
async def load_dataset_funding_rows(
    root: "Dataset",
    info: Info,
    where: Annotated["DatasetFundingWhereClause", strawberry.lazy("graphql_api.types.dataset_funding")] | None = None,
    order_by: Optional[
        list[Annotated["DatasetFundingOrderByClause", strawberry.lazy("graphql_api.types.dataset_funding")]]
    ] = [],
) -> Sequence[Annotated["DatasetFunding", strawberry.lazy("graphql_api.types.dataset_funding")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Dataset)
    relationship = mapper.relationships["funding_sources"]
    return await dataloader.loader_for(relationship, where, order_by).load(root.id)  # type:ignore


@strawberry.field
async def load_dataset_funding_aggregate_rows(
    root: "Dataset",
    info: Info,
    where: Annotated["DatasetFundingWhereClause", strawberry.lazy("graphql_api.types.dataset_funding")] | None = None,
) -> Optional[Annotated["DatasetFundingAggregate", strawberry.lazy("graphql_api.types.dataset_funding")]]:
    selections = info.selected_fields[0].selections[0].selections
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Dataset)
    relationship = mapper.relationships["funding_sources"]
    rows = await dataloader.aggregate_loader_for(relationship, where, selections).load(root.id)  # type:ignore
    aggregate_output = format_dataset_funding_aggregate_output(rows)
    return aggregate_output


@relay.connection(
    relay.ListConnection[
        Annotated["DatasetAuthor", strawberry.lazy("graphql_api.types.dataset_author")]
    ],  # type:ignore
)
async def load_dataset_author_rows(
    root: "Dataset",
    info: Info,
    where: Annotated["DatasetAuthorWhereClause", strawberry.lazy("graphql_api.types.dataset_author")] | None = None,
    order_by: Optional[
        list[Annotated["DatasetAuthorOrderByClause", strawberry.lazy("graphql_api.types.dataset_author")]]
    ] = [],
) -> Sequence[Annotated["DatasetAuthor", strawberry.lazy("graphql_api.types.dataset_author")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Dataset)
    relationship = mapper.relationships["authors"]
    return await dataloader.loader_for(relationship, where, order_by).load(root.id)  # type:ignore


@strawberry.field
async def load_dataset_author_aggregate_rows(
    root: "Dataset",
    info: Info,
    where: Annotated["DatasetAuthorWhereClause", strawberry.lazy("graphql_api.types.dataset_author")] | None = None,
) -> Optional[Annotated["DatasetAuthorAggregate", strawberry.lazy("graphql_api.types.dataset_author")]]:
    selections = info.selected_fields[0].selections[0].selections
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Dataset)
    relationship = mapper.relationships["authors"]
    rows = await dataloader.aggregate_loader_for(relationship, where, selections).load(root.id)  # type:ignore
    aggregate_output = format_dataset_author_aggregate_output(rows)
    return aggregate_output


@relay.connection(
    relay.ListConnection[Annotated["Run", strawberry.lazy("graphql_api.types.run")]],  # type:ignore
)
async def load_run_rows(
    root: "Dataset",
    info: Info,
    where: Annotated["RunWhereClause", strawberry.lazy("graphql_api.types.run")] | None = None,
    order_by: Optional[list[Annotated["RunOrderByClause", strawberry.lazy("graphql_api.types.run")]]] = [],
) -> Sequence[Annotated["Run", strawberry.lazy("graphql_api.types.run")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Dataset)
    relationship = mapper.relationships["runs"]
    return await dataloader.loader_for(relationship, where, order_by).load(root.id)  # type:ignore


@strawberry.field
async def load_run_aggregate_rows(
    root: "Dataset",
    info: Info,
    where: Annotated["RunWhereClause", strawberry.lazy("graphql_api.types.run")] | None = None,
) -> Optional[Annotated["RunAggregate", strawberry.lazy("graphql_api.types.run")]]:
    selections = info.selected_fields[0].selections[0].selections
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Dataset)
    relationship = mapper.relationships["runs"]
    rows = await dataloader.aggregate_loader_for(relationship, where, selections).load(root.id)  # type:ignore
    aggregate_output = format_run_aggregate_output(rows)
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
class DatasetWhereClauseMutations(TypedDict):
    id: IntComparators | None


"""
Supported WHERE clause attributes
"""


@strawberry.input
class DatasetWhereClause(TypedDict):
    deposition: Optional[Annotated["DepositionWhereClause", strawberry.lazy("graphql_api.types.deposition")]] | None
    funding_sources: (
        Optional[Annotated["DatasetFundingWhereClause", strawberry.lazy("graphql_api.types.dataset_funding")]] | None
    )
    authors: Optional[Annotated["DatasetAuthorWhereClause", strawberry.lazy("graphql_api.types.dataset_author")]] | None
    runs: Optional[Annotated["RunWhereClause", strawberry.lazy("graphql_api.types.run")]] | None
    title: Optional[StrComparators] | None
    description: Optional[StrComparators] | None
    organism_name: Optional[StrComparators] | None
    organism_taxid: Optional[IntComparators] | None
    tissue_name: Optional[StrComparators] | None
    tissue_id: Optional[StrComparators] | None
    cell_name: Optional[StrComparators] | None
    cell_type_id: Optional[StrComparators] | None
    cell_strain_name: Optional[StrComparators] | None
    cell_strain_id: Optional[StrComparators] | None
    sample_type: Optional[EnumComparators[sample_type_enum]] | None
    sample_preparation: Optional[StrComparators] | None
    grid_preparation: Optional[StrComparators] | None
    other_setup: Optional[StrComparators] | None
    key_photo_url: Optional[StrComparators] | None
    key_photo_thumbnail_url: Optional[StrComparators] | None
    cell_component_name: Optional[StrComparators] | None
    cell_component_id: Optional[StrComparators] | None
    deposition_date: Optional[DatetimeComparators] | None
    release_date: Optional[DatetimeComparators] | None
    last_modified_date: Optional[DatetimeComparators] | None
    publications: Optional[StrComparators] | None
    related_database_entries: Optional[StrComparators] | None
    related_database_links: Optional[StrComparators] | None
    dataset_citations: Optional[StrComparators] | None
    s3_prefix: Optional[StrComparators] | None
    https_prefix: Optional[StrComparators] | None
    id: Optional[IntComparators] | None


"""
Supported ORDER BY clause attributes
"""


@strawberry.input
class DatasetOrderByClause(TypedDict):
    deposition: Optional[Annotated["DepositionOrderByClause", strawberry.lazy("graphql_api.types.deposition")]] | None
    title: Optional[orderBy] | None
    description: Optional[orderBy] | None
    organism_name: Optional[orderBy] | None
    organism_taxid: Optional[orderBy] | None
    tissue_name: Optional[orderBy] | None
    tissue_id: Optional[orderBy] | None
    cell_name: Optional[orderBy] | None
    cell_type_id: Optional[orderBy] | None
    cell_strain_name: Optional[orderBy] | None
    cell_strain_id: Optional[orderBy] | None
    sample_type: Optional[orderBy] | None
    sample_preparation: Optional[orderBy] | None
    grid_preparation: Optional[orderBy] | None
    other_setup: Optional[orderBy] | None
    key_photo_url: Optional[orderBy] | None
    key_photo_thumbnail_url: Optional[orderBy] | None
    cell_component_name: Optional[orderBy] | None
    cell_component_id: Optional[orderBy] | None
    deposition_date: Optional[orderBy] | None
    release_date: Optional[orderBy] | None
    last_modified_date: Optional[orderBy] | None
    publications: Optional[orderBy] | None
    related_database_entries: Optional[orderBy] | None
    related_database_links: Optional[orderBy] | None
    dataset_citations: Optional[orderBy] | None
    s3_prefix: Optional[orderBy] | None
    https_prefix: Optional[orderBy] | None
    id: Optional[orderBy] | None


"""
Define Dataset type
"""


@strawberry.type(description="An author of a dataset")
class Dataset(EntityInterface):
    deposition: Optional[Annotated["Deposition", strawberry.lazy("graphql_api.types.deposition")]] = (
        load_deposition_rows
    )  # type:ignore
    funding_sources: Sequence[Annotated["DatasetFunding", strawberry.lazy("graphql_api.types.dataset_funding")]] = (
        load_dataset_funding_rows
    )  # type:ignore
    funding_sources_aggregate: Optional[
        Annotated["DatasetFundingAggregate", strawberry.lazy("graphql_api.types.dataset_funding")]
    ] = load_dataset_funding_aggregate_rows  # type:ignore
    authors: Sequence[Annotated["DatasetAuthor", strawberry.lazy("graphql_api.types.dataset_author")]] = (
        load_dataset_author_rows
    )  # type:ignore
    authors_aggregate: Optional[
        Annotated["DatasetAuthorAggregate", strawberry.lazy("graphql_api.types.dataset_author")]
    ] = load_dataset_author_aggregate_rows  # type:ignore
    runs: Sequence[Annotated["Run", strawberry.lazy("graphql_api.types.run")]] = load_run_rows  # type:ignore
    runs_aggregate: Optional[Annotated["RunAggregate", strawberry.lazy("graphql_api.types.run")]] = (
        load_run_aggregate_rows
    )  # type:ignore
    title: str = strawberry.field(description="Title of a CryoET dataset.")
    description: str = strawberry.field(
        description="A short description of a CryoET dataset, similar to an abstract for a journal article or dataset.",
    )
    organism_name: str = strawberry.field(
        description="Name of the organism from which a biological sample used in a CryoET study is derived from, e.g. homo sapiens.",
    )
    organism_taxid: Optional[int] = strawberry.field(
        description="NCBI taxonomy identifier for the organism, e.g. 9606",
        default=None,
    )
    tissue_name: Optional[str] = strawberry.field(
        description="Name of the tissue from which a biological sample used in a CryoET study is derived from.",
        default=None,
    )
    tissue_id: Optional[str] = strawberry.field(description="The UBERON identifier for the tissue.", default=None)
    cell_name: Optional[str] = strawberry.field(
        description="Name of the cell type from which a biological sample used in a CryoET study is derived from.",
        default=None,
    )
    cell_type_id: Optional[str] = strawberry.field(
        description="Cell Ontology identifier for the cell type",
        default=None,
    )
    cell_strain_name: Optional[str] = strawberry.field(description="Cell line or strain for the sample.", default=None)
    cell_strain_id: Optional[str] = strawberry.field(
        description="Link to more information about the cell strain.",
        default=None,
    )
    sample_type: Optional[sample_type_enum] = strawberry.field(
        description="Type of sample imaged in a CryoET study",
        default=None,
    )
    sample_preparation: Optional[str] = strawberry.field(
        description="Describes how the sample was prepared.",
        default=None,
    )
    grid_preparation: Optional[str] = strawberry.field(description="Describes Cryo-ET grid preparation.", default=None)
    other_setup: Optional[str] = strawberry.field(
        description="Describes other setup not covered by sample preparation or grid preparation that may make this dataset unique in the same publication.",
        default=None,
    )
    key_photo_url: Optional[str] = strawberry.field(description="URL for the dataset preview image.", default=None)
    key_photo_thumbnail_url: Optional[str] = strawberry.field(
        description="URL for the thumbnail of preview image.",
        default=None,
    )
    cell_component_name: Optional[str] = strawberry.field(description="Name of the cellular component.", default=None)
    cell_component_id: Optional[str] = strawberry.field(
        description="The GO identifier for the cellular component.",
        default=None,
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
    publications: Optional[str] = strawberry.field(
        description="Comma-separated list of DOIs for publications associated with the dataset.",
        default=None,
    )
    related_database_entries: Optional[str] = strawberry.field(
        description="Comma-separated list of related database entries for the dataset.",
        default=None,
    )
    related_database_links: Optional[str] = strawberry.field(
        description="Comma-separated list of related database links for the dataset.",
        default=None,
    )
    dataset_citations: Optional[str] = strawberry.field(
        description="Comma-separated list of DOIs for publications citing the dataset.",
        default=None,
    )
    s3_prefix: str = strawberry.field(description="Path to a directory containing data for this entity as an S3 url")
    https_prefix: str = strawberry.field(
        description="Path to a directory containing data for this entity as an HTTPS url",
    )
    id: int = strawberry.field(description="An identifier to refer to a specific instance of this type")


"""
We need to add this to each Queryable type so that strawberry will accept either our
Strawberry type *or* a SQLAlchemy model instance as a valid response class from a resolver
"""
Dataset.__strawberry_definition__.is_type_of = (  # type: ignore
    lambda obj, info: type(obj) == db.Dataset or type(obj) == Dataset
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
class DatasetNumericalColumns:
    organism_taxid: Optional[int] = None
    id: Optional[int] = None


"""
Define columns that support min/max aggregations
"""


@strawberry.type
class DatasetMinMaxColumns:
    title: Optional[str] = None
    description: Optional[str] = None
    organism_name: Optional[str] = None
    organism_taxid: Optional[int] = None
    tissue_name: Optional[str] = None
    tissue_id: Optional[str] = None
    cell_name: Optional[str] = None
    cell_type_id: Optional[str] = None
    cell_strain_name: Optional[str] = None
    cell_strain_id: Optional[str] = None
    sample_preparation: Optional[str] = None
    grid_preparation: Optional[str] = None
    other_setup: Optional[str] = None
    key_photo_url: Optional[str] = None
    key_photo_thumbnail_url: Optional[str] = None
    cell_component_name: Optional[str] = None
    cell_component_id: Optional[str] = None
    deposition_date: Optional[datetime.datetime] = None
    release_date: Optional[datetime.datetime] = None
    last_modified_date: Optional[datetime.datetime] = None
    publications: Optional[str] = None
    related_database_entries: Optional[str] = None
    related_database_links: Optional[str] = None
    dataset_citations: Optional[str] = None
    s3_prefix: Optional[str] = None
    https_prefix: Optional[str] = None
    id: Optional[int] = None


"""
Define enum of all columns to support count and count(distinct) aggregations
"""


@strawberry.enum
class DatasetCountColumns(enum.Enum):
    deposition = "deposition"
    fundingSources = "funding_sources"
    authors = "authors"
    runs = "runs"
    title = "title"
    description = "description"
    organismName = "organism_name"
    organismTaxid = "organism_taxid"
    tissueName = "tissue_name"
    tissueId = "tissue_id"
    cellName = "cell_name"
    cellTypeId = "cell_type_id"
    cellStrainName = "cell_strain_name"
    cellStrainId = "cell_strain_id"
    sampleType = "sample_type"
    samplePreparation = "sample_preparation"
    gridPreparation = "grid_preparation"
    otherSetup = "other_setup"
    keyPhotoUrl = "key_photo_url"
    keyPhotoThumbnailUrl = "key_photo_thumbnail_url"
    cellComponentName = "cell_component_name"
    cellComponentId = "cell_component_id"
    depositionDate = "deposition_date"
    releaseDate = "release_date"
    lastModifiedDate = "last_modified_date"
    publications = "publications"
    relatedDatabaseEntries = "related_database_entries"
    relatedDatabaseLinks = "related_database_links"
    datasetCitations = "dataset_citations"
    s3Prefix = "s3_prefix"
    httpsPrefix = "https_prefix"
    id = "id"


"""
All supported aggregation functions
"""


@strawberry.type
class DatasetAggregateFunctions:
    # This is a hack to accept "distinct" and "columns" as arguments to "count"
    @strawberry.field
    def count(self, distinct: Optional[bool] = False, columns: Optional[DatasetCountColumns] = None) -> Optional[int]:
        # Count gets set with the proper value in the resolver, so we just return it here
        return self.count  # type: ignore

    sum: Optional[DatasetNumericalColumns] = None
    avg: Optional[DatasetNumericalColumns] = None
    stddev: Optional[DatasetNumericalColumns] = None
    variance: Optional[DatasetNumericalColumns] = None
    min: Optional[DatasetMinMaxColumns] = None
    max: Optional[DatasetMinMaxColumns] = None
    groupBy: Optional[DatasetGroupByOptions] = None


"""
Wrapper around DatasetAggregateFunctions
"""


@strawberry.type
class DatasetAggregate:
    aggregate: Optional[list[DatasetAggregateFunctions]] = None


"""
------------------------------------------------------------------------------
Mutation types
------------------------------------------------------------------------------
"""


@strawberry.input()
class DatasetCreateInput:
    deposition_id: Optional[strawberry.ID] = strawberry.field(description=None, default=None)
    title: str = strawberry.field(description="Title of a CryoET dataset.")
    description: str = strawberry.field(
        description="A short description of a CryoET dataset, similar to an abstract for a journal article or dataset.",
    )
    organism_name: str = strawberry.field(
        description="Name of the organism from which a biological sample used in a CryoET study is derived from, e.g. homo sapiens.",
    )
    organism_taxid: Optional[int] = strawberry.field(
        description="NCBI taxonomy identifier for the organism, e.g. 9606",
        default=None,
    )
    tissue_name: Optional[str] = strawberry.field(
        description="Name of the tissue from which a biological sample used in a CryoET study is derived from.",
        default=None,
    )
    tissue_id: Optional[str] = strawberry.field(description="The UBERON identifier for the tissue.", default=None)
    cell_name: Optional[str] = strawberry.field(
        description="Name of the cell type from which a biological sample used in a CryoET study is derived from.",
        default=None,
    )
    cell_type_id: Optional[str] = strawberry.field(
        description="Cell Ontology identifier for the cell type",
        default=None,
    )
    cell_strain_name: Optional[str] = strawberry.field(description="Cell line or strain for the sample.", default=None)
    cell_strain_id: Optional[str] = strawberry.field(
        description="Link to more information about the cell strain.",
        default=None,
    )
    sample_type: Optional[sample_type_enum] = strawberry.field(
        description="Type of sample imaged in a CryoET study",
        default=None,
    )
    sample_preparation: Optional[str] = strawberry.field(
        description="Describes how the sample was prepared.",
        default=None,
    )
    grid_preparation: Optional[str] = strawberry.field(description="Describes Cryo-ET grid preparation.", default=None)
    other_setup: Optional[str] = strawberry.field(
        description="Describes other setup not covered by sample preparation or grid preparation that may make this dataset unique in the same publication.",
        default=None,
    )
    key_photo_url: Optional[str] = strawberry.field(description="URL for the dataset preview image.", default=None)
    key_photo_thumbnail_url: Optional[str] = strawberry.field(
        description="URL for the thumbnail of preview image.",
        default=None,
    )
    cell_component_name: Optional[str] = strawberry.field(description="Name of the cellular component.", default=None)
    cell_component_id: Optional[str] = strawberry.field(
        description="The GO identifier for the cellular component.",
        default=None,
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
    publications: Optional[str] = strawberry.field(
        description="Comma-separated list of DOIs for publications associated with the dataset.",
        default=None,
    )
    related_database_entries: Optional[str] = strawberry.field(
        description="Comma-separated list of related database entries for the dataset.",
        default=None,
    )
    related_database_links: Optional[str] = strawberry.field(
        description="Comma-separated list of related database links for the dataset.",
        default=None,
    )
    dataset_citations: Optional[str] = strawberry.field(
        description="Comma-separated list of DOIs for publications citing the dataset.",
        default=None,
    )
    s3_prefix: str = strawberry.field(description="Path to a directory containing data for this entity as an S3 url")
    https_prefix: str = strawberry.field(
        description="Path to a directory containing data for this entity as an HTTPS url",
    )
    id: int = strawberry.field(description="An identifier to refer to a specific instance of this type")


@strawberry.input()
class DatasetUpdateInput:
    deposition_id: Optional[strawberry.ID] = strawberry.field(description=None, default=None)
    title: Optional[str] = strawberry.field(description="Title of a CryoET dataset.")
    description: Optional[str] = strawberry.field(
        description="A short description of a CryoET dataset, similar to an abstract for a journal article or dataset.",
    )
    organism_name: Optional[str] = strawberry.field(
        description="Name of the organism from which a biological sample used in a CryoET study is derived from, e.g. homo sapiens.",
    )
    organism_taxid: Optional[int] = strawberry.field(
        description="NCBI taxonomy identifier for the organism, e.g. 9606",
        default=None,
    )
    tissue_name: Optional[str] = strawberry.field(
        description="Name of the tissue from which a biological sample used in a CryoET study is derived from.",
        default=None,
    )
    tissue_id: Optional[str] = strawberry.field(description="The UBERON identifier for the tissue.", default=None)
    cell_name: Optional[str] = strawberry.field(
        description="Name of the cell type from which a biological sample used in a CryoET study is derived from.",
        default=None,
    )
    cell_type_id: Optional[str] = strawberry.field(
        description="Cell Ontology identifier for the cell type",
        default=None,
    )
    cell_strain_name: Optional[str] = strawberry.field(description="Cell line or strain for the sample.", default=None)
    cell_strain_id: Optional[str] = strawberry.field(
        description="Link to more information about the cell strain.",
        default=None,
    )
    sample_type: Optional[sample_type_enum] = strawberry.field(
        description="Type of sample imaged in a CryoET study",
        default=None,
    )
    sample_preparation: Optional[str] = strawberry.field(
        description="Describes how the sample was prepared.",
        default=None,
    )
    grid_preparation: Optional[str] = strawberry.field(description="Describes Cryo-ET grid preparation.", default=None)
    other_setup: Optional[str] = strawberry.field(
        description="Describes other setup not covered by sample preparation or grid preparation that may make this dataset unique in the same publication.",
        default=None,
    )
    key_photo_url: Optional[str] = strawberry.field(description="URL for the dataset preview image.", default=None)
    key_photo_thumbnail_url: Optional[str] = strawberry.field(
        description="URL for the thumbnail of preview image.",
        default=None,
    )
    cell_component_name: Optional[str] = strawberry.field(description="Name of the cellular component.", default=None)
    cell_component_id: Optional[str] = strawberry.field(
        description="The GO identifier for the cellular component.",
        default=None,
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
    publications: Optional[str] = strawberry.field(
        description="Comma-separated list of DOIs for publications associated with the dataset.",
        default=None,
    )
    related_database_entries: Optional[str] = strawberry.field(
        description="Comma-separated list of related database entries for the dataset.",
        default=None,
    )
    related_database_links: Optional[str] = strawberry.field(
        description="Comma-separated list of related database links for the dataset.",
        default=None,
    )
    dataset_citations: Optional[str] = strawberry.field(
        description="Comma-separated list of DOIs for publications citing the dataset.",
        default=None,
    )
    s3_prefix: Optional[str] = strawberry.field(
        description="Path to a directory containing data for this entity as an S3 url",
    )
    https_prefix: Optional[str] = strawberry.field(
        description="Path to a directory containing data for this entity as an HTTPS url",
    )
    id: Optional[int] = strawberry.field(description="An identifier to refer to a specific instance of this type")


"""
------------------------------------------------------------------------------
Utilities
------------------------------------------------------------------------------
"""


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_datasets(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    authz_client: AuthzClient = Depends(get_authz_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[DatasetWhereClause] = None,
    order_by: Optional[list[DatasetOrderByClause]] = [],
    limit_offset: Optional[LimitOffsetClause] = None,
) -> typing.Sequence[Dataset]:
    """
    Resolve Dataset objects. Used for queries (see graphql_api/queries.py).
    """
    limit = limit_offset["limit"] if limit_offset and "limit" in limit_offset else None
    offset = limit_offset["offset"] if limit_offset and "offset" in limit_offset else None
    if offset and not limit:
        raise PlatformicsError("Cannot use offset without limit")
    return await get_db_rows(db.Dataset, session, authz_client, principal, where, order_by, AuthzAction.VIEW, limit, offset)  # type: ignore


def format_dataset_aggregate_output(query_results: Sequence[RowMapping] | RowMapping) -> DatasetAggregate:
    """
    Given a row from the DB containing the results of an aggregate query,
    format the results using the proper GraphQL types.
    """
    aggregate = []
    if type(query_results) is not list:
        query_results = [query_results]  # type: ignore
    for row in query_results:
        aggregate.append(format_dataset_aggregate_row(row))
    return DatasetAggregate(aggregate=aggregate)


def format_dataset_aggregate_row(row: RowMapping) -> DatasetAggregateFunctions:
    """
    Given a single row from the DB containing the results of an aggregate query,
    format the results using the proper GraphQL types.
    """
    output = DatasetAggregateFunctions()
    for key, value in row.items():
        # Key is either an aggregate function or a groupby key
        group_keys = key.split(".")
        aggregate = key.split("_", 1)
        if aggregate[0] not in aggregator_map.keys():
            # Turn list of groupby keys into nested objects
            if not output.groupBy:
                output.groupBy = DatasetGroupByOptions()
            group = build_dataset_groupby_output(output.groupBy, group_keys, value)
            output.groupBy = group
        else:
            aggregate_name = aggregate[0]
            if aggregate_name == "count":
                output.count = value
            else:
                aggregator_fn, col_name = aggregate[0], aggregate[1]
                if not getattr(output, aggregator_fn):
                    if aggregate_name in ["min", "max"]:
                        setattr(output, aggregator_fn, DatasetMinMaxColumns())
                    else:
                        setattr(output, aggregator_fn, DatasetNumericalColumns())
                setattr(getattr(output, aggregator_fn), col_name, value)
    return output


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_datasets_aggregate(
    info: Info,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    authz_client: AuthzClient = Depends(get_authz_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[DatasetWhereClause] = None,
    # TODO: add support for groupby, limit/offset
) -> DatasetAggregate:
    """
    Aggregate values for Dataset objects. Used for queries (see graphql_api/queries.py).
    """
    # Get the selected aggregate functions and columns to operate on, and groupby options if any were provided.
    # TODO: not sure why selected_fields is a list
    selections = info.selected_fields[0].selections[0].selections
    aggregate_selections = [selection for selection in selections if selection.name != "groupBy"]
    groupby_selections = [selection for selection in selections if selection.name == "groupBy"]
    groupby_selections = groupby_selections[0].selections if groupby_selections else []

    if not aggregate_selections:
        raise PlatformicsError("No aggregate functions selected")

    rows = await get_aggregate_db_rows(db.Dataset, session, authz_client, principal, where, aggregate_selections, [], groupby_selections)  # type: ignore
    aggregate_output = format_dataset_aggregate_output(rows)
    return aggregate_output


@strawberry.mutation(extensions=[DependencyExtension()])
async def create_dataset(
    input: DatasetCreateInput,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    authz_client: AuthzClient = Depends(get_authz_client),
    principal: Principal = Depends(require_auth_principal),
    is_system_user: bool = Depends(is_system_user),
) -> db.Dataset:
    """
    Create a new Dataset object. Used for mutations (see graphql_api/mutations.py).
    """
    validated = DatasetCreateInputValidator(**input.__dict__)
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
    new_entity = db.Dataset(**params)

    # Are we actually allowed to create this entity?
    if not authz_client.can_create(new_entity, principal):
        raise PlatformicsError("Unauthorized: Cannot create entity")

    session.add(new_entity)
    await session.commit()
    return new_entity


@strawberry.mutation(extensions=[DependencyExtension()])
async def update_dataset(
    input: DatasetUpdateInput,
    where: DatasetWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    authz_client: AuthzClient = Depends(get_authz_client),
    principal: Principal = Depends(require_auth_principal),
    is_system_user: bool = Depends(is_system_user),
) -> Sequence[db.Dataset]:
    """
    Update Dataset objects. Used for mutations (see graphql_api/mutations.py).
    """
    validated = DatasetUpdateInputValidator(**input.__dict__)
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
    entities = await get_db_rows(db.Dataset, session, authz_client, principal, where, [], AuthzAction.UPDATE)
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
async def delete_dataset(
    where: DatasetWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    authz_client: AuthzClient = Depends(get_authz_client),
    principal: Principal = Depends(require_auth_principal),
) -> Sequence[db.Dataset]:
    """
    Delete Dataset objects. Used for mutations (see graphql_api/mutations.py).
    """
    # Fetch entities for deletion, if we have access to them
    entities = await get_db_rows(db.Dataset, session, authz_client, principal, where, [], AuthzAction.DELETE)
    if len(entities) == 0:
        raise PlatformicsError("Unauthorized: Cannot delete entities")

    # Update DB
    for entity in entities:
        await session.delete(entity)
    await session.commit()
    return entities
