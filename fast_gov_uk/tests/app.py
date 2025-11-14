import fasthtml.common as fh

from fast_gov_uk import Fast
from fast_gov_uk import forms
import fast_gov_uk.design_system as ds


fast = Fast({
    "SERVICE_NAME": "Fast-gov-uk test",
    "DATABASE_URL": ":memory:",
    "DEV_MODE": False,
    "NOTIFY_API_KEY": "test-aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
})

@fast.page("/")
def home(session):
    fast.add_notification(session, "Test")
    return ds.Page(ds.P("Hello, world!"))


@fast.page
def error():
    raise Exception


@fast.form
def profile(data=None):
    return forms.Form(
        "profile",
        ds.TextInput("name", "What is your name?"),
        ds.Fieldset(
            ds.Radios(
                name="sex",
                label="What is your sex?",
                choices={"male": "Male", "female": "Female", "skip": "Prefer not to say"},
            ),
            ds.Radios(
                name="gender",
                label="Is your gender the same as your sex?",
                choices={"yes": "Yes", "no": "No", "skip": "Prefer not to say"},
            ),
        ),
        ds.Radios(
            name="ethnicity",
            label="What is your ethnicity?",
            choices={"white": "White", "mixed": "Mixed", "asian": "Asian", "black": "African or Caribbean", "other": "Other"},
        ),
        ds.DateInput("dob", "What is your date of birth?"),
        ds.FileUpload("picture", "Upload a profile picture"),
        ds.NumberInput("phone", "What is your phone number?"),
        ds.EmailInput("email", "What is your email?"),
        ds.CharacterCount(
            name="comments",
            label="Any comments?",
            maxchars=10,
            required=False,
        ),
        backends=[forms.DBBackend(db=fast.db)],
        data=data,
        cta="Send feedback",
        db=fast.db,
    )


def feedback_form(backend, data=None):
    return forms.Form(
        "feedback",
        ds.Radios(
            name="satisfaction",
            label="How satisfied did you feel about the service?",
            choices={"satisfied": "Satisfied", "dissatisfied": "Dissatisfied"},
        ),
        backends=[backend],
        data=data,
        cta="Send feedback",
    )


@fast.form
def log_feedback(data=None):
    backend = forms.LogBackend()
    return feedback_form(backend, data=data)


@fast.form
def email_feedback(data=None):
    notify = fast.notify("test", "test@test.com")
    backend = forms.EmailBackend(notify)
    return feedback_form(backend, data=data)


@fast.form
def api_feedback(data=None):
    backend = forms.APIBackend(
        url="https://test.com",
        username="test_user",
        password="test_password"
    )
    return feedback_form(backend, data=data)


@fast.form
def session_feedback(data=None):
    backend = forms.SessionBackend()
    return feedback_form(backend, data=data)


@fast.wizard
def mini_equality(step=0, data=None):
    return forms.Wizard(
        "equality",
        forms.Question(
            ds.Radios(
                name="permission",
                label="Do you want to answer the equality questions?",
                choices={
                    "yes": "Yes, answer the equality questions",
                    "no": "No, skip the equality questions"
                },
            ),
            cta="Continue",
        ),
        forms.Question(
            ds.Radios(
                name="health",
                label=(
                    "Do you have any physical or mental health conditions or illness "
                    "lasting or expected to last 12 months or more?"
                ),
                choices={"yes": "Yes", "no": "No", "skip": "Prefer not to say"},
            ),
            predicates={"permission": "yes"},
            cta="Continue",
        ),
        forms.Question(
            ds.Radios(
                name="ability",
                label=(
                    "Do any of your conditions or illnesses reduce your ability "
                    "to carry out day to day activities?"
                ),
                choices={"alot": "Yes, a lot", "little": "Yes, a little", "not": "Not at all", "skip": "Prefer not to say"},
                required=False,
            ),
            predicates={"permission": "yes", "health": "yes"},
            cta="Continue",
        ),
        forms.Question(
            ds.Fieldset(
                ds.Radios(
                    name="sex",
                    label="What is your sex?",
                    choices={"female": "Female", "male": "Male", "skip": "Prefer not to say"},
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
            predicates={"permission": "yes"},
            cta="Continue",
        ),
        backends=[forms.DBBackend(db=fast.db)],
        step=step,
        data=data,
    )


@fast.page
def session(session):
    return fh.JSONResponse(session)
