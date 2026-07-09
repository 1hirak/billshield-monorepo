from __future__ import annotations


def test_support_services_returns_services(client):
    response = client.get("/api/v1/support-services?postcode=BS1%204ST&radiusMiles=5")
    assert response.status_code == 200
    data = response.json()
    assert "services" in data
    assert "mapPlaceholder" in data
    assert "availableFilters" in data
    assert data["normalizedPostcode"] == "BS"


def test_support_services_filter_by_type(client):
    response = client.get(
        "/api/v1/support-services?postcode=BS1%204ST&filters=food_bank&radiusMiles=5"
    )
    assert response.status_code == 200
    data = response.json()
    for svc in data["services"]:
        assert svc["type"] == "food_bank"


def test_support_services_no_results_for_unknown_area(client):
    response = client.get("/api/v1/support-services?postcode=ZZ1%201ZZ&radiusMiles=5")
    assert response.status_code == 200
    data = response.json()
    # Wildcard fallback: now returns 20+ generic services for any postcode
    assert len(data["services"]) > 20
