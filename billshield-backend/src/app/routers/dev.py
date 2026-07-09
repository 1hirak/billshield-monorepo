from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.data.mock_seed import reset_demo_data, seed_demo_data
from app.db.session import get_db

router = APIRouter(prefix="/dev", tags=["dev"])


def _check_dev():
    if not settings.is_development:
        raise HTTPException(status_code=404, detail="Not found")


@router.post("/seed")
def seed_data(db: Session = Depends(get_db)):
    _check_dev()
    return seed_demo_data(db)


@router.post("/reset")
def reset_data(db: Session = Depends(get_db)):
    _check_dev()
    return reset_demo_data(db)
