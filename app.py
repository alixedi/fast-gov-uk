from os import environ as env

from fasthtml import common as fh

import fast_gov_uk.design_system as ds
from fast_gov_uk import forms
from fast_gov_uk.core import Fast

# This is your settings. They are set for development on your
# own computer by default. When you are deploying your service,
# you can override them by setting environment variables.
SETTINGS = {
    "DATABASE_URL": env.get("DATABASE_URL", "data/service.db"),
    "DEV_MODE": env.get("DEV_MODE", True),
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
@fast.form()
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
        title="Give feeback for Fast Gov UK",
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
                hint="Do not include any personal or financial infrmation, for example your national insurance number.",
            ),
        ],
        data=data,
        success_url="/",
        cta="Send feedback",
        db=fast.db,
    )


@fast.question()
def equality(step=0, data=None):
    """
    This is an example of a question-protocol aka wizard form.
    It steps through the fields one at a time.

    It takes step as an argument to know which field to show.
    It also takes data as an argument to fill in the fields
    that have already been filled in.

    Note that this form does not do anything with the data
    when it is completed. You can add your own processing logic
    in the process method of the Questions class.
    """
    return forms.DBQuestions(
        title="Equality monitoring",
        fields=[
            ds.Radios(
                name="permission",
                label="Do you want to answer the equality questions?",
                choices=[
                    "Yes, answer the equality questions",
                    "No, skip the equality questions"
                ],
            ),
            ds.DateInput(
                name="dob",
                label="What is your date of birth?",
            ),
            ds.Radios(
                name="health",
                label=(
                    "Do you have any physical or mental health conditions or illness "
                    "lasting or expected to last 12 months or more?"
                ),
                choices=["Yes", "No", "Prefer not to say"],
            ),
            ds.Radios(
                name="ability",
                label=(
                    "Do any of your conditions or illnesses reduce your ability "
                    "to carry out day to day activities?"
                ),
                choices=["Yes, a lot", "Yes, a little", "Not at all", "Prefer not to say"],
            ),
            ds.Radios(
                name="ethnic-group",
                label="What is your ethnic group?",
                choices=[
                    "White",
                    "Mixed or multiple ethnic groups",
                    "Asian or Asian British",
                    "Black, African, Caribbean or Black British",
                    "Other ethnic group",
                    "Prefer not to say",
                ],
            ),
            ds.Radios(
                name="white",
                label="Which of the following best describes your White background?",
                choices=[
                    "English, Welsh, Scottish, Northern Irish or British",
                    "Irish",
                    "Gypsy or Irish Traveller",
                    "Any other White background",
                    "Prefer not to say",
                ],
            ),
            ds.Radios(
                name="multiple",
                label=(
                    "Which of the following best describes your "
                    "multiple ethnic group background?"
                ),
                choices=[
                    "White and Black Caribbean",
                    "White and Black African",
                    "White and Asian",
                    "Any other mixed or multiple ethnic background",
                    "Prefer not to say",
                ],
            ),
            ds.Radios(
                name="asian",
                label=(
                    "Which of the following best describes your "
                    "Asian or Asian British background?"
                ),
                choices=[
                    "Indian",
                    "Pakistani",
                    "Bangladeshi",
                    "Chinese",
                    "Any other Asian background",
                    "Prefer not to say",
                ],
            ),
            ds.Radios(
                name="black",
                label=(
                    "Which of the following best describes your Black, African, "
                    "Caribbean or Black British background?"
                ),
                choices=[
                    "African",
                    "Caribbean",
                    "Any other Black, African or Caribbean background",
                    "Prefer not to say",
                ],
            ),
            ds.Radios(
                name="other",
                label="Which of the following best describes your background?",
                choices=["Arab", "Any other ethnic group", "Prefer not to say"],
            ),
            ds.Radios(
                name="marital-status",
                label="What is your legal marital or registered civil partnership status?",
                choices=[
                    "Never married and never registered in a civil partnership",
                    "Married",
                    "In a registered civil partnership",
                    "Separated, but still legally married",
                    "Separated, but still legally in a civil partnership",
                    "Divorced",
                    "Formerly in a civil partnership which is now legally dissolved",
                    "Widowed",
                    "Surviving partner from a registered civil partnership",
                    "Prefer not to say",
                ],
            ),
            ds.Radios(
                name="religion",
                label="What is your religion?",
                choices=[
                    "No religion",
                    "Christian",
                    "Buddhist",
                    "Hindu",
                    "Jewish",
                    "Muslim",
                    "Sikh",
                    "Any other religion",
                    "Prefer not to say",
                ],
            ),
            ds.Fieldset(
                "Sex and gender identity",
                ds.Radios(
                    name="sex",
                    label="What is your sex?",
                    choices=["Female", "Male", "Prefer not to say"],
                ),
                ds.Radios(
                    name="gender",
                    label=(
                        "Is the gender you identify with the same as "
                        "your sex registered at birth?"
                    ),
                    choices=["Yes", "No", "Prefer not to say"],
                )
            ),
            ds.Radios(
                name="sexual-orientation",
                label="Which of the following best describes your sexual orientation?",
                choices=[
                    "Heterosexual or straight",
                    "Gay or lesbian",
                    "Bisexual",
                    "Other",
                    "Prefer not to say",
                ],
            ),
        ],
        data=data,
        step=step,
        success_url="/",
        cta="Continue",
        db=fast.db,
    )

# Serves the app
fh.serve(app="fast")
