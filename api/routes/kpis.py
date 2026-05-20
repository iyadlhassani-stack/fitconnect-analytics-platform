from fastapi import APIRouter, HTTPException

from api.services.sample_data_service import read_csv_records

router = APIRouter(prefix="/kpis", tags=["kpis"])


@router.get("/overview")
def get_kpi_overview() -> dict:
    try:
        records = read_csv_records("kpi_overview_sample.csv")
        return records[0] if records else {}
    except FileNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.get("/engagement")
def get_engagement_metrics() -> list[dict]:
    try:
        return read_csv_records("engagement_sample.csv")
    except FileNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.get("/revenue")
def get_revenue_metrics() -> list[dict]:
    try:
        return read_csv_records("revenue_sample.csv")
    except FileNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
        