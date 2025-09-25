import json
from dataclasses import asdict
from unittest.mock import Mock, patch, call, ANY

import pytest


def test_form_get(client):
    response = client.get("/form/profile")
    assert response.status_code == 200


def test_form_get_404(client):
    response = client.get("/form/not-profile")
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
        "/form/profile",
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
        "sex": "male",
        "gender": "yes",
        "ethnicity": "mixed",
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
            {"name": "This field is required."}
        ),
        (
            # empty sex
            {"sex": ""},
            {"sex": "This field is required."}
        ),
        (
            # empty gender
            {"gender": ""},
            {"gender": "This field is required."}
        ),
        (
            # empty ethnicity
            {"ethnicity": ""},
            {"ethnicity": "This field is required."}
        ),
        (
            # empty dob
            {"dob": ["", "", ""]},
            {"dob": "This field is required."}
        ),
        (
            # partially empty dob
            {"dob": ["10", "10", ""]},
            {"dob": "This field is required."}
        ),
        (
            # invalid dob
            {"dob": ["foo", "10", "2003"]},
            {"dob": "Invalid values."}
        ),
        (
            # empty picture
            {"picture": ""},
            {"picture": "This field is required."}
        ),
        (
            # empty phone
            {"phone": ""},
            {"phone": "This field is required."}
        ),
        (
            # non-numeric phone
            {"phone": "A12345"},
            {"phone": "Value is not a number."}
        ),
        (
            # non-numeric phone
            {"phone": "test"},
            {"phone": "Value is not a number."}
        ),
        (
            # empty email
            {"email": ""},
            {"email": "This field is required."}
        ),
        (
            # invalid email
            {"email": "test"},
            {"email": "Value is not an email."}
        ),
        (
            # Comments more than 10 chars
            {"comments": "This is a long comment."},
            {"comments": "Characters exceed limit of 10."}
        ),
))
def test_form_post_invalid(errors, expected, client, db, picture):
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
    with patch("fast_gov_uk.core.ds.Page") as mock_page:
        response = client.post(
            "/form/profile",
            data=data,
            files={"picture": picture},
        )
        form = mock_page.call_args.args[0]
        assert response.status_code == 200
        assert form.errors == expected


def test_email_form_post_valid(fast, db, client):
    data = {"satisfaction": "satisfied"}
    response = client.post(
        "/form/email_feedback",
        data=data,
    )
    assert response.status_code == 303
    notify_call_args = fast.notify_client.send_email_notification.call_args
    assert notify_call_args == call(
        email_address='test@test.com',
        template_id='test',
        personalisation={
            'form_name': 'Feedback',
            'form_data': '* satisfaction: satisfied',
            'service_name': 'Fast-gov-uk test'
        }
    )


def test_api_form_post_valid(fast, db, client):
    data = {"satisfaction": "satisfied"}
    with patch("fast_gov_uk.forms._client") as mock_client:
        mock_post = Mock()
        mock_client.return_value = Mock(post=mock_post)
        response = client.post(
            "/form/api_feedback",
            data=data,
        )
    assert response.status_code == 303
    assert mock_client.call_args == call("test_user", "test_password")
    assert mock_post.call_args == call(
        'https://test.com',
        data={
            'satisfaction': 'satisfied',
            'form_name': 'Feedback',
            'submitted_on': ANY,
        }
    )


def test_questions_get(client):
    response = client.get("/questions/mini_equality")
    assert response.status_code == 307
    response = client.get("/questions/mini_equality/0")
    assert response.status_code == 200
    response = client.get("/questions/mini_equality/1")
    assert response.status_code == 200
    response = client.get("/questions/mini_equality/2")
    assert response.status_code == 200
    response = client.get("/questions/mini_equality/3")
    assert response.status_code == 200


def test_question_no_permission(db, client):
    response = client.post(
        "/questions/mini_equality/",
        data={"permission": "no"},
    )
    assert response.status_code == 303
    assert response.headers["Location"] == "/"


def test_question_permission(db, client):
    response = client.post(
        "/questions/mini_equality/",
        data={"permission": "yes"},
    )
    assert response.status_code == 303
    assert response.headers["Location"] == "/questions/mini_equality/1"


def test_questions_no_predicate(db, client):
    response = client.post(
        "/questions/mini_equality/1",
        data={"permission": "yes", "health": "no"},
    )
    assert response.status_code == 303
    assert response.headers["Location"] == "/questions/mini_equality/3"


def test_questions_predicate(db, client):
    response = client.post(
        "/questions/mini_equality/1",
        data={"permission": "yes", "health": "yes"},
    )
    assert response.status_code == 303
    assert response.headers["Location"] == "/questions/mini_equality/2"


def test_questions_valid(db, client):
    response = client.post(
        "/questions/mini_equality/3",
        data={"permission": "yes", "health": "yes", "ability": "yes", "sex": "skip", "gender": "skip"},
    )
    assert response.status_code == 303
    assert response.headers["Location"] == "/"
    forms = db.t.forms()
    form = forms[0]
    assert form.title == "Equality monitoring"
    form_json = asdict(form)
    form_data = form_json["data"]
    form_dict = json.loads(form_data)
    assert form_dict == {
        "permission": "yes",
        "health": "yes",
        "ability": "yes",
        "sex": "skip",
        "gender": "skip"
    }
