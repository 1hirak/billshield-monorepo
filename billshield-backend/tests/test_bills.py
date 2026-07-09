from __future__ import annotations


def _create_household(client) -> str:
    resp = client.post(
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
    return resp.json()["id"]


def test_upload_bill_success(client):
    household_id = _create_household(client)

    response = client.post(
        "/api/v1/bills/upload",
        data={"householdId": household_id, "billType": "energy"},
        files={"file": ("bill.pdf", b"%PDF-1.4 mock pdf content", "application/pdf")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "extracted"
    assert "billId" in data
    assert "extractionSummary" in data


def test_upload_bill_unsupported_type(client):
    household_id = _create_household(client)

    response = client.post(
        "/api/v1/bills/upload",
        data={"householdId": household_id, "billType": "energy"},
        files={"file": ("bill.txt", b"not a bill", "text/plain")},
    )
    assert response.status_code == 415


def test_upload_bill_invalid_household(client):
    response = client.post(
        "/api/v1/bills/upload",
        data={"householdId": "00000000-0000-0000-0000-000000000000", "billType": "energy"},
        files={"file": ("bill.pdf", b"%PDF-1.4 content", "application/pdf")},
    )
    assert response.status_code == 404


def test_get_bill_extraction(client):
    household_id = _create_household(client)
    upload_resp = client.post(
        "/api/v1/bills/upload",
        data={"householdId": household_id, "billType": "energy"},
        files={"file": ("bill.pdf", b"%PDF-1.4 content", "application/pdf")},
    )
    bill_id = upload_resp.json()["billId"]

    response = client.get(f"/api/v1/bills/{bill_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "extracted"
    assert data["extraction"] is not None
    assert data["reviewWarning"] is not None


def test_confirm_bill_fields(client):
    household_id = _create_household(client)
    upload_resp = client.post(
        "/api/v1/bills/upload",
        data={"householdId": household_id, "billType": "energy"},
        files={"file": ("bill.pdf", b"%PDF-1.4 content", "application/pdf")},
    )
    bill_id = upload_resp.json()["billId"]

    response = client.patch(
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
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "confirmed"


def test_delete_bill_data(client):
    household_id = _create_household(client)
    upload_resp = client.post(
        "/api/v1/bills/upload",
        data={"householdId": household_id, "billType": "energy"},
        files={"file": ("bill.pdf", b"%PDF-1.4 content", "application/pdf")},
    )
    bill_id = upload_resp.json()["billId"]

    response = client.delete(f"/api/v1/bills/{bill_id}/data")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "deleted"
