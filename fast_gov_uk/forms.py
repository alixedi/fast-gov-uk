import logging
from dataclasses import dataclass
from datetime import datetime

import fasthtml.common as fh

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
    def errors(self) -> dict:
        """
        Get the error messages from the field.
        Returns:
            dict: Error messages from fields.
        """
        return {field.name: field.error for field in self.fields if field.error}

    @property
    def valid(self) -> bool:
        """
        Check if the form is valid.
        Returns:
            bool: True if all fields are valid, False otherwise.
        """
        return all(field.error == "" for field in self.fields)

    @property
    async def clean(self) -> dict:
        """
        Calls clean function in respective fields to get cleaned
        field values. E.g. A cleaned value for DateInput would be
        a date object instead of ["10", "10", "2000"].
        """
        return {
            f.name: await f.clean
            for f in self.fields
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
            for field in self.fields:
                field.value = self.data.get(field.name, "")

    def __ft__(self) -> fh.FT:
        return fh.Form(
            Fieldset(self.title, *self.fields),
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
