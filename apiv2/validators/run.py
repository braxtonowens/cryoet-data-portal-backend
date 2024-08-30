"""
Pydantic validator for Run

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/validators/class_name.py.j2 instead.
"""

# ruff: noqa: E501 Line too long


import uuid

from pydantic import BaseModel, ConfigDict, Field, StringConstraints
from typing_extensions import Annotated


class RunCreateInputValidator(BaseModel):
    # Pydantic stuff
    model_config = ConfigDict(from_attributes=True)
    dataset_id: Annotated[uuid.UUID, Field()]
    name: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
        ),
    ]
    s3_prefix: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
        ),
    ]
    https_prefix: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
        ),
    ]
    id: Annotated[int, Field()]


class RunUpdateInputValidator(BaseModel):
    # Pydantic stuff
    model_config = ConfigDict(from_attributes=True)
    dataset_id: Annotated[uuid.UUID | None, Field()]
    name: Annotated[
        str | None,
        StringConstraints(
            strip_whitespace=True,
        ),
    ]
    s3_prefix: Annotated[
        str | None,
        StringConstraints(
            strip_whitespace=True,
        ),
    ]
    https_prefix: Annotated[
        str | None,
        StringConstraints(
            strip_whitespace=True,
        ),
    ]
    id: Annotated[int | None, Field()]