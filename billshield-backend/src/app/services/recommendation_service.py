from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.errors import HouseholdNotFoundError, RecommendationNotFoundError
from app.repositories.household_repository import HouseholdRepository
from app.repositories.recommendation_repository import RecommendationRepository


class RecommendationService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.household_repo = HouseholdRepository(db)
        self.rec_repo = RecommendationRepository(db)

    def get_for_household(self, household_id: str) -> dict:
        household = self.household_repo.get_by_id(household_id)
        if not household:
            raise HouseholdNotFoundError(household_id)

        recommendations = self.rec_repo.get_by_household(household_id)
        if not recommendations:
            raise RecommendationNotFoundError(household_id)

        formatted = []
        for rec in recommendations:
            steps = []
            if rec.steps_json and isinstance(rec.steps_json, dict):
                steps = rec.steps_json.get("steps", [])

            formatted.append({
                "id": str(rec.id),
                "householdId": str(rec.household_id),
                "engineType": rec.engine_type.value,
                "rank": rec.rank,
                "title": rec.title,
                "description": rec.description,
                "whatDetected": rec.what_detected,
                "whyItMatters": rec.why_it_matters,
                "monthlySavingPounds": float(rec.monthly_saving_pounds) if rec.monthly_saving_pounds else None,
                "annualSavingPounds": float(rec.annual_saving_pounds) if rec.annual_saving_pounds else None,
                "savingLabel": rec.saving_label.value,
                "effort": rec.effort.value,
                "confidence": rec.confidence.value,
                "urgency": rec.urgency.value,
                "safetyRisk": rec.safety_risk.value,
                "eligibilityCaveat": rec.eligibility_caveat,
                "safetyCaveat": rec.safety_caveat,
                "nextStep": rec.next_step,
                "steps": steps,
                "callScript": rec.call_script,
                "ctaLabel": "View steps",
                "status": rec.status.value,
            })

        return {
            "householdId": household_id,
            "recommendations": formatted,
            "topCount": len(formatted),
            "totalCount": len(formatted),
        }
