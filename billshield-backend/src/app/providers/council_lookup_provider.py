from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass
class CouncilInfo:
    name: str
    website: str
    council_tax_reduction_page: str


class CouncilLookupProvider(Protocol):
    def get_council_for_postcode(self, postcode: str) -> CouncilInfo: ...
