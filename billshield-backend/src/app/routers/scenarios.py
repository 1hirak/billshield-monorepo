from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.scenario import SimulateScenarioRequest, ScenarioSimulationResponse
from app.services.scenario_service import ScenarioService

router = APIRouter(prefix="/scenarios", tags=["scenarios"])


@router.post("/simulate", response_model=ScenarioSimulationResponse)
def simulate_scenario(data: SimulateScenarioRequest, db: Session = Depends(get_db)):
    service = ScenarioService(db)
    return service.simulate(data)  # type: ignore[return-value]
