import json
from dataclasses import asdict
from unittest.mock import Mock, patch, call, ANY

import pytest

from .app import session_feedback
from fast_gov_uk import forms


def test_form_get(client):
    response = client.get("/forms/profile")
    assert response.status_code == 200


def test_form_get_404(client):
    response = client.get("/forms/not-profile")
    assert response.status_code == 404


def test_db_form_post_valid(client, db, picture):
    data = {
        "name": "Test",
        "sex": "male",
        "gender": "yes",
        "ethnicity": "mixed",
        "dob": ["10", "10", "2000"],
        "phone": "12345",
        "email": "test@test",
        "comments": "Test",
    }
    response = client.post(
        "/forms/profile",
        data=data,
        files={"picture": picture},
    )
    assert response.status_code == 303
    forms = db.t.forms()
    form = forms[0]
    form_json = asdict(form)
    form_data = form_json["data"]
    form_dict = json.loads(form_data)
    assert form_dict == {
        "name": "Test",
        "sex": "Male",
        "gender": "Yes",
        "ethnicity": "Mixed",
        # This should be a date string
        "dob": "2000-10-10",
        # This should be a path to the file stored in /media
        "picture": "media/picture.png",
        # This should be a number
        "phone": 12345,
        "email": "test@test",
        "comments": "Test",
    }


@pytest.mark.parametrize("errors, expected", (
        (
            # empty name
            {"name": ""},
            ("name", "This field is required.")
        ),
        (
            # empty sex
            {"sex": ""},
            ("sex", "This field is required.")
        ),
        (
            # empty gender
            {"gender": ""},
            ("gender", "This field is required.")
        ),
        (
            # empty ethnicity
            {"ethnicity": ""},
            ("ethnicity", "This field is required.")
        ),
        (
            # empty dob
            {"dob": ["", "", ""]},
            ("dob", "This field is required.")
        ),
        (
            # partially empty dob
            {"dob": ["10", "10", ""]},
            ("dob", "This field is required.")
        ),
        (
            # invalid dob
            {"dob": ["foo", "10", "2003"]},
            ("dob", "Invalid values.")
        ),
        (
            # empty picture
            {"picture": ""},
            ("picture", "This field is required.")
        ),
        (
            # empty phone
            {"phone": ""},
            ("phone", "This field is required.")
        ),
        (
            # non-numeric phone
            {"phone": "A12345"},
            ("phone", "Value is not a number.")
        ),
        (
            # non-numeric phone
            {"phone": "test"},
            ("phone", "Value is not a number.")
        ),
        (
            # empty email
            {"email": ""},
            ("email", "This field is required.")
        ),
        (
            # invalid email
            {"email": "test"},
            ("email", "Value is not an email.")
        ),
        (
            # Comments more than 10 chars
            {"comments": "This is a long comment."},
            ("comments", "Characters exceed limit of 10.")
        ),
))
def test_form_post_invalid(errors, expected, client, db, picture, html, find):
    data = {
        "name": "Test",
        "sex": "male",
        "gender": "yes",
        "ethnicity": "mixed",
        "dob": ["10", "10", "2000"],
        "phone": "12345",
        "email": "test@test",
        "comments": "Test",
    }
    data.update(errors)
    response = client.post(
        "/forms/profile",
        data=data,
        files={"picture": picture},
    )
    assert response.status_code == 200
    field_name, error_message = expected
    expected_html = html(
        f'<p class="govuk-error-message" id="{field_name}-error">'
            '<span class="govuk-visually-hidden">Error: </span>'
            f"{error_message}"
        "</p>"
    )
    error_p = find(response.text, "p", {"class": "govuk-error-message"})
    assert html(error_p) == expected_html


@patch("fast_gov_uk.forms.logger")
def test_log_form_post_valid(mock_logger, client):
    data = {"satisfaction": "satisfied"}
    response = client.post(
        "/forms/log_feedback",
        data=data,
    )
    assert response.status_code == 303
    logger_call_args = mock_logger.info.call_args
    assert logger_call_args == call(
        "Form: 'feedback' processed with: {'satisfaction': 'Satisfied'}."
    )


def test_email_form_post_valid(fast, db, client):
    data = {"satisfaction": "satisfied"}
    response = client.post(
        "/forms/email_feedback",
        data=data,
    )
    assert response.status_code == 303
    notify_call_args = fast.notify_client.send_email_notification.call_args
    assert notify_call_args == call(
        email_address='test@test.com',
        template_id='test',
        personalisation={
            'form_name': 'feedback',
            'form_data': '* satisfaction: Satisfied',
            'service_name': 'Fast-gov-uk test'
        }
    )


