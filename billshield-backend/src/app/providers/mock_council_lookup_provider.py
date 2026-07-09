from __future__ import annotations

from app.providers.council_lookup_provider import CouncilInfo, CouncilLookupProvider


class MockCouncilLookupProvider(CouncilLookupProvider):
    def get_council_for_postcode(self, postcode: str) -> CouncilInfo:
        area = postcode[:2].upper()
        return CouncilInfo(
            name=f"{area} City Council",
            website=f"https://{area.lower()}.gov.uk",
            council_tax_reduction_page=f"https://{area.lower()}.gov.uk/council-tax-reduction",
        )
