from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.bill import Bill


class BillRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, bill: Bill) -> Bill:
        self.db.add(bill)
        self.db.commit()
        self.db.refresh(bill)
        return bill

    def get_by_id(self, bill_id: str) -> Bill | None:
        return self.db.query(Bill).filter(Bill.id == bill_id, Bill.deleted_at.is_(None)).first()

    def update(self, bill: Bill, **kwargs) -> Bill:
        for key, value in kwargs.items():
            if value is not None and hasattr(bill, key):
                setattr(bill, key, value)
        self.db.commit()
        self.db.refresh(bill)
        return bill

    def soft_delete(self, bill: Bill) -> Bill:
        bill.deleted_at = datetime.now(tz=timezone.utc)
        bill.status = bill.status  # preserve status for audit
        self.db.commit()
        self.db.refresh(bill)
        return bill

    def get_by_household(self, household_id: str) -> list[Bill]:
        return (
            self.db.query(Bill)
            .filter(Bill.household_id == household_id, Bill.deleted_at.is_(None))
            .order_by(Bill.created_at.desc())
            .all()
        )
