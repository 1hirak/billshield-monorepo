from __future__ import annotations

from decimal import Decimal

from app.core.constants import DIRECT_DEBIT_HEALTHY_MAX_DIFF, ConfidenceLevel, EffortLevel, SavingLabel, UrgencyLevel
from app.engines.ranking_engine import RecommendationCandidate
from app.models.bill import Bill


def check_direct_debit_health(  # noqa: C901
    bill: Bill | None,
) -> list[RecommendationCandidate]:
    if not bill or not bill.confirmed_fields_json:
        return _create_generic_dd_check()

    fields = bill.confirmed_fields_json
    monthly_dd = fields.get("monthlyDirectDebit")
    elec_unit = fields.get("electricityUnitRatePencePerKwh")
    gas_unit = fields.get("gasUnitRatePencePerKwh")
    elec_sc = fields.get("electricityStandingChargePencePerDay")
    gas_sc = fields.get("gasStandingChargePencePerDay")
    elec_usage = fields.get("annualElectricityUsageKwh")
    gas_usage = fields.get("annualGasUsageKwh")

    if not all([monthly_dd, elec_unit, gas_unit, elec_sc, gas_sc, elec_usage, gas_usage]):
        return _create_generic_dd_check()

    monthly_dd = Decimal(str(monthly_dd))
    elec_unit = Decimal(str(elec_unit))
    gas_unit = Decimal(str(gas_unit))
    elec_sc = Decimal(str(elec_sc))
    gas_sc = Decimal(str(gas_sc))
    elec_usage = int(elec_usage)
    gas_usage = int(gas_usage)

    annual_dd = monthly_dd * 12

    forecast_annual = (
        Decimal(elec_usage) * elec_unit / 100
        + Decimal(gas_usage) * gas_unit / 100
        + 365 * elec_sc / 100
        + 365 * gas_sc / 100
    )

    monthly_forecast = forecast_annual / 12
    monthly_difference = monthly_dd - monthly_forecast

    if monthly_difference >= DIRECT_DEBIT_HEALTHY_MAX_DIFF:
        return [
            RecommendationCandidate(
                engine_type="direct_debit_health_check",
                title="Request a Direct Debit review",
                description="Your Direct Debit appears higher than your forecast usage.",
                what_detected=f"Your monthly Direct Debit is £{int(monthly_dd)}, but your forecast usage suggests a monthly cost of around £{round(monthly_forecast)}.",
                why_it_matters="You may be building unnecessary credit with your supplier while your monthly budget is tight.",
                monthly_saving_pounds=Decimal(str(round(float(monthly_difference)))),
                annual_saving_pounds=Decimal(str(round(float(monthly_difference) * 12))),
                saving_label=SavingLabel.CASHFLOW_IMPROVEMENT,
                effort=EffortLevel.LOW,
                confidence=ConfidenceLevel.HIGH,
                urgency=UrgencyLevel.MEDIUM,
                next_step="Submit a meter reading, then ask your supplier to review your Direct Debit.",
                steps=[
                    "Submit an up-to-date meter reading.",
                    "Check whether your account is in credit.",
                    "Ask your supplier to recalculate your Direct Debit based on actual usage.",
                ],
            )
        ]

    if monthly_difference <= -DIRECT_DEBIT_HEALTHY_MAX_DIFF:
        return [
            RecommendationCandidate(
                engine_type="direct_debit_health_check",
                title="Your Direct Debit may be too low",
                description=f"Your monthly Direct Debit is £{int(monthly_dd)}, but your forecast usage suggests higher costs.",
                what_detected="Your Direct Debit appears below your forecast usage cost.",
                why_it_matters="This can lead to debt building up. A realistic payment plan can prevent a larger bill later.",
                monthly_saving_pounds=None,
                annual_saving_pounds=None,
                saving_label=SavingLabel.RISK_REDUCTION,
                effort=EffortLevel.LOW,
                confidence=ConfidenceLevel.HIGH,
                urgency=UrgencyLevel.HIGH,
                next_step="Contact your supplier to discuss a realistic payment plan based on actual usage.",
                steps=[
                    "Submit an up-to-date meter reading.",
                    "Ask your supplier to review your payment level.",
                    "Agree a plan that covers your usage without building debt.",
                ],
                call_script="I want to make sure my payments cover my usage so I don't build up debt. Can we review my Direct Debit?",
            )
        ]

    return []


def _create_generic_dd_check() -> list[RecommendationCandidate]:
    return [
        RecommendationCandidate(
            engine_type="direct_debit_health_check",
            title="Review your Direct Debit once your bill is confirmed",
            description="After confirming your bill details, we can check whether your Direct Debit matches your usage.",
            what_detected="You have a Direct Debit set up.",
            why_it_matters="Ensuring your Direct Debit matches your usage can prevent credit build-up or debt.",
            monthly_saving_pounds=None,
            annual_saving_pounds=None,
            saving_label=SavingLabel.CASHFLOW_IMPROVEMENT,
            effort=EffortLevel.LOW,
            confidence=ConfidenceLevel.NEEDS_REVIEW,
            urgency=UrgencyLevel.LOW,
            next_step="Confirm your bill details so we can check your Direct Debit.",
            steps=["Review and confirm your bill extraction."],
        ),
    ]
