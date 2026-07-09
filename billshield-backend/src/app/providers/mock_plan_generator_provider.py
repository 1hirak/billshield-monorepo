from __future__ import annotations

from app.models.household import Household
from app.models.recommendation import Recommendation
from app.providers.plan_generator_provider import GeneratedPlan, PlanGeneratorProvider


class MockPlanGeneratorProvider(PlanGeneratorProvider):
    def generate_plan(
        self,
        household: Household,
        recommendations: list[Recommendation],
    ) -> GeneratedPlan:
        sorted_recs = sorted(
            [r for r in recommendations if r.rank],
            key=lambda r: r.rank,
        )

        this_week_items = []
        next_two_weeks_items = []
        by_day_thirty_items = []

        for i, rec in enumerate(sorted_recs):
            item = {
                "id": rec.engine_type.value if hasattr(rec.engine_type, "value") else str(rec.engine_type),
                "title": rec.title,
                "description": rec.next_step,
                "estimatedSavingPounds": float(rec.monthly_saving_pounds) if rec.monthly_saving_pounds else None,
                "savingLabel": rec.saving_label.value if hasattr(rec.saving_label, "value") else str(rec.saving_label),
                "effort": rec.effort.value if hasattr(rec.effort, "value") else str(rec.effort),
                "done": False,
            }
            if rec.call_script:
                item["callScript"] = rec.call_script

            if i < 3:
                this_week_items.append(item)
            elif i < 6:
                next_two_weeks_items.append(item)
            else:
                by_day_thirty_items.append(item)

        if len(this_week_items) < 3:
            fallback = [
                {
                    "id": "submit_meter_reading",
                    "title": "Submit a meter reading",
                    "description": "Send your latest gas and electricity readings so your supplier can bill actual usage.",
                    "estimatedSavingPounds": None,
                    "savingLabel": "billing_accuracy",
                    "effort": "low",
                    "done": False,
                },
                {
                    "id": "check_priority_services",
                    "title": "Check Priority Services Register",
                    "description": "If you or someone in your household has a health condition, disability, or is of pension age, you may be able to join your supplier's Priority Services Register.",
                    "estimatedSavingPounds": None,
                    "savingLabel": "support_access",
                    "effort": "low",
                    "done": False,
                },
            ]
            for fb in fallback:
                if len(this_week_items) < 3 and not any(
                    item["id"] == fb["id"] for item in this_week_items
                ):
                    this_week_items.append(fb)

        return GeneratedPlan(
            title="Your 30-day bill survival plan",
            intro=(
                "This plan focuses on practical steps that may reduce pressure this month. "
                "Start with the actions that are low effort or time-sensitive."
            ),
            this_week={"title": "This week", "items": this_week_items},
            next_two_weeks={"title": "Next 2 weeks", "items": next_two_weeks_items},
            by_day_thirty={
                "title": "By day 30",
                "items": by_day_thirty_items + [
                    {
                        "id": "compare_tariff_options",
                        "title": "Compare tariff options",
                        "description": "Check whether a cheaper fixed or variable tariff is available for your usage profile.",
                        "estimatedSavingPounds": None,
                        "savingLabel": "potential_saving",
                        "effort": "medium",
                        "done": False,
                    },
                    {
                        "id": "apply_for_eligible_support",
                        "title": "Apply for eligible support",
                        "description": "Complete applications for any support routes you confirmed you may qualify for.",
                        "estimatedSavingPounds": None,
                        "savingLabel": "potential_saving",
                        "effort": "medium",
                        "done": False,
                    },
                    {
                        "id": "review_budget_pressure",
                        "title": "Review household budget pressure",
                        "description": "Check whether your monthly buffer has improved after completed actions.",
                        "estimatedSavingPounds": None,
                        "savingLabel": "planning",
                        "effort": "low",
                        "done": False,
                    },
                ],
            },
            tone="supportive_practical",
            reassurance=(
                "You do not have to do everything at once. Start with the first low-effort "
                "action and return when you are ready."
            ),
        )
