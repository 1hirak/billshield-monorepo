from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import Field

from app.schemas.common import CamelModel


class ApiErrorDetail(CamelModel):
    code: str
    message: str
    details: dict[str, Any] = Field(default_factory=dict)


class ApiErrorResponse(CamelModel):
    error: ApiErrorDetail


class ActionStep(CamelModel):
    title: str | None = None
    description: str | None = None
    order: int | None = None
