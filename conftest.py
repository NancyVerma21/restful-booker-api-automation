import os

import pytest
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv(
    "BASE_URL", "https://restful-booker.herokuapp.com"
).rstrip("/")
API_USERNAME = os.getenv("API_USERNAME", "admin")
API_PASSWORD = os.getenv("API_PASSWORD", "password123")


@pytest.fixture
def api_base_url():
    return BASE_URL


@pytest.fixture
def api_session():
    session = requests.Session()
    session.headers.update({"Accept": "application/json"})
    yield session
    session.close()


@pytest.fixture
def auth_token(api_session, api_base_url):
    response = api_session.post(
        f"{api_base_url}/auth",
        json={"username": API_USERNAME, "password": API_PASSWORD},
        timeout=20,
    )
    assert response.status_code == 200, (
        f"Authentication request failed: {response.status_code} "
        f"{response.text}"
    )
    token = response.json().get("token")
    assert token, f"Authentication response did not contain a token: {response.text}"
    return token


@pytest.fixture
def booking_payload():
    import random
    from datetime import date, timedelta

    checkin = date.today() + timedelta(days=7)
    checkout = checkin + timedelta(days=4)

    return {
        "firstname": "Automation",
        "lastname": f"Tester{random.randint(1000, 9999)}",
        "totalprice": random.randint(100, 5000),
        "depositpaid": True,
        "bookingdates": {
            "checkin": checkin.isoformat(),
            "checkout": checkout.isoformat(),
        },
        "additionalneeds": "Breakfast",
    }


@pytest.fixture
def created_booking(api_session, api_base_url, auth_token, booking_payload):
    response = api_session.post(
        f"{api_base_url}/booking",
        json=booking_payload,
        timeout=20,
    )
    assert response.status_code == 200, (
        f"Booking creation failed: {response.status_code} {response.text}"
    )

    body = response.json()
    booking_id = body.get("bookingid")
    assert booking_id is not None, f"No booking ID in response: {body}"

    yield {"id": booking_id, "payload": booking_payload}

    # Clean up only the booking created by this test.
    try:
        api_session.delete(
            f"{api_base_url}/booking/{booking_id}",
            headers={"Cookie": f"token={auth_token}"},
            timeout=20,
        )
    except requests.RequestException:
        pass
