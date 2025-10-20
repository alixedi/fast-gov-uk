import fasthtml.common as fh
from notifications_python_client import notifications as notify

import fast_gov_uk.design_system as ds
from fast_gov_uk.demo import demo
from fast_gov_uk.forms import QuestionsFinished


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
    return fh.FileResponse(f"assets/{fname}.{ext}")


class Fast(fh.FastHTML):
    def __init__(self, settings, *args, **kwargs):
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
        # Service name
        self.service_name = settings["SERVICE_NAME"]
        # Set up Database
        db_url = settings["DATABASE_URL"]
        self.db = fh.database(db_url)
        # Set up flag for whether we are in dev mode
        self.dev = settings["DEV_MODE"]
        # Initialize form registry
        self.forms = {}
        # Initialise wizard registry
        self.questions = {}
        # Set up routes
        if self.dev:
            self.route("/demo")(demo)
        self.route("/{fname:path}.{ext:static}")(assets)
        self.route("/form/{name}", methods=["GET", "POST"])(self.process_form)
        self.route("/questions/{name}/{step}", methods=["GET", "POST"])(
            self.process_questions
        )
        self.route("/cookie-banner", methods=["GET", "POST"])(self.cookie_banner)
        self.route("/notifications")(self.notifications)
        # Initialise notify client
        notify_key = settings["NOTIFY_API_KEY"]
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

    def question(self, url=None):
        def question_decorator(func):
            _url = url or func.__name__
            self.questions[_url] = func
            return func

        if callable(url):
            # Used as @app.form
            func = url
            url = None
            return question_decorator(func)
        # Used as @app.question("/some-url")
        return question_decorator

    async def process_form(self, req, name: str, post: dict):
        mkform = self.forms.get(name, None)
        if not mkform:
            raise fh.HTTPException(status_code=404)
        # If GET, just return the form
        if req.method == "GET":
            form = mkform()
            return form
        # If POST, fill the form
        form = mkform(post)
        # If valid, process
        if form.valid:
            return await form.process(req)
        # Else return with errors
        return form

    async def process_questions(
        self, req, session: dict, name: str, step: str, post: dict
    ):
        try:
            mk_question = self.questions[name]
            _step = int(step or "0")
        except (KeyError, ValueError):
            raise fh.HTTPException(status_code=404)
        # If GET, just return the form
        if req.method == "GET":
            question = mk_question(step=_step)
            return question
        # If POST, fill the form
        question = mk_question(step=_step, data=post)
        # If step valid
        if question.step_valid:
            return await question.next_step(req)
        # Else return with errors
        return question

    def cookie_banner(self, req, post: dict, cookie_policy: str = ""):
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

    def notifications(self, session):
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
