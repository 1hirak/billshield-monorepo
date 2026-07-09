from __future__ import annotations

from typing import TypeVar

from pydantic import BaseModel, ConfigDict


def to_camel(snake_str: str) -> str:
    first, *rest = snake_str.split("_")
    return first + "".join(word.capitalize() for word in rest)


class CamelModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
        str_strip_whitespace=True,
    )


T = TypeVar("T", bound=CamelModel)
