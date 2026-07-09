from __future__ import annotations


def test_create_household_success(client):
    response = client.post(
        "/api/v1/households",
        json={
            "postcode": "BS1 4ST",
            "householdType": "family_with_children",
            "incomeBand": "15k_25k",
            "energyProvider": "BrightSpark Energy",
            "paymentMethod": "direct_debit",
            "monthlyRentOrMortgage": 850,
            "monthlyFoodCost": 360,
            "monthlyTransportCost": 155,
            "monthlyCouncilTax": 168,
            "monthlyBroadbandMobileCost": 52,
            "monthlyWaterCost": 39,
            "receivesQualifyingBenefits": True,
            "hasChildren": True,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["postcode"] == "BS1 4ST"
    assert data["normalizedPostcode"] == "BS14ST"
    assert data["householdType"] == "family_with_children"
    assert "id" in data
    assert "createdAt" in data


def test_create_household_invalid_postcode(client):
    response = client.post(
        "/api/v1/households",
        json={
            "postcode": "INVALID",
            "householdType": "single_adult",
            "incomeBand": "15k_25k",
            "energyProvider": "Test Energy",
            "paymentMethod": "direct_debit",
            "monthlyRentOrMortgage": 500,
            "monthlyFoodCost": 200,
            "monthlyTransportCost": 100,
            "monthlyCouncilTax": 100,
            "monthlyBroadbandMobileCost": 30,
            "monthlyWaterCost": 25,
        },
    )
    assert response.status_code == 422


def test_create_household_invalid_income_band(client):
    response = client.post(
        "/api/v1/households",
        json={
            "postcode": "BS1 4ST",
            "householdType": "single_adult",
            "incomeBand": "unknown_band",
            "energyProvider": "Test Energy",
            "paymentMethod": "direct_debit",
            "monthlyRentOrMortgage": 500,
            "monthlyFoodCost": 200,
            "monthlyTransportCost": 100,
            "monthlyCouncilTax": 100,
            "monthlyBroadbandMobileCost": 30,
            "monthlyWaterCost": 25,
        },
    )
    assert response.status_code == 422


def test_create_household_missing_required_fields(client):
    response = client.post(
        "/api/v1/households",
        json={
            "postcode": "BS1 4ST",
        },
    )
    assert response.status_code == 422


def test_get_household(client):
    create_resp = client.post(
        "/api/v1/households",
        json={
            "postcode": "BS1 4ST",
            "householdType": "family_with_children",
            "incomeBand": "15k_25k",
            "energyProvider": "BrightSpark Energy",
            "paymentMethod": "direct_debit",
            "monthlyRentOrMortgage": 850,
            "monthlyFoodCost": 360,
            "monthlyTransportCost": 155,
            "monthlyCouncilTax": 168,
            "monthlyBroadbandMobileCost": 52,
            "monthlyWaterCost": 39,
        },
    )
    household_id = create_resp.json()["id"]

    response = client.get(f"/api/v1/households/{household_id}")
    assert response.status_code == 200
    assert response.json()["id"] == household_id


def test_get_household_not_found(client):
    response = client.get("/api/v1/households/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "HOUSEHOLD_NOT_FOUND"
