"""
These components are not directly part of the GOV.UK Design System but are used often in many
applications and services.

E.g. EmailInput and GBPInput can be used in forms to collect emails and GBP values. NumberInput
and DecimalInput can be used to validate if the user filled-in an integer or a decimal number
in a field. PastDateInput and FutureDateInput can validate if the date entered by the user is
in the past and the future respectively etc.

This module also serves as an example on how to extend/modify the base fields.
"""

from datetime import date
from email.utils import parseaddr
import re

import fasthtml.common as fh

from .inputs import TextInput, DateInput
from .navigation import BackLink


class EmailInput(TextInput):
    """
    GOV.UK TextInput component with some basic email validation using Python's
    built-in `email.utils.parseaddr`.

    If your workflow needs to ensure that the email actually belongs to the user,
    you might want to send them a confirmation email etc.

    Examples:

        >>> email = ds.EmailInput("email")
        >>> email.value = "test"
        >>> email.error
        'Value is not an email'
        >>> email.value = "test@test"
        >>> email.error
        ''
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
    GOV.UK TextInput component that validates number input using the `int()` typecast.

    Examples:

        >>> number = ds.NumberInput("number")
        >>> number.value = "x"
        >>> number.error
        'Value is not an number'
        >>> number.value = "3.4"
        >>> number.error
        'Value is not an number'
        >>> number.value = "10"
        >>> number.error
        ''
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
    GOV.UK TextInput component that validates decimal input using the `float()` typecast.

    Examples:

        >>> decimal = ds.DecimalInput("decimal")
        >>> decimal.value = "x"
        >>> decimal.error
        'Value is not an number'
        >>> decimal.value = "10"
        >>> decimal.error
        ''
        >>> decimal.value = "3.4"
        >>> decimal.error
        ''
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
    A DecimalInput with a currency prefix, commonly used for GBP (£) field
    in GOV.UK services.

    Examples:

        >>> gbp = ds.GBPInput("gbp")
        # Input with £ prefix: £ ____
        >>> gbp.value = "x"
        >>> gbp.error
        'Value is not an number'
        >>> gbp.value = "10"
        >>> gbp.error
        ''
        >>> gbp.value = "3.4"
        >>> gbp.error
        ''
    """

    def __init__(self, *args, prefix: str = "£", **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = prefix


def BackLinkJS(text: str = "Back", inverse: bool = False) -> fh.FT:
    """
    An implmentation of `GOV.UK back link`_ component that uses JavaScript to go back one page
    in the browser.

    This is often useful in cases where it is clunky to maintain state for the current step
    in a multi-step journey on the server.

    Note that this would not work if a user has `javascript` disabled in their browser.

    Examples:

        >>> back = ds.BackLinkJS()
        >>> str(back)
        '<a href="javascript:history.back()" class="govuk-back-link">Back</a>'

    Args:
        text (str, optional): The text for the backlink. Defaults to "Back".
        inverse (bool, optional): Use inverse style. Defaults to False.

    Returns:
        FT: A FastHTML BackLink component.

    .. _GOV.UK back link: https://design-system.service.gov.uk/components/back-link/
    """
    return BackLink("javascript:history.back()", text=text, inverse=inverse)


class RegexInput(TextInput):
    """
    GOV.UK TextInput component that accepts a `regex` string to validate user input.

    This can be handy for e.g. postcodes - https://stackoverflow.com/a/69806181/1182202.

    Examples:

        >>> re = ds.RegexInput("postcode", regex="(blue|white|red)")
        >>> re.value="white"
        >>> re.error
        ''
        >>> re.value="green"
        >>> re.error
        'Value does not match the required format.'
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
    GOV.UK DateInput component that only accepts a date in the past.

    This is useful for collecting date of birth etc.

    Examples:

        >>> past = ds.PastDateInput("past")
        >>> past.value=["1", "1", "2000"]
        >>> past.error
        ''
        >>> past.value = ["1", "1", "3000"]
        >>> past.error
        'The date must be in the past.'
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
    GOV.UK DateInput component that only accepts a date in the future.

    This is useful for when a service allows users to e.g. booking something in advance.

    Examples:

        >>> future = ds.FutureDateInput("future")
        >>> future.value = ["1", "1", "3000"]
        >>> future.error
        ''
        >>> future.value=["1", "1", "2000"]
        >>> future.error
        'The date must be in the future.'
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
