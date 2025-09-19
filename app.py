from os import environ as env

from fasthtml import common as fh

import fast_gov_uk.design_system as ds
from fast_gov_uk import forms
from fast_gov_uk.core import Fast

# This is your settings. They are set for development on your
# own computer by default. When you are deploying your service,
# you can override them by setting environment variables.
SETTINGS = {
    "SERVICE_NAME": env.get("SERVICE_NAME", "Fast Gov UK"),
    "DATABASE_URL": env.get("DATABASE_URL", "data/service.db"),
    "DEV_MODE": env.get("DEV_MODE", True),
    "NOTIFY_API_KEY": env.get("NOTIFY_API_KEY", None),
}


# This creates the Fast object that encapsulates everything
# in your service
fast = Fast(SETTINGS)


# If I do @fast.page() instead, this page will be available
# on /home i.e. the name of the function
@fast.page("/")
def home():
    return ds.Page(
        # A single Paragraph
        ds.P("Welcome to Fast Gov UK.")
    )


# I can do @fast.form("foo") instead to make this page available
# on /form/foo instead of the default /form/feedback
@fast.form
def feedback(data=None):
    """
    Feedback form is common and recommended in gov.uk services.
    This form also serves as an example for how to add new forms
    to fast-gov-uk.

    Forms can be empty when rendered for the first time. Forms
    can also have data e.g. when you enter invalid information in
    a field and the you get the form again with errors as well as
    what you filled in.

    In view of the above, this is a function that takes data as as
    argument and passes it into the Form.

    It also sets -

    success_url: Redirects here if the form is submitted correctly

    cta: Call to action - label for the form button

    db: This is a DBForm so it needs a reference to the database
    so that it can save upon correct submission
    """
    # A DBForm gets saved to the database when its valid
    return forms.DBForm(
        title="Give feedback for Fast Gov UK",
        fields=[
            ds.Radios(
                name="satisfaction",
                label="Overall, how satisfied did you feel about Fast Gov UK?",
                choices=[
                    "Very Satisfied",
                    "Satisfied",
                    "Neither satisfied not dissatisfied",
                    "Dissatisfied",
                    "Very dissatisfied",
                ],
            ),
            ds.CharacterCount(
                name="comments",
                label="How could we improve this service?",
                maxchars=1200,
                required=False,
                hint=(
                    "Do not include any personal or financial information, "
                    "for example your national insurance number."
                ),
            ),
        ],
        data=data,
        success_url="/",
        cta="Send feedback",
        db=fast.db,
    )


# Serves the app
fh.serve(app="fast")
