"""
Pydantic validator for Pet

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/validators/class_name.py.j2 instead.
"""

# ruff: noqa: E501 Line too long


import uuid

from pydantic import BaseModel, ConfigDict, Field, StringConstraints
from typing_extensions import Annotated


class PetCreateInputValidator(BaseModel):
    # Pydantic stuff
    model_config = ConfigDict(from_attributes=True)
    name: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
        ),
    ]
    owner_id: Annotated[uuid.UUID | None, Field()]


class PetUpdateInputValidator(BaseModel):
    # Pydantic stuff
    model_config = ConfigDict(from_attributes=True)
    name: Annotated[
        str | None,
        StringConstraints(
            strip_whitespace=True,
        ),
    ]
    owner_id: Annotated[uuid.UUID | None, Field()]
