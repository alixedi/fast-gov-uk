def test_home_get(client):
    response = client.get("/")
    assert response.status_code == 200


def test_cookie_banner_get(client):
    response = client.get("/cookie-banner")
    assert response.status_code == 200
    assert 'id="cookie-banner"' in response.text
    assert list(response.cookies.items()) == []

def test_cookie_banner_post(client):
    response = client.post(
        "/cookie-banner",
        data={"cookies[additional]": "hide"},
    )
    assert response.status_code == 200
    assert 'id="cookie-banner"' not in response.text
    assert list(response.cookies.items()) == [
        ("cookie_policy", 'hide')
    ]

def test_cookies_get(client):
    response = client.get("/cookies")
    assert response.status_code == 200
    assert "session_cookie" in response.text
    assert "cookie_policy" in response.text


def test_phase_get(client):
    response = client.get("/phase")
    assert response.status_code == 200
    assert "Alpha" in response.text


def test_notification_get(client):
    client.get("/")
    response = client.get("/notifications")
    assert response.status_code == 200
    assert "Important" in response.text
