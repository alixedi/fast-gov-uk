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
            ds.Radios(
                name="gender",
                label="What is your gender?",
                choices=["Male", "Female", "Prefer not to say"],
            ),
            ds.Radios(
                name="ethnicity",
                label="What is your ethnicity?",
                choices=["White", "Mixed", "Asian", "African or Caribbean", "Other"],
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
                choices=["Satisfied", "Dissatisfied"],
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
                choices=["Satisfied", "Dissatisfied"],
            ),
        ],
        data=data,
        success_url="/",
        cta="Send feedback",
        url="https://test.com",
        username="test_user",
        password="test_password",
    )
