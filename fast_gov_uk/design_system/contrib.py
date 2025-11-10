from datetime import date
from email.utils import parseaddr
import re

import fasthtml.common as fh

from .inputs import TextInput, DateInput
from .navigation import BackLink


class EmailInput(TextInput):
    """
    EmailInput component.

    Validates the value as an email and sets the error attribute if invalid.
    """

    @TextInput.value.setter
    def value(self, value):
        self._value = value
        if self.required:
            if not value:
                self.error = "This field is required."
                return
            _, email = parseaddr(self._value)
            if "@" not in email:
                self.error = "Value is not an email."


class NumberInput(TextInput):
    """
    NumberInput component.

    Validates the value as a number and sets the error attribute if invalid.
    """

    def __init__(self, *args, numeric: bool = True, **kwargs):
        super().__init__(*args, **kwargs)
        self.numeric = numeric

    @TextInput.value.setter
    def value(self, value):
        self._value = value
        if self.required:
            if not value:
                self.error = "This field is required."
                return
            try:
                _ = int(self._value)
            except (ValueError, TypeError):
                self.error = "Value is not a number."

    @property
    async def clean(self):
        if not self.value:
            return None
        number = int(self.value)
        return number


class DecimalInput(TextInput):
    """
    DecimalInput component.

    Validates the value as a decimal and sets the error attribute if invalid.
    """

    def __init__(self, *args, numeric: bool = True, **kwargs):
        super().__init__(*args, **kwargs)
        self.numeric = numeric

    @TextInput.value.setter
    def value(self, value):
        self._value = value
        if self.required:
            if not value:
                self.error = "This field is required."
                return
            try:
                _ = float(self._value)
            except (ValueError, TypeError):
                self.error = "Value is not a number."

    @property
    async def clean(self):
        if not self.value:
            return None
        number = float(self.value)
        return number


class GBPInput(DecimalInput):
    """
    GBPInput component.

    A DecimalInput with a currency prefix, commonly used for GBP (£).
    """

    def __init__(self, *args, prefix: str = "£", **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = prefix


def BackLinkJS(text: str = "Back", inverse: bool = False) -> fh.FT:
    """
    BackLink component based on JavaScript.

    Args:
        text (str, optional): The text for the backlink. Defaults to "Back".
        inverse (bool, optional): Use inverse style. Defaults to False.

    Returns:
        FT: A FastHTML BackLink component.
    """
    return BackLink("javascript:history.back()", text=text, inverse=inverse)


class RegexInput(TextInput):
    """
    RegexInput component.

    Validates the value against a regex and sets the error attribute if invalid.
    """

    def __init__(self, *args, regex: str = ".*", **kwargs):
        super().__init__(*args, **kwargs)
        self.regex = regex

    @TextInput.value.setter
    def value(self, value):
        self._value = value
        if self.required:
            if not value:
                self.error = "This field is required."
                return
            pattern = re.compile(self.regex)
            if not pattern.match(self._value):
                self.error = 'Value does not match the required format.'


class PastDateInput(DateInput):
    """
    PastDateInput component.

    Validates that the date is in the past.
    """

    @DateInput.value.setter
    def value(self, value):
        self._value = value or ("", "", "")
        day, month, year = self._value
        if self.required:
            if (not day or not month or not year):
                self.error = "This field is required."
                return
            try:
                day, month, year = int(day), int(month), int(year)
                _date = date(day=day, month=month, year=year)
                if _date > date.today():
                    self.error = "The date must be in the past."
            except (ValueError, TypeError):
                self.error = "Invalid values."


class FutureDateInput(DateInput):
    """
    FutureDateInput component.

    Validates that the date is in the future.
    """

    @DateInput.value.setter
    def value(self, value):
        self._value = value or ("", "", "")
        day, month, year = self._value
        if self.required:
            if (not day or not month or not year):
                self.error = "This field is required."
                return
            try:
                day, month, year = int(day), int(month), int(year)
                _date = date(day=day, month=month, year=year)
                if _date < date.today():
                    self.error = "The date must be in the future."
            except (ValueError, TypeError):
                self.error = "Invalid values."
