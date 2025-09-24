import logging
from functools import cache
from dataclasses import dataclass
from datetime import datetime

import httpx
import fasthtml.common as fh
from notifications_python_client.errors import HTTPError

from fast_gov_uk.design_system import Button, Field, Fieldset

logger = logging.getLogger(__name__)


class Backend:
    """
    Base class for backend processing.
    """

    def success(self):
        success_url = getattr(self, "success_url")
        return fh.Redirect(success_url)

    def process(self):
        """Process the form using the backend function."""
        raise NotImplementedError("Subclasses must implement this method.")


@dataclass
class LogBackend(Backend):
    """
    Backend that logs form data.
    """

    def process(self):
        """Log the form data."""
        title = getattr(self, "title")
        data = getattr(self, "data")
        logger.info(f"Form: '{title}' processed with: {data}.")
        return self.success()


class DBBackend(Backend):
    """
    Backend that stores data in the DB.
    """

    def get_table(self):
        db = getattr(self, "db")
        forms = db.t.forms
        if forms not in db.t:
            forms.create(id=int, title=str, created_on=datetime, data=dict, pk="id")
        return forms

    async def process(self):
        forms = self.get_table()
        Record = forms.dataclass()
        title = getattr(self, "title")
        now = datetime.now()
        data = await getattr(self, "clean")
        record = Record(title=title, created_on=now, data=data)
        forms.insert(record)
        logger.info(f"Form: '{title}' saved with: {data}.")
        return self.success()


class EmailBackend(Backend):
    """
    Backend that sends submitted forms to admin email.
    """

    async def format(self, data):
        return "\n".join(
            f"* {key}: {val}"
            for key, val in data.items()
        )

    async def process(self):
        notify = getattr(self, "notify")
        title = getattr(self, "title")
        data = await getattr(self, "clean")
        formatted_data = await self.format(data)
        try:
            resp = await notify(form_name=title, form_data=formatted_data)
            logger.info(f"Email sent for form: {resp}")
        except HTTPError as e:
            logger.error(f"Error sending email for form '{title}': {e}")
            # User should not get the impression that the form
            # was submitted successfully if email failed
            raise
        return self.success()


@cache
def _client(username, password):
    auth = httpx.BasicAuth(username=username, password=password)
    return httpx.Client(auth=auth)


class APIBackend(Backend):
    """
    Backend that sends submitted forms to an API.
    """
    async def process(self):
        url = getattr(self, "url")
        username = getattr(self, "username")
        password = getattr(self, "password")
        title = getattr(self, "title")
        data = await getattr(self, "clean")
        data["form_name"] = title
        data["submitted_on"] = datetime.now()
        try:
            client = _client(username, password)
            client.post(url, data=data)
        except httpx.HTTPError as e:
            logger.error(f"Error sending request for form '{title}': {e}")
            # User should not get the impression that the form
            # was submitted successfully if email failed
            raise
        return self.success()


class Form:
    """
    Wrapper around fh Form for consistency.
    Args:
        title (str): Title of the Form.
        fields: Fields for the Form.
        method (str): HTTP method for the Form. Default: "POST".
        action (str): Action URL for the Form. Default: "".
        cta (str): Label for Submit button.
        data (dict|None): Initial data for the Form. Default: None.
        kwargs (dict): kwargs for Form.
    """

    def __init__(
        self,
        title: str,
        fields: list[Field],
        success_url: str,
        method: str = "POST",
        action: str = "",
        cta: str = "Submit",
        data: dict | None = None,
        **kwargs,
    ):
        self.title = title
        self.fields = fields
        self.success_url = success_url
        self.method = method
        self.action = action
        self.cta = cta
        self.data = data
        self.kwargs = kwargs
        self.bind()

    @property
    def form_fields(self):
        for field in self.fields:
            if isinstance(field, Fieldset):
                for field in field.fields:
                    yield field
            else:
                yield field

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
        return {
            f.name: await f.clean
            for f in self.form_fields
        }

    def bind(self):
        """
        Bind data to the form fields.
        Args:
            data (dict): Data to bind to the form fields.
        """
        # `if self.data:` doesn't work b/c the form could
        # have a single radio field and submitted empty
        # with POST dict = {}
        if self.data is not None:
            for field in self.form_fields:
                field.value = self.data.get(field.name, "")

    def __ft__(self) -> fh.FT:
        return fh.Form(
            Fieldset(*self.fields, legend=self.title),
            Button(self.cta),
            method=self.method,
            action=self.action,
            **self.kwargs,
        )


class LogForm(Form, LogBackend):
    pass


class DBForm(Form, DBBackend):
    def __init__(self, db, *args, **kwargs):
        self.db = db
        super().__init__(*args, **kwargs)


class EmailForm(Form, EmailBackend):
    def __init__(self, notify, *args, **kwargs):
        self.notify = notify
        super().__init__(*args, **kwargs)


class APIForm(Form, APIBackend):
    def __init__(self, url, username, password, *args, **kwargs):
        self.url = url
        self.username = username
        self.password = password
        super().__init__(*args, **kwargs)
