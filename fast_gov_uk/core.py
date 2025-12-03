from pathlib import Path

import fasthtml.common as fh
from notifications_python_client import notifications as notify

import fast_gov_uk.design_system as ds
from fast_gov_uk import forms


GOV_UK_HTTP_HEADERS = [
    fh.Link(rel="stylesheet", href="/govuk-frontend-5.11.1.min.css", type="text/css"),
    fh.Meta(name="theme-color", content="#1d70b8"),
    fh.Link(rel="icon", sizes="48x48", href="/assets/rebrand/images/favicon.ico"),
    fh.Link(
        rel="icon",
        sizes="any",
        href="/assets/rebrand/images/favicon.svg",
        type="image/svg+xml",
    ),
    fh.Link(
        rel="mask-icon",
        href="/assets/rebrand/images/govuk-icon-mask.svg",
        color="#1d70b8",
    ),
    fh.Link(rel="apple-touch-icon", href="/assets/rebrand/images/govuk-icon-180.png"),
]


def not_found(req, exc):
    return ds.Page(
        ds.H1("Page not found"),
        ds.P("If you typed the web address, check it is correct."),
        ds.P("If you pasted the web address, check you copied the entire address."),
        ds.P(
            "If the web address is correct or you selected a link or button, ",
            ds.A("contact us", "/contact-us"),
            "to speak to someone and get help.",
        ),
    )


def problem_with_service(req, exc):
    return ds.Page(
        ds.H1("Sorry, there is a problem with this service"),
        ds.P("Try again later."),
        ds.P(
            ds.A("Contact us", "/contact-us"),
            " if you need to speak to someone about this.",
        ),
    )


def assets(fname: str, ext: str):
    """Serve static assets from the assets directory."""
    assets = Path(__file__).parent / "assets"
    return fh.FileResponse(f"{assets}/{fname}.{ext}")


def footer():
    """
    Footer that will be rendered on every `Page` in the service.

    You can override this like so -

        @fast.page
        def footer():
            return ds.Footer(("My custom footer link", "/link"), ..)
    """
    return ds.Footer(("Cookies", "/cookies"))


def phase():
    """
    Returns a phase banner snippet that is inserted into every
    `Page` of the service using htmx.

    You can override this like so -

        @fast.page
        def phase():
            return ds.PhaseBanner(
                ds.Span("This is a slightly older service.")
                phase="Beta",
            )
    """
    return ds.PhaseBanner(
        ds.Span(
            "This is a new service. Help us improve it and ",
            ds.A("give your feedback.", href="/forms/feedback"),
        ),
        phase="Alpha",
    )


def cookies():
    """
    This returns the standard GDS cookies page. E.g. -
    https://design-system.service.gov.uk/patterns/cookies-page/full-page/

    It is preset to Essential cookies but if you are using more cookies,
    you can override this as follows -

        @fast.page
        def cookies():
            return ds.Cookies(
                ds.H2("Analytical cookies")
                ds.P("...")
                ds.Table(...)
            )
    """
    return ds.Cookies()


def feedback(data=None):
    """
    Feedback form is common and recommended in gov.uk services. This form
    is an attempt to reproduce -

    https://www.gov.uk/service-manual/service-assessments/get-feedback-page

    This forms logs the feedback. If you want to change this form or change
    the Backend so that you get an email when a user submits feedback -

        @fast.form
        def feedback(data=None):
            return forms.Form(
                "feedback",
                ...
                backends=[forms.EmailBackend(...)]
            )
    """
    # A DBForm gets saved to the database when its valid
    return forms.Form(
        "feedback",
        ds.H1("Give feedback on Fast GOV UK"),
        ds.H2("Satisfaction survey"),
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
            heading="s",
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
            heading="s",
        ),
        backends=[forms.LogBackend()],
        success_url="/",
        data=data,
        cta="Send feedback",
    )


def notifications(session):
    notifications = session.get("notifications", [])
    banners = ds.Div(
        *[
            ds.Notification(
                n["content"],
                title=n["title"],
                success=(n["title"] == "Success")
            )
            for n in notifications
        ]
    )
    session.pop("notifications", None)
    return banners


