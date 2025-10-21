from inspect import isawaitable
import logging
from functools import cache
from datetime import datetime
from typing import Callable

import httpx
import fasthtml.common as fh
from notifications_python_client.errors import HTTPError

from fast_gov_uk.design_system import Button, Field, Fieldset, ErrorSummary, A, Page

logger = logging.getLogger(__name__)


class BackendError(Exception):
    pass


class Backend:
    """
    Base class for backend processing.
    """

    async def process(self, request, name, data, *args, **kwargs):
        """Process the form using the backend function."""
        raise NotImplementedError("Subclasses must implement this method.")


class LogBackend(Backend):
    """
    Backend that logs form data.
    """

    async def process(self, request, name, data, *args, **kwargs):
        """Log the form data."""
        if isawaitable(data):
            data = await data
        logger.info(f"Form: '{name}' processed with: {data}.")


class DBBackend(Backend):
    """
    Backend that stores data in the DB.
    """

    def __init__(self, db, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = db

    def get_table(self):
        forms = self.db.t.forms
        if forms not in self.db.t:
            forms.create(id=int, name=str, created_on=datetime, data=dict, pk="id")
        return forms

    async def process(self, request, name, data, *args, **kwargs):
        if isawaitable(data):
            data = await data
        forms = self.get_table()
        Record = forms.dataclass()
        record = Record(name=name, created_on=datetime.now(), data=data)
        forms.insert(record)
        logger.info(f"Form: '{name}' saved with: {data}.")


class EmailBackend(Backend):
    """
    Backend that sends submitted forms to admin email.
    """

    def __init__(self, notify, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.notify = notify

    async def format(self, data):
        return "\n".join(f"* {key}: {val}" for key, val in data.items())

    async def process(self, request, name, data, *args, **kwargs):
        if isawaitable(data):
            data = await data
        formatted_data = await self.format(data)
        try:
            resp = await self.notify(form_name=name, form_data=formatted_data)
            logger.info(f"Email sent for form: {resp}")
        except HTTPError as e:
            logger.error(f"Error sending email for form '{name}': {e}")
            # User should not get the impression that the form
            # was submitted successfully if email failed
            raise


@cache
def _client(username, password):
    auth = httpx.BasicAuth(username=username, password=password)
    return httpx.Client(auth=auth)


class APIBackend(Backend):
    """
    Backend that sends submitted forms to an API.
    """

    def __init__(self, url, username, password, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = url
        self.username = username
        self.password = password

    async def process(self, request, name, data, *args, **kwargs):
        if isawaitable(data):
            data = await data
        data["form_name"] = name
        data["submitted_on"] = datetime.now()
        try:
            client = _client(self.username, self.password)
            client.post(self.url, data=data)
        except httpx.HTTPError as e:
            logger.error(f"Error sending request for form '{name}': {e}")
            # User should not get the impression that the form
            # was submitted successfully if email failed
            raise


class SessionBackend(Backend):
    """
    Backend that stores form data to the session.
    """

    async def process(self, request, name, data, *args, **kwargs):
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
        success_url: str | Callable = "/",
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
        return [item for item in self.items if isinstance(item, (Field, Fieldset))]

    @property
    def form_fields(self):
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
        if isinstance(self.success_url, Callable):
            self.success_url = self.success_url(self.data)
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
        fields_with_errors = [f for f in self.form_fields if f.error]
        if not fields_with_errors:
            return
        return ErrorSummary(
            "There is a problem", *[A(f.label, f"#{f._id}") for f in fields_with_errors]
        )

    @property
    def render(self) -> fh.FT:
        return fh.Form(
            self.error_summary(),
            *self.items,
            Button(self.cta),
            method=self.method,
            action=self.action,
            **self.kwargs,
        )

    def __ft__(self) -> fh.FT:
        return Page(self.render) if self.page else self.render


class Question:
    """
    An interface to the underlying _Question which is a Form. This is useful
    b/c all the Question objects that belong to the same flow will have the
    same name and so if we insist on directlry using _Question, the user will
    have to pass in the same name for each _Question which can be erorr-prone.
    """

    def __init__(self, *args, predicates: dict | None = None, **kwargs):
        self.args = args
        self.predicates = predicates
        self.kwargs = kwargs


class _Question(Form):
    """
    Subclass of Form to be used as a single Question page in GDS-style
    question pages.
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
    pass


class Wizard:
    """
    Implements the question-protocol aka Wizard i.e. forms that step
    through the fields one at a time.
    """

    def __init__(
        self,
        name: str,
        *questions: Question,
        backends: list[Backend] | None = None,
        success_url: str | Callable = "/",
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
        if isinstance(self.success_url, Callable):
            self.success_url = self.success_url(self.data)
        return fh.Redirect(self.success_url)

    @property
    def step_valid(self):
        return self.question.valid

    async def process(self, req, *args, **kwargs):
        data = req.session[self.name]["data"]
        try:
            for backend in self.backends:
                await backend.process(req, self.name, data, *args, **kwargs)
        except BackendError:
            raise
        return self.success

    async def next_step(self, req):
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
        return self.question
