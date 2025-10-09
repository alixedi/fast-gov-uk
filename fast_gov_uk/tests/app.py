import fast_gov_uk.design_system as ds
from fast_gov_uk import forms
from fast_gov_uk.core import Fast


fast = Fast({
    "SERVICE_NAME": "Fast-gov-uk test",
    "DATABASE_URL": ":memory:",
    "DEV_MODE": False,
    "NOTIFY_API_KEY": "test-aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
})

@fast.page("/")
def home():
    return ds.Page(ds.P("Hello, world!"))


@fast.form
def profile(data=None):
    return forms.DBForm(
        title="Create a Profile",
        fields=[
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
        ],
        data=data,
        success_url="/",
        cta="Send feedback",
        db=fast.db,
    )


@fast.form
def email_feedback(data=None):
    return forms.EmailForm(
        title="Feedback",
        fields=[
            ds.Radios(
                name="satisfaction",
                label="How satisfied did you feel about the service?",
                choices={"satisfied": "Satisfied", "dissatisfied": "Dissatisfied"},
            ),
        ],
        data=data,
        success_url="/",
        cta="Send feedback",
        notify=fast.notify("test", "test@test.com"),
    )


@fast.form
def api_feedback(data=None):
    return forms.APIForm(
        title="Feedback",
        fields=[
            ds.Radios(
                name="satisfaction",
                label="How satisfied did you feel about the service?",
                choices={"satisfied": "Satisfied", "dissatisfied": "Dissatisfied"},
            ),
        ],
        data=data,
        success_url="/",
        cta="Send feedback",
        url="https://test.com",
        username="test_user",
        password="test_password",
    )


@fast.question
def mini_equality(step=0, data=None):
    return forms.DBQuestions(
        title="Equality monitoring",
        fields=[
            ds.Radios(
                name="permission",
                label="Do you want to answer the equality questions?",
                choices={
                    "yes": "Yes, answer the equality questions",
                    "no": "No, skip the equality questions"
                },
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
                choices={"alot": "Yes, a lot", "little": "Yes, a little", "not": "Not at all", "skip": "Prefer not to say"},
                required=False,
            ),
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
        ],
        data=data,
        step=step,
        success_url="/",
        cta="Continue",
        db=fast.db,
        predicates={
            # These fields are only run if the data collected
            # in specified prior fields have the specified values
            "health": {"permission": "yes"},
            "ability": {"permission": "yes", "health": "yes"},
            "sex-and-gender": {"permission": "yes"},
        }
    )


@fast.page
def cookies():
    return ds.Cookies()


@fast.page
def phase():
    return ds.PhaseBanner(
        ds.Span(
            "This is a new service. Help us improve it and ",
            ds.A("give your feedback.", href="/form/feedback"),
        ),
        phase="Alpha",
    )