def test_api_form_post_valid(fast, db, client):
    data = {"satisfaction": "satisfied"}
    with patch("fast_gov_uk.forms._client") as mock_client:
        mock_post = Mock()
        mock_client.return_value = Mock(post=mock_post)
        response = client.post(
            "/forms/api_feedback",
            data=data,
        )
    assert response.status_code == 303
    assert mock_client.call_args == call("test_user", "test_password")
    assert mock_post.call_args == call(
        'https://test.com',
        data={
            'satisfaction': 'Satisfied',
            'form_name': 'feedback',
            'submitted_on': ANY,
        }
    )


def test_session_form_post_valid(fast, db, client):
    data = {"satisfaction": "satisfied"}
    response = client.post(
        "/forms/session_feedback",
        data=data,
        follow_redirects=True,
    )
    assert response.status_code == 200
    response = client.get("/session")
    feedback = response.json()["feedback"]
    assert feedback == {"satisfaction": "Satisfied"}


def test_questions_get(client):
    response = client.get("/wizards/mini_equality")
    assert response.status_code == 307
    response = client.get("/wizards/mini_equality/0")
    assert response.status_code == 200
    response = client.get("/wizards/mini_equality/1")
    assert response.status_code == 200
    response = client.get("/wizards/mini_equality/2")
    assert response.status_code == 200
    response = client.get("/wizards/mini_equality/3")
    assert response.status_code == 200


def test_question_no_permission(db, client):
    response = client.post(
        "/wizards/mini_equality/",
        data={"permission": "no"},
    )
    assert response.status_code == 303
    assert response.headers["Location"] == "/"


def test_question_permission(db, client):
    response = client.post(
        "/wizards/mini_equality/",
        data={"permission": "yes"},
    )
    assert response.status_code == 303
    assert response.headers["Location"] == "/wizards/mini_equality/1"


def test_questions_predicate_true(db, client):
    response = client.post(
        "/wizards/mini_equality/",
        data={"permission": "yes"},
    )
    assert response.status_code == 303
    assert response.headers["Location"] == "/wizards/mini_equality/1"


def test_questions_predicate_false(db, client):
    response = client.post(
        "/wizards/mini_equality",
        data={"permission": "no"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert response.url == "http://testserver/"


def test_questions_valid(db, client):
    # First step
    response = client.post(
        "/wizards/mini_equality/",
        data={"permission": "yes"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    # Second step
    response = client.post(
        response.url,
        data={"health": "yes"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    # Third step
    response = client.post(
        response.url,
        data={"ability": "alot"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    # Invalid input
    response = client.post(
        response.url,
        data={},
        follow_redirects=True,
    )
    assert response.status_code == 200
    # Still third step
    response = client.post(
        "/wizards/mini_equality/3",
        data={"sex": "skip", "gender": "skip"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert response.url.path == "/"
    forms = db.t.forms()
    form = forms[0]
    assert form.name == "equality"
    form_json = asdict(form)
    form_data = form_json["data"]
    form_dict = json.loads(form_data)
    assert form_dict == {
        "permission": "Yes, answer the equality questions",
        "health": "Yes",
        "ability": "Yes, a lot",
        "sex": "Prefer not to say",
        "gender": "Prefer not to say"
    }
    # Invalid step
    response = client.get(
        "/wizards/mini_equality/20",
        follow_redirects=True,
    )
    assert response.status_code == 404



def test_error_summary(html, find):
    form = session_feedback(data={})
    expected = html(
        # The error summary - containine a link to the Radio field
        '<div class="govuk-error-summary" data-module="govuk-error-summary">'
            '<div role="alert">'
                '<h2 class="govuk-error-summary__title">There is a problem</h2>'
                '<div class="govuk-error-summary__body">'
                    '<ul class="govuk-list govuk-error-summary__list">'
                        '<li><a class="govuk-link" href="#satisfaction">How satisfied did you feel about the service?</a></li>'
                    "</ul>"
                "</div>"
            "</div>"
        "</div>"
    )
    form_html = html(form)
    error_summary = find(form_html, "div", {"class": "govuk-error-summary"})
    assert html(error_summary) == expected


def test_no_fields_at_root():
    with pytest.raises(ValueError):
        forms.Form("test", "test")


@patch("fast_gov_uk.forms.httpx")
def test_client(mock_httpx):
    _ = forms._client("test", "test")
    auth = mock_httpx.BasicAuth
    assert auth.call_args == call(username="test", password="test")
    client = mock_httpx.Client
    assert client.called
