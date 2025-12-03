from inspect import isawaitable
import logging
from functools import cache
from datetime import datetime

import httpx
import fasthtml.common as fh

from fast_gov_uk.design_system import Button, Field, Fieldset, ErrorSummary, A, Page

logger = logging.getLogger(__name__)


class BackendError(Exception):
    """
    Exception raised for errors in backend processing.
    """
    pass


class Backend:
    """
    Base class for backend processing.
    """

    async def process(self, request, name, data, *args, **kwargs):
        """
        Process the form using the backend function.

        Args:
            request: The HTTP request object.
            name (str): Name of the form.
            data (dict|awaitable): Cleaned form data.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        raise NotImplementedError("Subclasses must implement this method.")


class LogBackend(Backend):
    """
    Backend that logs form data. This is mainly useful for debugging.

    Example:

        .. code-block:: python

            @fast.form
            def email(data=None):
                forms.Form(
                    "email",
                    ds.EmailInput("email"),
                    backends=[forms.LogBackend()],
                    data=data,
                )
    """

    async def process(self, request, name, data, *args, **kwargs):
        """
        Log the form data.

        Args:
            request: The HTTP request object.
            name (str): Name of the form.
            data (dict|awaitable): Cleaned form data.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        if isawaitable(data):
            data = await data
        logger.info(f"Form: '{name}' processed with: {data}.")


