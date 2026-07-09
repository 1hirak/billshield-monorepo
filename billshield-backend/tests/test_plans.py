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


def test_30_day_plan_returns_required_sections(client):
    household_id, _ = _create_household_and_bill(client)

    response = client.post(
        "/api/v1/plans/30-day",
        json={
            "householdId": household_id,
            "tone": "supportive_practical",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "planId" in data
    assert "thisWeek" in data
    assert "nextTwoWeeks" in data
    assert "byDayThirty" in data
    assert "reassurance" in data
    assert "actions" in data
    assert data["thisWeek"]["title"] == "This week"
    assert data["nextTwoWeeks"]["title"] == "Next 2 weeks"
    assert data["byDayThirty"]["title"] == "By day 30"


def test_30_day_plan_invalid_household(client):
    response = client.post(
        "/api/v1/plans/30-day",
        json={
            "householdId": "00000000-0000-0000-0000-000000000000",
        },
    )
    assert response.status_code == 404
