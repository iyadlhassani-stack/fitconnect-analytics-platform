from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_health_endpoint_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_root_endpoint_returns_service_info():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["service"] == "FitConnect Analytics Platform API"
    assert response.json()["status"] == "running"


def test_kpi_overview_endpoint_returns_data():
    response = client.get("/kpis/overview")

    assert response.status_code == 200
    assert "TOTAL_USERS" in response.json() or "total_users" in response.json()


def test_weekly_insights_endpoint_returns_data():
    response = client.get("/insights/weekly")

    assert response.status_code == 200
    assert "summary" in response.json()
    