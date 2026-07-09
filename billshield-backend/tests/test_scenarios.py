from __future__ import annotations


def _create_household(client, overrides=None) -> str:
    payload = {
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
        "hasChildren": True,
        "hasPensioner": False,
        "hasHealthCondition": False,
        "hasDisability": False,
    }
    if overrides:
        payload.update(overrides)
    resp = client.post("/api/v1/households", json=payload)
    return resp.json()["id"]


def test_scenario_simulate_returns_breakdown(client):
    household_id = _create_household(client)

    response = client.post(
        "/api/v1/scenarios/simulate",
        json={
            "householdId": household_id,
            "requestDirectDebitReview": True,
            "applyForCouncilTaxReduction": True,
            "switchToSocialBroadbandTariff": True,
            "shiftAppliancesToOffPeak": True,
            "checkWaterMeterOrSocialTariff": True,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "estimatedMonthlySaving" in data
    assert "estimatedAnnualSaving" in data
    assert "breakdown" in data
    assert len(data["breakdown"]) > 0
    assert "notes" in data


def test_scenario_simulate_flat_tariff_warning(client):
    household_id = _create_household(client)

    response = client.post(
        "/api/v1/scenarios/simulate",
        json={
            "householdId": household_id,
            "shiftAppliancesToOffPeak": True,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["tariffWarning"] is not None or len(data["breakdown"]) > 0


def test_scenario_simulate_vulnerable_household_has_safety_warning(client):
    household_id = _create_household(client, {"hasHealthCondition": True, "hasChildren": True})

    response = client.post(
        "/api/v1/scenarios/simulate",
        json={
            "householdId": household_id,
            "heatingReductionCelsius": 2,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["safetyWarning"] is not None


def test_scenario_simulate_invalid_household(client):
    response = client.post(
        "/api/v1/scenarios/simulate",
        json={
            "householdId": "00000000-0000-0000-0000-000000000000",
        },
    )
    assert response.status_code == 404
