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


class AddSessionBackend(Backend):
    """
    Backend that updates (instead of overwrite) session with form data.
    """

    async def process(self, request, name, data, *args, **kwargs):
        if isawaitable(data):
            data = await data
        session = request.session
        if name not in session:
            session[name] = {}
        session[name].update(await data)


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
                    yield fitem
            else:
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


class QuestionsFinished(Exception):
    pass


class Questions(Form):
    """
    Implements the question-protocol aka Wizard i.e. forms that step
    through the fields one at a time.
    """

    def __init__(self, *args, step: int = 0, predicates: dict | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.step = step
        self.predicates = predicates or {}

    @property
    def step_valid(self):
        field = self.fields[self.step]
        if isinstance(field, Fieldset):
            return all(not f.error for f in field.fields)
        return field.error == ""

    @property
    def next_step(self):
        data = self.data or {}
        next_step = self.step + 1
        if next_step >= len(self.fields):
            raise QuestionsFinished()
        next_field = self.fields[next_step]
        if next_field.name not in self.predicates:
            return next_step
        while next_step < len(self.fields):
            predicate = self.predicates.get(next_field.name, {})
            if all([data.get(k) == v for k, v in predicate.items()]):
                return next_step
            next_step = next_step + 1
            if next_step >= len(self.fields):
                raise QuestionsFinished()
            next_field = self.fields[next_step]
            continue

    def __ft__(self) -> fh.FT:
        try:
            field = self.fields[self.step]
        except IndexError:
            raise fh.HTTPException(status_code=404)
        return fh.Form(
            # We are not including ErrorSummary here
            # b/c most of the times, questions have a
            # single field and therefore its not necessary
            # to have an error summary
            field,
            Button(self.cta),
            method=self.method,
            action=self.action,
            **self.kwargs,
        )
