import json
from dataclasses import asdict
from unittest.mock import patch, call

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
        "gender": "male",
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
        "gender": "male",
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
            # empty phone
            {"phone": ""},
            {"phone": "This field is required."}
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
        "gender": "male",
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


def test_email_form_post_valid(fast, client):
    data = {"satisfaction": "satisfied"}
    response = client.post(
        "/form/feedback",
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
