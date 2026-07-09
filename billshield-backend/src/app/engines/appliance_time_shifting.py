from __future__ import annotations

from decimal import Decimal

from app.core.constants import ConfidenceLevel, EffortLevel, SavingLabel, UrgencyLevel
from app.engines.ranking_engine import RecommendationCandidate
from app.models.bill import Bill


def check_appliance_time_shifting(
    bill: Bill | None,
) -> list[RecommendationCandidate]:
    if not bill or not bill.confirmed_fields_json:
        return _create_generic_appliance_advice()

    fields = bill.confirmed_fields_json
    tariff_type = fields.get("tariffType", "standard_variable")

    if tariff_type in ("fixed", "standard_variable", "prepayment", "other"):
        return [
            RecommendationCandidate(
                engine_type="appliance_time_shifting",
                title="Shift appliance use to off-peak windows",
                description="This only saves money on Economy 7, time-of-use, EV, battery, or smart off-peak tariffs.",
                what_detected="You are on a flat-rate tariff where the unit price is the same at all times of day.",
                why_it_matters="On flat tariffs, shifting appliance use may be greener but not cheaper.",
                monthly_saving_pounds=None,
                annual_saving_pounds=None,
                saving_label=SavingLabel.GREEN_ONLY,
                effort=EffortLevel.LOW,
                confidence=ConfidenceLevel.HIGH,
                urgency=UrgencyLevel.LOW,
                safety_risk=None,
                eligibility_caveat="On flat tariffs, this may be greener but not cheaper.",
                next_step="Check whether your tariff has cheaper off-peak rates.",
                steps=[
                    "Look at your tariff details to see if you have different day and night rates.",
                    "If you have an off-peak rate, programme your dishwasher, washing machine, and other high-use appliances for off-peak times.",
                ],
            ),
        ]

    return [
        RecommendationCandidate(
            engine_type="appliance_time_shifting",
            title="Shift heavy appliance use to off-peak hours",
            description=f"Your {tariff_type} tariff may have cheaper off-peak rates for running appliances.",
            what_detected=f"You are on a {tariff_type} tariff.",
            why_it_matters="Off-peak rates can be significantly cheaper, reducing your electricity costs.",
            monthly_saving_pounds=Decimal("7"),
            annual_saving_pounds=Decimal("84"),
            saving_label=SavingLabel.POTENTIAL_SAVING,
            effort=EffortLevel.LOW,
            confidence=ConfidenceLevel.MEDIUM,
            urgency=UrgencyLevel.LOW,
            safety_risk=None,
            eligibility_caveat="Check your tariff off-peak hours before shifting appliance use.",
            next_step="Check your off-peak hours and programme appliances for these times.",
            steps=[
                "Find your off-peak hours from your bill or supplier.",
                "Use timers or delay-start features on washing machines and dishwashers.",
                "Avoid running appliances overnight if there is a fire or safety risk.",
            ],
        ),
    ]


def _create_generic_appliance_advice() -> list[RecommendationCandidate]:
    return [
        RecommendationCandidate(
            engine_type="appliance_time_shifting",
            title="Check if off-peak appliance use could save money",
            description="Once your tariff details are confirmed, we can check whether off-peak use saves you money.",
            what_detected="Your tariff details have not been confirmed.",
            why_it_matters="Off-peak rates only save money if your tariff has different day and night prices.",
            monthly_saving_pounds=None,
            annual_saving_pounds=None,
            saving_label=SavingLabel.GREEN_ONLY,
            effort=EffortLevel.LOW,
            confidence=ConfidenceLevel.NEEDS_REVIEW,
            urgency=UrgencyLevel.LOW,
            next_step="Confirm your bill details so we can check your tariff type.",
            steps=["Review and confirm your bill extraction."],
        ),
    ]