class Fast(fh.FastHTML):
    def __init__(self, settings=None, *args, **kwargs):
        super().__init__(
            pico=False,
            hdrs=GOV_UK_HTTP_HEADERS,
            cls="govuk-template govuk-template--rebranded",
            # TODO: Why do I have to do this?
            style="margin: 0px;",
            exception_handlers={404: not_found, 500: problem_with_service},
            # Set up session cookie
            session_cookie="session_cookie",
            max_age=24*60*60,
        )
        settings = settings or {}
        # Service name
        self.service_name = settings.get("SERVICE_NAME", "Fast")
        # Set up Database
        db_url = settings.get("DATABASE_URL", ":memory:")
        self.db = fh.database(db_url)
        # Set up flag for whether we are in dev mode
        self.dev = settings.get("DEV_MODE", True)
        # Initialize form registry
        self.forms = {}
        # Initialise wizard registry
        self.wizards = {}
        # Set up routes
        self.route("/{fname:path}.{ext:static}")(assets)
        self.route("/forms/{name}", methods=["GET", "POST"])(self.process_form)
        self.route("/wizards/{name}/{step}", methods=["GET", "POST"])(
            self.process_wizard
        )
        self.route("/cookie-banner", methods=["GET", "POST"])(self.cookie_banner)
        self.route()(footer)
        self.route()(phase)
        self.route()(cookies)
        self.form()(feedback)
        self.route("/notifications")(notifications)
        # Initialise notify client
        notify_key = settings.get("NOTIFY_API_KEY", "")
        if notify_key:
            self.notify_client = notify.NotificationsAPIClient(notify_key)

    def notify(self, template_id: str, email: str):
        if not hasattr(self, "notify_client"):
            raise ValueError("NOTIFY_API_KEY not configured.")

        async def _notifier(**kwargs):
            kwargs["service_name"] = self.service_name
            return self.notify_client.send_email_notification(
                email_address=email,
                template_id=template_id,
                personalisation=kwargs,
            )

        return _notifier

    def page(self, url=None):
        def page_decorator(func):
            _url = url or f"/{func.__name__}"
            self.route(_url)(func)
            return func

        if callable(url):
            # Used as @app.page
            func = url
            url = None
            return page_decorator(func)
        # Used as @app.page("/some-url")
        return page_decorator

    def form(self, url=None):
        def form_decorator(func):
            _url = url or func.__name__
            self.forms[_url] = func
            return func

        if callable(url):
            # Used as @app.form
            func = url
            url = None
            return form_decorator(func)
        # Used as @app.form("/some-url")
        return form_decorator

    def wizard(self, url=None):
        def wizard_decorator(func):
            _url = url or func.__name__
            self.wizards[_url] = func
            return func

        if callable(url):
            # Used as @app.form
            func = url
            url = None
            return wizard_decorator(func)
        # Used as @app.question("/some-url")
        return wizard_decorator

    async def process_form(self, req, name: str, post: dict):
        mkform = self.forms.get(name, None)
        if not mkform:
            raise fh.HTTPException(status_code=404)
        # If GET, just return the form
        if req.method == "GET":
            return mkform()
        # If POST, fill the form
        form = mkform(post)
        # If valid, process
        if form.valid:
            return await form.process(req)
        # Else return with errors
        return form

    async def process_wizard(
        self, req, session: dict, name: str, step: str, post: dict
    ):
        try:
            mkwizard = self.wizards[name]
            _step = int(step or "0")
        except (KeyError, ValueError):
            raise fh.HTTPException(status_code=404)
        # If GET, just return the form
        if req.method == "GET":
            return mkwizard(step=_step)
        # If POST, fill the form
        wizard = mkwizard(step=_step, data=post)
        # If step valid
        if wizard.step_valid:
            return await wizard.next_step(req)
        # Else return with errors
        return wizard

    def cookie_banner(self, req, post: dict, cookie_policy: str = ""):
        # TODO: Use @fast.form decorator for this with a custom
        # cookie backend
        banner = ds.CookieBanner(
            self.service_name,
            ds.P("We use some essential cookies to make this service work."),
            cookie_form_link="/cookie-banner",
            # TODO: ATM, we only use essential cookies so no need
            # to show the banner with accept/reject options
            confirmation=True,
        )
        if req.method == "POST":
            val = post.get("cookies[additional]", None)
            hide = val == "hide"
            cookie_val = "hide" if hide else ""
            # Cookie should expire in a year
            cookie_age = 365*24*60*60
            cookie = fh.cookie("cookie_policy", cookie_val, max_age=cookie_age)
            return "" if hide else banner, cookie
        hide = "hide" in cookie_policy
        return "" if hide else banner

    def add_notification(self, session, content, success=False):
        notifications = session.get("notifications", [])
        notifications.append({"title": "Success" if success else "Important", "content": content})
        session["notifications"] = notifications
