import json
from pathlib import Path

import pytest
from jsonschema import validate


@pytest.mark.regression
def test_get_bookings_returns_list(api_session, api_base_url):
    response = api_session.get(f"{api_base_url}/booking", timeout=20)

    assert response.status_code == 200
    bookings = response.json()
    assert isinstance(bookings, list)

    if bookings:
        assert "bookingid" in bookings[0]


@pytest.mark.regression
def test_get_nonexistent_booking_returns_not_found(api_session, api_base_url):
    response = api_session.get(
        f"{api_base_url}/booking/999999999",
        timeout=20,
    )

    assert response.status_code == 404


@pytest.mark.regression
def test_create_booking_matches_response_schema(
    api_session, api_base_url, booking_payload
):
    schema_path = Path(__file__).resolve().parents[1] / "schemas"
    booking_schema = json.loads(
        (schema_path / "booking.json").read_text(encoding="utf-8-sig")
    )
    response_schema = json.loads(
        (schema_path / "booking_response_schema.json").read_text(
            encoding="utf-8-sig"
        )
    )

    # Resolve the referenced booking schema locally.
    response_schema["properties"]["booking"]["$ref"] = "#/definitions/booking"
    response_schema["definitions"] = {"booking": booking_schema}

    token_response = api_session.post(
        f"{api_base_url}/auth",
        json={"username": "admin", "password": "password123"},
        timeout=20,
    )
    assert token_response.status_code == 200
    token = token_response.json().get("token")
    assert token, "Authentication response did not contain a token"

    booking_id = None

    try:
        response = api_session.post(
            f"{api_base_url}/booking",
            json=booking_payload,
            timeout=20,
        )

        assert response.status_code == 200
        body = response.json()
        booking_id = body.get("bookingid")

        validate(instance=body, schema=response_schema)

        assert body["booking"]["firstname"] == booking_payload["firstname"]
        assert body["booking"]["lastname"] == booking_payload["lastname"]

    finally:
        # Delete only the booking created by this test.
        if booking_id is not None:
            api_session.delete(
                f"{api_base_url}/booking/{booking_id}",
                headers={"Cookie": f"token={token}"},
                timeout=20,
            )
