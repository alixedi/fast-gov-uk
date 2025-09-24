from dataclasses import dataclass
from email.utils import parseaddr

from .inputs import TextInput


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

    numeric = True

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

    numeric = True

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
