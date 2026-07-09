from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.recommendation import Recommendation


class RecommendationRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_many(self, recommendations: list[Recommendation]) -> list[Recommendation]:
        self.db.add_all(recommendations)
        self.db.commit()
        for rec in recommendations:
            self.db.refresh(rec)
        return recommendations

    def get_by_household(self, household_id: str) -> list[Recommendation]:
        return (
            self.db.query(Recommendation)
            .filter(Recommendation.household_id == household_id)
            .order_by(Recommendation.rank.asc())
            .all()
        )

    def delete_by_household(self, household_id: str) -> None:
        self.db.query(Recommendation).filter(
            Recommendation.household_id == household_id
        ).delete()
        self.db.commit()

    def get_by_id(self, recommendation_id: str) -> Recommendation | None:
        return self.db.query(Recommendation).filter(Recommendation.id == recommendation_id).first()
