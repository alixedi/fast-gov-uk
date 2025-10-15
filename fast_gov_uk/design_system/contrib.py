from dataclasses import dataclass
from datetime import date
from email.utils import parseaddr
import re

import fasthtml.common as fh

from .inputs import TextInput, DateInput
from .navigation import Backlink


@dataclass
class EmailInput(TextInput):
    """
    EmailInput component - A TextInput field that
    validates the value as an email and sets the
    error attribute if invalid.
    """

    @TextInput.value.setter
    def value(self, value):
        self._value = value
        if self.required and not value:
            self.error = "This field is required."
            return
        _, email = parseaddr(self._value)
        if "@" not in email:
            self.error = "Value is not an email."


@dataclass
class NumberInput(TextInput):
    """
    NumberInput component - A TextInput field that
    validates the value as a number and sets the
    error attribute if invalid.
    """

    numeric: bool = True

    @TextInput.value.setter
    def value(self, value):
        self._value = value
        if self.required and not value:
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


@dataclass
class DecimalInput(TextInput):
    """
    DecimalInput component - A TextInput field that
    validates the value as a decimal and sets the
    error attribute if invalid.
    """

    numeric: bool = True

    @TextInput.value.setter
    def value(self, value):
        self._value = value
        if self.required and not value:
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


@dataclass
class GBPInput(DecimalInput):
    """
    GBPInput because its such a common ask.
    """
    prefix : str = "£"


def BacklinkJS(text: str = "Back", inverse: bool = False) -> fh.FT:
    """
    Backlink component based on js
    """
    return Backlink("javascript:history.back()", text=text, inverse=inverse)


@dataclass
class RegexInput(TextInput):
    """
    RegexInput component - A TextInput field that
    validates the value againt a regex and sets the
    error attribute if invalid.
    """

    regex: str = ".*"

    @TextInput.value.setter
    def value(self, value):
        self._value = value
        if self.required and not value:
            self.error = "This field is required."
            return
        pattern = re.compile(self.regex)
        if not pattern.match(self._value):
            self.error = 'Value does not match the required format.'


@dataclass
class PastDateInput(DateInput):

    @DateInput.value.setter
    def value(self, value):
        self._value = value or ("", "", "")
        day, month, year = self._value
        if self.required and (not day or not month or not year):
            self.error = "This field is required."
            return
        try:
            day, month, year = int(day), int(month), int(year)
            _date = date(day=day, month=month, year=year)
            if _date > date.today():
                self.error = "The date must be in the past."
        except (ValueError, TypeError):
            self.error = "Invalid values."



@dataclass
class FutureDateInput(DateInput):

    @DateInput.value.setter
    def value(self, value):
        self._value = value or ("", "", "")
        day, month, year = self._value
        if self.required and (not day or not month or not year):
            self.error = "This field is required."
            return
        try:
            day, month, year = int(day), int(month), int(year)
            _date = date(day=day, month=month, year=year)
            if _date < date.today():
                self.error = "The date must be in the future."
        except (ValueError, TypeError):
            self.error = "Invalid values."
