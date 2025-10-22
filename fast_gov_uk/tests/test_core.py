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


def test_not_found_get(client):
    response = client.get("/foobar")
    assert response.status_code == 404
    assert "Page not found" in response.text


def test_problem_with_service_get(error_client):
    response = error_client.get("/error")
    assert response.status_code == 500
    assert "Sorry, there is a problem with this service" in response.text


def test_asset_get(client):
    response = client.get("/govuk-frontend-5.11.1.min.css")
    assert response.status_code == 200


def test_page_decorator(fast, client):
    @fast.page
    def test1():
        return
    @fast.page("/foo")
    def test2():
        return
    routes = {r.path for r in fast.routes}
    assert "/test1" in routes
    assert "/foo" in routes
    assert client.get("test1").status_code == 200
    assert client.get("foo").status_code == 200
    assert client.get("bar").status_code == 404


def test_form_decorator(fast, client):
    @fast.form
    def test1(data=None):
        return
    @fast.form("foo")
    def test2(data=None):
        return
    @fast.form()
    def test3(data=None):
        return
    assert "test1" in fast.forms
    assert "foo" in fast.forms
    assert "test3" in fast.forms
    assert client.get("forms/test1").status_code == 200
    assert client.get("forms/foo").status_code == 200
    assert client.get("forms/test3").status_code == 200
    assert client.get("bar").status_code == 404


def test_wizard_decorator(fast, client):
    @fast.wizard
    def test1(step=0, data=None):
        return
    @fast.wizard("foo")
    def test2(step=0, data=None):
        return
    @fast.wizard()
    def test3(step=0, data=None):
        return
    assert "test1" in fast.wizards
    assert "foo" in fast.wizards
    assert "test3" in fast.wizards
    assert client.get("wizards/test1", follow_redirects=True).status_code == 200
    assert client.get("wizards/foo", follow_redirects=True).status_code == 200
    assert client.get("wizards/test3", follow_redirects=True).status_code == 200
    assert client.get("wizards/foo/not-a-step", follow_redirects=True).status_code == 404
    assert client.get("bar", follow_redirects=True).status_code == 404
