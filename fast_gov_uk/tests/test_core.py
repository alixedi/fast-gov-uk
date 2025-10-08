def test_home_get(client):
    response = client.get("/")
    assert response.status_code == 200


def test_cookie_get(client):
    response = client.get("/cookie-banner")
    assert response.status_code == 200
    assert 'id="cookie-banner"' in response.text
    assert list(response.cookies.items()) == []

def test_cookie_post(client):
    response = client.post(
        "/cookie-banner",
        data={"cookies[additional]": "hide"},
    )
    assert response.status_code == 200
    assert 'id="cookie-banner"' not in response.text
    assert list(response.cookies.items()) == [
        ("cookie_policy", 'hide')
    ]
