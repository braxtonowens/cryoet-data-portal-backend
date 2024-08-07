"""
Pydantic validator for AnnotationFile

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/validators/class_name.py.j2 instead.
"""

# ruff: noqa: E501 Line too long


from support.enums import annotation_file_source_enum

import typing
import datetime
import uuid

from pydantic import BaseModel, ConfigDict, Field, StringConstraints
from typing_extensions import Annotated


class AnnotationFileCreateInputValidator(BaseModel):
    # Pydantic stuff
    model_config = ConfigDict(from_attributes=True)
    alignment_id: Annotated[uuid.UUID | None, Field()]
    annotation_shape_id: Annotated[uuid.UUID | None, Field()]
    tomogram_voxel_spacing_id: Annotated[uuid.UUID | None, Field()]
    format: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
        ),
    ]
    s3_path: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
        ),
    ]
    https_path: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
        ),
    ]
    is_visualization_default: Annotated[bool | None, Field()]
    source: Annotated[annotation_file_source_enum | None, Field()]
    id: Annotated[int, Field()]


class AnnotationFileUpdateInputValidator(BaseModel):
    # Pydantic stuff
    model_config = ConfigDict(from_attributes=True)
    alignment_id: Annotated[uuid.UUID | None, Field()]
    annotation_shape_id: Annotated[uuid.UUID | None, Field()]
    tomogram_voxel_spacing_id: Annotated[uuid.UUID | None, Field()]
    format: Annotated[
        str | None,
        StringConstraints(
            strip_whitespace=True,
        ),
    ]
    s3_path: Annotated[
        str | None,
        StringConstraints(
            strip_whitespace=True,
        ),
    ]
    https_path: Annotated[
        str | None,
        StringConstraints(
            strip_whitespace=True,
        ),
    ]
    is_visualization_default: Annotated[bool | None, Field()]
    source: Annotated[annotation_file_source_enum | None, Field()]
    id: Annotated[int | None, Field()]
