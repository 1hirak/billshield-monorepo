from __future__ import annotations

PLAN_TEMPLATES: dict[str, dict] = {
    "default": {
        "this_week": {
            "title": "This week",
            "items": [
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
                    "id": "direct_debit_review",
                    "title": "Check your Direct Debit amount",
                    "description": "Your payment may be higher than your forecast usage. Ask for a review after submitting a meter reading.",
                    "estimatedSavingPounds": 22,
                    "savingLabel": "cashflow_improvement",
                    "effort": "low",
                    "done": False,
                },
                {
                    "id": "council_tax_support",
                    "title": "Review Council Tax Reduction eligibility",
                    "description": "Your income band and household profile suggest this is worth checking.",
                    "estimatedSavingPounds": 35,
                    "savingLabel": "potential_saving",
                    "effort": "medium",
                    "done": False,
                },
            ],
        },
        "next_two_weeks": {
            "title": "Next 2 weeks",
            "items": [
                {
                    "id": "supplier_repayment_plan",
                    "title": "Contact supplier about an affordable repayment plan if needed",
                    "description": "If arrears are building, ask for a plan based on income and essential costs.",
                    "estimatedSavingPounds": None,
                    "savingLabel": "risk_reduction",
                    "effort": "medium",
                    "done": False,
                    "callScript": "I'm struggling to pay. I want to agree an affordable repayment plan based on my income and essential costs.",
                },
                {
                    "id": "broadband_social_tariff",
                    "title": "Check broadband social tariff",
                    "description": "Some households on qualifying benefits can access cheaper broadband packages.",
                    "estimatedSavingPounds": 18,
                    "savingLabel": "potential_saving",
                    "effort": "low",
                    "done": False,
                },
                {
                    "id": "local_support_service",
                    "title": "Visit a local support service if pressure is high",
                    "description": "Local advice services can help with benefits, debt, food support, and emergency council help.",
                    "estimatedSavingPounds": None,
                    "savingLabel": "support_access",
                    "effort": "medium",
                    "done": False,
                },
            ],
        },
        "by_day_thirty": {
            "title": "By day 30",
            "items": [
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
        "tone": "supportive_practical",
        "reassurance": "You do not have to do everything at once. Start with the first low-effort action and return when you are ready.",
    }
}