class DBBackend(Backend):
    """
    Backend that stores data in the DB. Requires a `db` instance.

    Example:

        .. code-block:: python

            @fast.form
            def email(data=None):
                forms.Form(
                    "email",
                    ds.EmailInput("email"),
                    backends=[forms.DBBackend(db=fast.db)],
                    data=data,
                )

    The data is stored in the "forms" table in the given database.
    It has the following format -

        - **name (str)**: name of the form e.g. "email" for our example
        - **created_on (datetime)**: Timestamp for when the form was processed
        - **data (dict)**: JSON blob of the form data e.g. ``{"email": ".."}`` for our example

    In order to use this backend, you need to pass in ``DATABASE_URL`` in your settings
    when instantiating ``Fast`` object, like so -

    .. code-block:: python

        fast = Fast({
            "DATABASE_URL": "service.db",
        })

    This will create a sqlite database called ``service.db`` in your root directory and the
    ``DBBackend`` will store the data submitted in forms to the same database.

    Args:
        db: Database instance.
    """

    def __init__(self, db, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = db

    def get_table(self):
        """
        Get or create the forms table.

        Returns:
            Table: The forms table.
        """
        forms = self.db.t.forms
        if forms not in self.db.t:
            forms.create(id=int, name=str, created_on=datetime, data=dict, pk="id")
        return forms

    async def process(self, request, name, data, *args, **kwargs):
        """
        Store the form data in the DB.

        Args:
            request: The HTTP request object.
            name (str): Name of the form.
            data (dict|awaitable): Cleaned form data.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        if isawaitable(data):
            data = await data
        forms = self.get_table()
        Record = forms.dataclass()
        record = Record(name=name, created_on=datetime.now(), data=data)
        forms.insert(record)
        logger.info(f"Form: '{name}' saved with: {data}.")


class EmailBackend(Backend):
    """
    Backend that sends submitted forms to the given email address.

    Example:

        .. code-block:: python

            @fast.form
            def email(data=None):
                forms.Form(
                    "email",
                    ds.EmailInput("email"),
                    backends=[forms.EmailBackend(
                        fast.notify("<notify_template_id>", "test@test.com")
                    )],
                    data=data,
                )

    In order to use this backend, you need to -

    1. create an account for your service in `GOV.UK Notify <https://www.notifications.service.gov.uk>`_
    2. create an API key under "API Integration" and finally
    3. pass-in your API key when instantiating ``Fast`` using environment variables like so -

    .. code-block:: python

        from os import environ as env

        fast = Fast({
            "NOTIFY_API_KEY": env.get("NOTIFY_API_KEY"),
        })

    You would also need to create an email template in your GOV.UK Notify service
    account -

    ::

        ((service_name))
        Someone submitted the form: “((form_name))” with the following data -
        ((form_data))

    Args:
        notify: Notification function to send emails.
    """

    def __init__(self, notify, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.notify = notify

    async def format(self, data):
        """
        Format the form data for email.
        """
        return "\n".join(f"* {key}: {val}" for key, val in data.items())

    async def process(self, request, name, data, *args, **kwargs):
        """
        Send the form data via email.

        Args:
            request: The HTTP request object.
            name (str): Name of the form.
            data (dict|awaitable): Cleaned form data.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        if isawaitable(data):
            data = await data
        formatted_data = await self.format(data)
        resp = await self.notify(form_name=name, form_data=formatted_data)
        logger.info(f"Email sent for form: {resp}")


@cache
def _client(username, password):
    """
    Create an HTTP client with basic auth.

    Args:
        username (str): Username for basic auth.
        password (str): Password for basic auth.

    Returns:
        httpx.Client: HTTP client with basic auth.
    """
    auth = httpx.BasicAuth(username=username, password=password)
    return httpx.Client(auth=auth)


class APIBackend(Backend):
    """
    Backend that sends submitted forms to an API.

    Example:

        .. code-block:: python

            @fast.form
            def email(data=None):
                forms.Form(
                    "email",
                    ds.EmailInput("email"),
                    backends=[forms.APIBackend(
                        url="https://test.com",
                        username="test_user",
                        password="test_password"
                    )],
                    data=data,
                )

    The format of the payload is -

    ::

        {
            "form_name": "email",
            "submitted_on": <datetime when the form was processed>,
            "email": <email address submitted by the user>,
            ...
        }

    This implementation is more-or-less a placeholder, an exemplar of how
    you would implement an API backend for an API with basic HTTP auth. It
    is likely that **your** API might use different authentication or indeed
    a different format for the payload. If this is the case, rip-off this
    code to write your own API backend.

    Args:
        url (str): API endpoint URL.
        username (str): Username for basic auth.
        password (str): Password for basic auth.
    """

    def __init__(self, url, username, password, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = url
        self.username = username
        self.password = password

    async def process(self, request, name, data, *args, **kwargs):
        """
        Send the form data to the API.

        Args:
            request: The HTTP request object.
            name (str): Name of the form.
            data (dict|awaitable): Cleaned form data.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        if isawaitable(data):
            data = await data
        data["form_name"] = name
        data["submitted_on"] = datetime.now()
        client = _client(self.username, self.password)
        client.post(self.url, data=data)


class SessionBackend(Backend):
    """
    Backend that stores form data to the session cookie.

    Example:

        .. code-block:: python

            @fast.form
            def email(data=None):
                forms.Form(
                    "email",
                    ds.EmailInput("email"),
                    backends=[forms.SessionBackend()],
                    data=data,
                )

    The format for data persisted in the session cookie for our example would be -

    ::

        {"email": {"email": "test@test.com"}}

    """

    async def process(self, request, name, data, *args, **kwargs):
        """
        Store the form data in the session.

        Args:
            request: The HTTP request object.
            name (str): Name of the form.
            data (dict|awaitable): Cleaned form data.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        if isawaitable(data):
            data = await data
        session = request.session
        session[name] = data


class QuestionBackend(Backend):
    """
    Backend that appends data as well as values to the session.
    Used by question pages to store state as the user progress
    from one page to another.
    """

    async def process(self, request, name, data, *args, **kwargs):
        """
        Append the question data in the session.

        Args:
            request: The HTTP request object.
            name (str): Name of the form.
            data (dict|awaitable): Cleaned form data.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        if isawaitable(data):
            data = await data
        session = request.session
        if name not in session:
            session[name] = {"values": {}, "data": {}}
        session[name]["values"].update(data["values"])
        session[name]["data"].update(data["data"])


class Form:
    """
    Wrapper around fh Form for consistency.

    Examples:

        >>> form = Form(
        ...     "contact-form",
        ...     Field("name", label="Name"),
        ...     Field("email", label="Email", type="email"),
        ...     backends=[LogBackend()],
        ...     success_url="/thank-you",
        ...     cta="Send",
        ... )

    Args:
        name (str): Name of the Form.
        backends (list): List of backends to process submitted data.
        success_url (str or function): Redirect URL after form is processed.
        items (list): Items in the Form.
        method (str): HTTP method for the Form. Default: "POST".
        action (str): Action URL for the Form. Default: "".
        cta (str): Label for Submit button.
        data (dict|None): Initial data for the Form. Default: None.
        page (bool): Render form in a page? Default: True.
        kwargs (dict): kwargs for underlying fh.Form.
    """

    def __init__(
        self,
        name: str,
        *items,
        backends: list[Backend] | None = None,
        success_url: str = "/",
        method: str = "POST",
        action: str = "",
        cta: str = "Submit",
        data: dict | None = None,
        page: bool = True,
        **kwargs,
    ):
        self.name = name
        self.items = items
        self.backends = backends or [SessionBackend()]
        self.success_url = success_url
        self.method = method
        self.action = action
        self.cta = cta
        self.data = data
        self.page = page
        self.kwargs = kwargs
        if not self.fields:
            raise ValueError(
                "Your Form definition does not seem to have any Field or Fieldset component at the root level."
            )
        self.bind()

    @property
    def fields(self):
        """
        Get all Field and Fieldset items in the form.
        """
        return [item for item in self.items if isinstance(item, (Field, Fieldset))]

    @property
    def form_fields(self):
        """
        Get all Field items in the form, including those inside Fieldsets.
        Yields:
            Field: Field items in the form.
        """
        for item in self.fields:
            if isinstance(item, Fieldset):
                for fitem in item.fields:
                    if isinstance(fitem, Field):
                        yield fitem
            else:
                if isinstance(item, Field):
                    yield item

    @property
    def errors(self) -> dict:
        """
        Get the error messages from the field.
        Returns:
            dict: Error messages from fields.
        """
        return {field.name: field.error for field in self.form_fields if field.error}

    @property
    def valid(self) -> bool:
        """
        Check if the form is valid.
        Returns:
            bool: True if all fields are valid, False otherwise.
        """
        return all(field.error == "" for field in self.form_fields)

    @property
    async def clean(self) -> dict:
        """
        Calls clean function in respective fields to get cleaned
        field values. E.g. A cleaned value for DateInput would be
        a date object instead of ["10", "10", "2000"].
        """
        return {f.name: await f.clean for f in self.form_fields}

    def bind(self):
        """
        Bind data to the form fields.
        """
        # `if self.data:` doesn't work b/c the form could
        # have a single radio field and submitted empty
        # with POST dict = {}
        if self.data is not None:
            for field in self.form_fields:
                field.value = self.data.get(field.name, "")

    @property
    def success(self):
        """
        Get the success redirect response.
        Returns:
            fh.Redirect: Redirect response to success URL.
        """
        return fh.Redirect(self.success_url)

    async def process(self, req, *args, **kwargs):
        """
        Call the process methods on form backends.
        """
        try:
            for backend in self.backends:
                await backend.process(req, self.name, self.clean, *args, **kwargs)
        except BackendError:
            raise
        return self.success

    def error_summary(self):
        """
        Generate an error summary if there are field errors.
        Returns:
            ErrorSummary|None: Error summary component or None if no errors.
        """
        fields_with_errors = [f for f in self.form_fields if f.error]
        if not fields_with_errors:
            return
        return ErrorSummary(
            "There is a problem", *[A(f.label, f"#{f._id}") for f in fields_with_errors]
        )

    @property
    def render(self) -> fh.FT:
        """
        Render the form with error summary and submit button.
        Returns:
            fh.FT: Rendered form component.
        """
        return fh.Form(
            self.error_summary(),
            *self.items,
            Button(self.cta),
            method=self.method,
            action=self.action,
            **self.kwargs,
        )

    def __ft__(self) -> fh.FT:
        """
        Render the form, optionally wrapped in a Page.
        Returns:
            fh.FT: Rendered form or page component.
        """
        return Page(self.render) if self.page else self.render


class Question:
    """
    An interface to the underlying _Question which is a Form. This is useful
    b/c all the Question objects that belong to the same flow will have the
    same name and so if we insist on directlry using _Question, the user will
    have to pass in the same name for each _Question which can be erorr-prone.

    Examples:

        >>> Question(
        ...     ds.H1("Thank you for your interest"),
        ...     ds.P("Please answer the following questions:"),
        ...     ds.NumberInput("age", label="What is your age?"),
        ... )

    Args:
        args: Positional arguments for the _Question.
        predicates (dict|None): Predicates to determine if this question
            should be shown based on previous answers.
        kwargs: Keyword arguments for the _Question.
    """

    def __init__(self, *args, predicates: dict | None = None, **kwargs):
        self.args = args
        self.predicates = predicates
        self.kwargs = kwargs


class _Question(Form):
    """
    Subclass of Form to be used as a single Question page in GDS-style
    question pages.

    You should not instantiate this class directly but rather use
    the Question interface.

    Args:
        args: Positional arguments for the Form.
        cta (str): Label for Submit button.
        kwargs: Keyword arguments for the Form.
    """

    def __init__(self, *args, cta: str = "Continue", **kwargs):
        super().__init__(
            *args,
            cta=cta,
            backends=[QuestionBackend()],
            **kwargs
        )

    @property
    async def clean(self) -> dict:
        """
        Override the form clean function to not only save cleaned
        data from fields but also raw values. The raw values are
        used to determind control flow through question pages.
        """
        values = {f.name: f.value for f in self.form_fields}
        data = {f.name: await f.clean for f in self.form_fields}
        return {"values": values, "data": data}


class QuestionsFinished(Exception):
    """
    Exception raised when there are no more questions left in the wizard.
    """
    pass


class Wizard:
    """
    Implements the question-protocol aka Wizard i.e. forms that step
    through the fields one at a time.

    Examples:
        >>> wizard = Wizard(
        ...     "example-wizard",
        ...     Question(
        ...         ds.H1("Thank you for your interest"),
        ...         ds.P("Please answer the following questions:"),
        ...         ds.NumberInput("age", label="What is your age?"),
        ...     ),
        ...     Question(
        ...         ds.TextInput("name", label="What is your name?"),
        ...         predicates={"age": "18"},
        ...     ),
        ...     backends=[LogBackend()],
        ...     success_url="/thank-you",
        ... )

    Args:
        name (str): Name of the Wizard.
        questions (list): List of Question objects.
        backends (list): List of backends to process submitted data.
        success_url (str): Redirect URL after wizard is completed.
        step (int): Current step in the wizard. Default: 0.
        data (dict|None): Initial data for the current question. Default: None.
    """

    def __init__(
        self,
        name: str,
        *questions: Question,
        backends: list[Backend] | None = None,
        success_url: str = "/",
        step: int = 0,
        data: dict | None = None
    ):
        self.name = name
        self.questions = questions
        self.backends = backends or [SessionBackend()]
        self.success_url = success_url
        self.step = step
        self.data = data
        try:
            question = self.questions[self.step]
            self.question = _Question(
                name,
                *question.args,
                **question.kwargs,
                data=data,
            )
        except IndexError:
            raise fh.HTTPException(status_code=404)

    @property
    def success(self):
        """
        Get the success redirect response.
        """
        return fh.Redirect(self.success_url)

    @property
    def step_valid(self):
        """
        Check if the current step/question is valid.
        """
        return self.question.valid

    async def process(self, req, *args, **kwargs):
        """
        Call the process methods on wizard backends.
        Args:
            req: The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        Returns:
            fh.Redirect: Redirect response to success URL.
        """
        data = req.session[self.name]["data"]
        try:
            for backend in self.backends:
                await backend.process(req, self.name, data, *args, **kwargs)
        except BackendError:
            raise
        return self.success

    async def next_step(self, req):
        """
        Process the current question and determine the next step
        in the wizard based on predicates.
        Args:
            req: The HTTP request object.
        Returns:
            fh.Redirect: Redirect response to the next question or success URL.
        """
        await self.question.process(req)
        data = req.session[self.name]["values"]
        next_step = self.step + 1

        while next_step < len(self.questions):
            next_field = self.questions[next_step]
            predicates = next_field.predicates or {}

            if not predicates or all(data.get(k) == v for k, v in predicates.items()):
                return fh.Redirect(f'/wizards/{req.path_params["name"]}/{next_step}')

            next_step += 1

        return await self.process(req)


    def __ft__(self) -> _Question:
        """
        Render the current question.
        Returns:
            _Question: The current question form.
        """
        return self.question
