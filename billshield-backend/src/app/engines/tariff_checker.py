from __future__ import annotations

from decimal import Decimal

from app.core.constants import (
    BENCHMARK_TARIFF_THRESHOLD_PCT,
    TARIFF_HIGH_THRESHOLD_PCT,
    ConfidenceLevel,
    EffortLevel,
    SavingLabel,
    UrgencyLevel,
)
from app.engines.ranking_engine import RecommendationCandidate
from app.models.bill import Bill
from app.models.household import Household
from app.providers.mock_tariff_benchmark_provider import MockTariffBenchmarkProvider
from app.providers.tariff_benchmark_provider import TariffBenchmarkProvider


def check_tariff(
    household: Household,
    bill: Bill | None,
    tariff_provider: TariffBenchmarkProvider | None = None,
) -> list[RecommendationCandidate]:
    if tariff_provider is None:
        tariff_provider = MockTariffBenchmarkProvider()

    benchmark = tariff_provider.get_benchmark(household.postcode, household.payment_method)

    if not bill or not bill.confirmed_fields_json:
        return _create_generic_tariff_check(benchmark)

    fields = bill.confirmed_fields_json
    candidates: list[RecommendationCandidate] = []

    elec_rate = fields.get("electricityUnitRatePencePerKwh")
    gas_rate = fields.get("gasUnitRatePencePerKwh")
    elec_sc = fields.get("electricityStandingChargePencePerDay")
    gas_sc = fields.get("gasStandingChargePencePerDay")

    above_benchmark = False
    high_above = False

    if elec_rate:
        user_rate = Decimal(str(elec_rate))
        bench_rate = benchmark.electricity_unit_rate_pence_per_kwh
        if user_rate > bench_rate * (1 + Decimal(str(BENCHMARK_TARIFF_THRESHOLD_PCT)) / 100):
            above_benchmark = True
        if user_rate > bench_rate * (1 + Decimal(str(TARIFF_HIGH_THRESHOLD_PCT)) / 100):
            high_above = True

    if gas_rate:
        user_rate = Decimal(str(gas_rate))
        bench_rate = benchmark.gas_unit_rate_pence_per_kwh
        if user_rate > bench_rate * (1 + Decimal(str(BENCHMARK_TARIFF_THRESHOLD_PCT)) / 100):
            above_benchmark = True
        if user_rate > bench_rate * (1 + Decimal(str(TARIFF_HIGH_THRESHOLD_PCT)) / 100):
            high_above = True

    if above_benchmark:
        candidate = RecommendationCandidate(
            engine_type="tariff_check",
            title="Check whether a cheaper tariff is available",
            description="Your tariff appears above the benchmark for your profile. Check fixed deals or ask your supplier whether a cheaper tariff is available.",
            what_detected="Your energy unit rates appear above current benchmark rates for your payment method.",
            why_it_matters="A cheaper tariff could reduce your annual bill without changing your energy use.",
            monthly_saving_pounds=Decimal("15") if not high_above else Decimal("25"),
            annual_saving_pounds=Decimal("180") if not high_above else Decimal("300"),
            saving_label=SavingLabel.POTENTIAL_SAVING,
            effort=EffortLevel.MEDIUM,
            confidence=ConfidenceLevel.MEDIUM if high_above else ConfidenceLevel.LOW,
            urgency=UrgencyLevel.HIGH if high_above else UrgencyLevel.MEDIUM,
            next_step="Compare tariffs on your supplier's website or check a few comparison sites.",
            steps=[
                "Check your current tariff end date and any exit fees.",
                "Look at fixed and variable tariffs for your usage level.",
                "Use a comparison tool to find cheaper options.",
                "Ask your current supplier if they can offer a better rate.",
            ],
            eligibility_caveat="Actual tariffs vary by region, meter type, payment method, and supplier.",
        )
        candidates.append(candidate)

    return candidates


def _create_generic_tariff_check(benchmark) -> list[RecommendationCandidate]:
    candidate = RecommendationCandidate(
        engine_type="tariff_check",
        title="Check your energy tariff",
        description="Once your bill details are confirmed, we can compare your tariff against current market rates.",
        what_detected="Your tariff details have not been confirmed yet.",
        why_it_matters="Comparing tariffs can help you find a cheaper deal.",
        monthly_saving_pounds=None,
        annual_saving_pounds=None,
        saving_label=SavingLabel.POTENTIAL_SAVING,
        effort=EffortLevel.LOW,
        confidence=ConfidenceLevel.NEEDS_REVIEW,
        urgency=UrgencyLevel.LOW,
        next_step="Confirm your bill details so we can check your tariff.",
        steps=["Review and confirm your bill extraction.", "We will then compare against benchmark rates."],
    )
    return [candidate]
