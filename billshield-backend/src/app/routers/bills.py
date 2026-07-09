from __future__ import annotations

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.core.constants import BillType
from app.core.errors import HouseholdNotFoundError
from app.db.session import get_db
from app.repositories.household_repository import HouseholdRepository
from app.schemas.bill import ConfirmBillFieldsRequest
from app.services.bill_service import BillService

router = APIRouter(prefix="/bills", tags=["bills"])


@router.post("/upload")
async def upload_bill(
    household_id: str = Form(alias="householdId"),
    bill_type: str = Form(default="energy", alias="billType"),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    household_repo = HouseholdRepository(db)
    household = household_repo.get_by_id(household_id)
    if not household:
        raise HouseholdNotFoundError(household_id)

    try:
        bt = BillType(bill_type)
    except ValueError:
        bt = BillType.ENERGY

    service = BillService(db)
    return service.upload(household_id, file, bt)


@router.get("/{bill_id}")
def get_bill(bill_id: str, db: Session = Depends(get_db)):
    service = BillService(db)
    return service.get_extraction(bill_id)


@router.patch("/{bill_id}/confirm")
def confirm_bill(bill_id: str, data: ConfirmBillFieldsRequest, db: Session = Depends(get_db)):
    service = BillService(db)
    return service.confirm_fields(bill_id, data)


@router.delete("/{bill_id}/data")
def delete_bill_data(bill_id: str, db: Session = Depends(get_db)):
    service = BillService(db)
    return service.delete_data(bill_id)
