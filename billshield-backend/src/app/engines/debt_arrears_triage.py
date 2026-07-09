from __future__ import annotations

from decimal import Decimal

from app.core.constants import (
    INCOME_BAND_MONTHLY_MAP,
    ConfidenceLevel,
    EffortLevel,
    SavingLabel,
    UrgencyLevel,
)
from app.engines.ranking_engine import RecommendationCandidate
from app.models.household import Household


def triage_debt_arrears(
    household: Household,
) -> list[RecommendationCandidate]:
    candidates: list[RecommendationCandidate] = []

    estimated_income = INCOME_BAND_MONTHLY_MAP.get(household.income_band, 1650)
    monthly_pressure = (
        float(household.monthly_rent_or_mortgage)
        + float(household.monthly_food_cost)
        + float(household.monthly_transport_cost)
        + float(household.monthly_council_tax)
        + float(household.monthly_broadband_mobile_cost)
        + float(household.monthly_water_cost)
        + 142
    )

    disposable = estimated_income - monthly_pressure

    if disposable < 0:
        candidates.append(
            RecommendationCandidate(
                engine_type="debt_arrears_triage",
                title="Prioritise essential bills",
                description=(
                    "Your estimated monthly costs appear higher than your estimated income. "
                    "Prioritise rent/mortgage, council tax, and energy as the highest-consequence bills."
                ),
                what_detected="Your estimated monthly outgoings exceed your estimated income.",
                why_it_matters="Some bills have more serious consequences than others if unpaid.",
                monthly_saving_pounds=None,
                annual_saving_pounds=None,
                saving_label=SavingLabel.RISK_REDUCTION,
                effort=EffortLevel.MEDIUM,
                confidence=ConfidenceLevel.HIGH,
                urgency=UrgencyLevel.HIGH,
                next_step="Contact your priority bill providers and your local Citizens Advice.",
                steps=[
                    "Priority 1: Rent or mortgage. Contact your landlord or lender if you cannot pay.",
                    "Priority 2: Council tax. Ask about Council Tax Reduction or a payment plan.",
                    "Priority 3: Energy. Contact your supplier about an affordable repayment plan.",
                    "Contact Citizens Advice or a free debt advice service for support.",
                    "Do not ignore these bills — consequences can include eviction, court action, or disconnection.",
                ],
                call_script="I'm struggling to pay. I want to agree an affordable repayment plan based on my income and essential costs.",
            )
        )

    if disposable < 200:
        candidates.append(
            RecommendationCandidate(
                engine_type="debt_arrears_triage",
                title="Contact free debt advice",
                description="Free, confidential debt advice is available from organisations like StepChange and Citizens Advice.",
                what_detected="Your monthly budget looks tight with a small financial buffer.",
                why_it_matters="Early debt advice can prevent problems getting worse.",
                monthly_saving_pounds=None,
                annual_saving_pounds=None,
                saving_label=SavingLabel.RISK_REDUCTION,
                effort=EffortLevel.MEDIUM,
                confidence=ConfidenceLevel.HIGH,
                urgency=UrgencyLevel.MEDIUM,
                next_step="Contact StepChange or Citizens Advice for free guidance.",
                steps=[
                    "Call StepChange on 0800 138 1111 or visit stepchange.org.",
                    "Or contact Citizens Advice on 0800 144 8848.",
                    "Both are free, confidential, and will not judge your situation.",
                ],
                safety_caveat="BillShield does not provide regulated debt advice. Always speak to a qualified adviser for serious debt concerns.",
            )
        )

    return candidates
