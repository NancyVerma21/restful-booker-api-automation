import pytest


@pytest.mark.regression
def test_created_booking_can_be_retrieved(
    api_session, api_base_url, created_booking
):
    response = api_session.get(
        f"{api_base_url}/booking/{created_booking['id']}",
        timeout=20,
    )

    assert response.status_code == 200
    body = response.json()
    assert body["firstname"] == created_booking["payload"]["firstname"]
    assert body["lastname"] == created_booking["payload"]["lastname"]


@pytest.mark.regression
def test_created_booking_can_be_updated(
    api_session, api_base_url, auth_token, created_booking
):
    updated_payload = dict(created_booking["payload"])
    updated_payload["firstname"] = "UpdatedAutomation"

    response = api_session.put(
        f"{api_base_url}/booking/{created_booking['id']}",
        json=updated_payload,
        headers={"Cookie": f"token={auth_token}"},
        timeout=20,
    )

    assert response.status_code == 200
    assert response.json()["firstname"] == "UpdatedAutomation"


@pytest.mark.regression
def test_created_booking_can_be_deleted(
    api_session, api_base_url, auth_token, created_booking
):
    response = api_session.delete(
        f"{api_base_url}/booking/{created_booking['id']}",
        headers={"Cookie": f"token={auth_token}"},
        timeout=20,
    )

    assert response.status_code in (200, 201)
    verify_response = api_session.get(
        f"{api_base_url}/booking/{created_booking['id']}",
        timeout=20,
    )
    assert verify_response.status_code == 404
