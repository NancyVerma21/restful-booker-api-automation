import pytest


@pytest.mark.smoke
def test_api_health_check(api_session, api_base_url):
    response = api_session.get(f"{api_base_url}/ping", timeout=20)

    assert response.status_code == 201
    assert response.text.strip().lower() == "created"


@pytest.mark.smoke
def test_valid_authentication_returns_token(api_session, api_base_url):
    response = api_session.post(
        f"{api_base_url}/auth",
        json={"username": "admin", "password": "password123"},
        timeout=20,
    )

    assert response.status_code == 200
    assert response.json().get("token")
