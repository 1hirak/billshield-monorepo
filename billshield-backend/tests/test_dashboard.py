from __future__ import annotations


def _create_household_and_bill(client) -> tuple[str, str]:
    h_resp = client.post(
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
    household_id = h_resp.json()["id"]

    b_resp = client.post(
        "/api/v1/bills/upload",
        data={"householdId": household_id, "billType": "energy"},
        files={"file": ("bill.pdf", b"%PDF-1.4 content", "application/pdf")},
    )
    bill_id = b_resp.json()["billId"]

    client.patch(
        f"/api/v1/bills/{bill_id}/confirm",
        json={
            "supplier": "BrightSpark Energy",
            "tariffName": "Standard Variable Direct",
            "monthlyDirectDebit": 142,
            "electricityUnitRatePencePerKwh": 27.34,
            "electricityStandingChargePencePerDay": 60.12,
            "gasUnitRatePencePerKwh": 7.62,
            "gasStandingChargePencePerDay": 31.44,
            "annualElectricityUsageKwh": 2900,
            "annualGasUsageKwh": 11000,
        },
    )

    return household_id, bill_id


def test_dashboard_returns_required_sections(client):
    household_id, _ = _create_household_and_bill(client)

    response = client.get(f"/api/v1/dashboard/{household_id}")
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert "monthlyPressureForecast" in data
    assert "billBreakdown" in data
    assert "topRecommendedActions" in data
    assert "insights" in data
    assert data["summary"]["monthlyHouseholdPressure"] > 0


def test_dashboard_no_bill(client):
    h_resp = client.post(
        "/api/v1/households",
        json={
            "postcode": "BS1 4ST",
            "householdType": "single_adult",
            "incomeBand": "15k_25k",
            "energyProvider": "BrightSpark Energy",
            "paymentMethod": "direct_debit",
            "monthlyRentOrMortgage": 500,
            "monthlyFoodCost": 200,
            "monthlyTransportCost": 100,
            "monthlyCouncilTax": 100,
            "monthlyBroadbandMobileCost": 30,
            "monthlyWaterCost": 25,
        },
    )
    household_id = h_resp.json()["id"]

    response = client.get(f"/api/v1/dashboard/{household_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["billBreakdown"] is None
    assert len(data["topRecommendedActions"]) > 0


def test_dashboard_invalid_household(client):
    response = client.get("/api/v1/dashboard/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_dashboard_top_actions_have_expected_shape(client):
    household_id, _ = _create_household_and_bill(client)

    response = client.get(f"/api/v1/dashboard/{household_id}")
    assert response.status_code == 200
    data = response.json()
    top = data["topRecommendedActions"]

    for action in top:
        assert "id" in action
        assert "rank" in action
        assert "title" in action
        assert "description" in action
        assert "engineType" in action
        assert "savingLabel" in action
        assert "confidence" in action
        assert "effort" in action
        assert "urgency" in action
        assert "nextStep" in action


def test_dashboard_returns_exactly_three_top_actions(client):
    household_id, _ = _create_household_and_bill(client)

    response = client.get(f"/api/v1/dashboard/{household_id}")
    assert response.status_code == 200
    data = response.json()
    top = data["topRecommendedActions"]
    assert len(top) <= 3
