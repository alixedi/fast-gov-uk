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
                choices={
                    "very-satisfied": "Very Satisfied",
                    "satisfied": "Satisfied",
                    "neutral": "Neither satisfied not dissatisfied",
                    "dissatisfied": "Dissatisfied",
                    "very-dissatisfied": "Very dissatisfied",
                },
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
                choices={
                    "yes": "Yes, answer the equality questions",
                    "no": "No, skip the equality questions",
                },
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
                choices={"yes": "Yes", "no": "No", "skip": "Prefer not to say"},
            ),
            ds.Radios(
                name="ability",
                label=(
                    "Do any of your conditions or illnesses reduce your ability "
                    "to carry out day to day activities?"
                ),
                choices={
                    "alot": "Yes, a lot",
                    "little": "Yes, a little",
                    "not": "Not at all",
                    "skip": "Prefer not to say",
                },
                required=False,
            ),
            ds.Radios(
                name="ethnic-group",
                label="What is your ethnic group?",
                choices={
                    "white": "White",
                    "mixed": "Mixed or multiple ethnic groups",
                    "asian": "Asian or Asian British",
                    "black": "Black, African, Caribbean or Black British",
                    "other": "Other ethnic group",
                    "skip": "Prefer not to say",
                },
            ),
            ds.Radios(
                name="white",
                label="Which of the following best describes your White background?",
                choices={
                    "british": "English, Welsh, Scottish, Northern Irish or British",
                    "irish": "Irish",
                    "gypsy": "Gypsy or Irish Traveller",
                    "other": "Any other White background",
                    "skip": "Prefer not to say",
                },
                required=False,
            ),
            ds.Radios(
                name="mixed",
                label=(
                    "Which of the following best describes your "
                    "multiple ethnic group background?"
                ),
                choices={
                    "caribbean": "White and Black Caribbean",
                    "african": "White and Black African",
                    "asian": "White and Asian",
                    "mixed": "Any other mixed or multiple ethnic background",
                    "skip": "Prefer not to say",
                },
                required=False,
            ),
            ds.Radios(
                name="asian",
                label=(
                    "Which of the following best describes your "
                    "Asian or Asian British background?"
                ),
                choices={
                    "indian": "Indian",
                    "pakistani": "Pakistani",
                    "bangladeshi": "Bangladeshi",
                    "chinese": "Chinese",
                    "other": "Any other Asian background",
                    "skip": "Prefer not to say",
                },
                required=False,
            ),
            ds.Radios(
                name="black",
                label=(
                    "Which of the following best describes your Black, African, "
                    "Caribbean or Black British background?"
                ),
                choices={
                    "african": "African",
                    "caribbean": "Caribbean",
                    "other": "Any other Black, African or Caribbean background",
                    "skip": "Prefer not to say",
                },
                required=False,
            ),
            ds.Radios(
                name="other",
                label="Which of the following best describes your background?",
                choices={
                    "arab": "Arab",
                    "other": "Any other ethnic group",
                    "skip": "Prefer not to say",
                },
                required=False,
            ),
            ds.Radios(
                name="marital-status",
                label="What is your legal marital or registered civil partnership status?",
                choices={
                    "never": "Never married and never registered in a civil partnership",
                    "married": "Married",
                    "civil-partnership": "In a registered civil partnership",
                    "separated-married": "Separated, but still legally married",
                    "separated-civil-partnership": "Separated, but still legally in a civil partnership",
                    "divorced": "Divorced",
                    "dissolved": "Formerly in a civil partnership which is now legally dissolved",
                    "widowed": "Widowed",
                    "surviving-partner": "Surviving partner from a registered civil partnership",
                    "skip": "Prefer not to say",
                },
            ),
            ds.Radios(
                name="religion",
                label="What is your religion?",
                choices={
                    "no": "No religion",
                    "christian": "Christian",
                    "budhhist": "Buddhist",
                    "hindu": "Hindu",
                    "jewish": "Jewish",
                    "muslim": "Muslim",
                    "sikh": "Sikh",
                    "other": "Any other religion",
                    "skip": "Prefer not to say",
                },
            ),
            ds.Fieldset(
                ds.Radios(
                    name="sex",
                    label="What is your sex?",
                    choices={
                        "female": "Female",
                        "male": "Male",
                        "skip": "Prefer not to say",
                    },
                ),
                ds.Radios(
                    name="gender",
                    label=(
                        "Is the gender you identify with the same as "
                        "your sex registered at birth?"
                    ),
                    choices={"yes": "Yes", "no": "No", "skip": "Prefer not to say"},
                ),
                legend="Sex and gender identity",
                name="sex-and-gender",
            ),
            ds.Radios(
                name="sexual-orientation",
                label="Which of the following best describes your sexual orientation?",
                choices={
                    "straight": "Heterosexual or straight",
                    "gay-or-lesbian": "Gay or lesbian",
                    "bisexual": "Bisexual",
                    "other": "Other",
                    "skip": "Prefer not to say",
                },
            ),
        ],
        data=data,
        step=step,
        success_url="/",
        cta="Continue",
        db=fast.db,
        predicates={
            # These fields are only run if the data collected
            # in specified prior fields have the specified values
            "dob": {"permission": "yes"},
            "health": {"permission": "yes"},
            "ability": {"permission": "yes", "health": "yes"},
            "ethnic-group": {"permission": "yes"},
            "white": {"permission": "yes", "ethnic-group": "white"},
            "mixed": {"permission": "yes", "ethnic-group": "mixed"},
            "asian": {"permission": "yes", "ethnic-group": "asian"},
            "black": {"permission": "yes", "ethnic-group": "black"},
            "other": {"permission": "yes", "ethnic-group": "other"},
            "marital-status": {"permission": "yes"},
            "religion": {"permission": "yes"},
            "sex-and-gender": {"permission": "yes"},
            "sexual-orientation": {"permission": "yes"},
        },
    )


@fast.page
def cookies():
    return ds.Cookies()


# Serves the app
fh.serve(app="fast")
