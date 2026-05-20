from fastapi import APIRouter, HTTPException

from api.services.sample_data_service import read_json

router = APIRouter(prefix="/insights", tags=["insights"])


@router.get("/weekly")
def get_weekly_insights() -> dict:
    try:
        return read_json("ai_weekly_insights_sample.json")
    except FileNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error

        