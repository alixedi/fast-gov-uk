from datetime import date
from enum import Enum
from pathlib import Path
from typing import List

import fasthtml.common as fh

from .typography import H2, A
from .utils import mkid


def Label(
    field_id: str,
    text: str,
    heading: str = "",
    required: bool = True,
    extra_cls: str = "",
) -> fh.FT:
    """
    Label component. Generally attached to a Field.

    Args:
        field_id (str): HTML id of the field this label is for.
        text (str): Text to be displayed in the label.
        heading (str, optional): Heading size. Defaults to "".
        required (bool, optional): Is this for a field that is required? Defaults to True.
        extra_cls (str, optional): Extra CSS classes. Defaults to "".

    Returns:
        FT: A FastHTML label component.
    """
    optional = "" if required else " (Optional)"
    heading_cls = f" govuk-label--{heading}" if heading else ""
    label = fh.Label(
        f"{text}{optional}", cls=f"govuk-label{heading_cls}{extra_cls}", _for=field_id
    )
    if heading:
        label = fh.H1(label, cls="govuk-label-wrapper")
    return label


def Hint(field_id: str, text: str, extra_cls: str = "") -> fh.FT:
    """
    Hint component. Generally attached to a Field.

    Args:
        field_id (str): HTML id of the field this hint is for.
        text (str): Text to be displayed as hint.
        extra_cls (str, optional): Extra CSS classes. Defaults to "".

    Returns:
        FT: A FastHTML hint component.
    """
    return fh.Div(text, cls=f"govuk-hint{extra_cls}", id=f"{field_id}-hint")


def Error(field_id: str, text: str, extra_cls: str = "") -> fh.FT:
    """
    Error component. Generally attached to a Field.

    Args:
        field_id (str): HTML id of the field this error is for.
        text (str): Text to be displayed as error.
        extra_cls (str, optional): Extra CSS classes. Defaults to "".

    Returns:
        FT: A FastHTML error component.
    """
    return fh.P(
        fh.Span("Error: ", cls="govuk-visually-hidden"),
        text,
        cls=f"govuk-error-message{extra_cls}",
        id=f"{field_id}-error",
    )


class AbstractField:
    pass


class Field(AbstractField):
    """
    Baseclass for form fields.

    Args:
        name (str): The name of the field.
        label (str, optional): Label for the field. Defaults to "".
        hint (str, optional): Hint for the field. Defaults to "".
        error (str, optional): Error message for the field. Defaults to "".
        heading (str, optional): Heading size. Defaults to "".
        required (bool, optional): Is this field required? Defaults to True.
        **kwargs: Additional keyword arguments.
    """

    def __init__(
        self,
        name: str,
        label: str = "",
        hint: str = "",
        error: str = "",
        heading: str = "",
        required: bool = True,
        **kwargs,
    ):
        self.name = name
        self.label = label
        self.hint = hint
        self.error = error
        self.heading = heading
        self.required = required
        self._value = None
        self.kwargs = kwargs

    @property
    def value(self):
        return self._value

    @property
    async def clean(self):
        if not self.value:
            return None
        return self.value

    @value.setter
    def value(self, value):
        """
        Assigns a value to a field, runs validation, and sets errors.

        Args:
            value: The value to assign.
        """
        if self.required and not value:
            self.error = "This field is required."
        self._value = value

    @property
    def _id(self):
        """
        Computes a good id from the field name.

        Returns:
            str: Computed id.
        """
        return mkid(self.name)

    @property
    def annotations(self):
        """
        Returns label, hint, and error components for the field.

        Returns:
            tuple: (Label, Hint, Error)
        """
        return (
            (
                Label(self._id, self.label, self.heading, self.required)
                if self.label
                else ""
            ),
            Hint(self._id, self.hint) if self.hint else "",
            Error(self._id, self.error) if self.error else "",
        )

    def __ft__(self, *children: fh.FT, **kwargs) -> fh.FT:
        """
        Renders the field as a FastHTML component.

        Args:
            *children (FT): Optional children components to include.
            **kwargs: Additional keyword arguments.

        Returns:
            FT: A FastHTML component for the field.
        """
        extra_cls = kwargs.pop("cls", "")
        error_cls = " govuk-form-group--error" if self.error else ""
        return fh.Div(
            *self.annotations,
            *children,
            cls=f"govuk-form-group{extra_cls}{error_cls}",
            **kwargs,
        )


class Select(Field):
    """
    Select component. Renders a dropdown. Inherits from Field.

    Args:
        *args: Arguments for Field.
        choices (dict, optional): Choices for the select. Defaults to None.
        **kwargs: Additional keyword arguments.
    """

    def __init__(self, *args, choices: dict | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = choices or {}

    @property
    async def clean(self):
        for val, text in self.choices.items():
            if val == self.value:
                return text

    @property
    def options(self):
        return [
            fh.Option(text, value=value, selected=(value == self.value))
            for value, text in self.choices.items()
        ]

    def __ft__(self, *children, **kwargs) -> fh.FT:
        """
        Renders the select field as a FastHTML component.

        Args:
            *children: Optional children components.
            **kwargs: Additional keyword arguments.

        Returns:
            FT: FastHTML Select component.
        """
        error_cls = " govuk-select--error" if self.error else ""
        return super().__ft__(
            fh.Select(
                name=self.name,
                *self.options,
                _id=self._id,
                cls=f"govuk-select{error_cls}",
            ),
            **self.kwargs,
        )


class Textarea(Field):
    """
    Textarea component. Inherits from Field.

    Args:
        *args: Arguments for Field.
        rows (int, optional): Number of rows in the textarea. Defaults to 5.
        **kwargs: Additional keyword arguments.
    """

    def __init__(self, *args, rows: int = 5, **kwargs):
        super().__init__(*args, **kwargs)
        self.rows = rows

    def __ft__(self, *children, **kwargs) -> fh.FT:
        """
        Renders the textarea field as a FastHTML component.

        Args:
            *children: Optional children components.
            **kwargs: Additional keyword arguments.

        Returns:
            FT: FastHTML Textarea component.
        """
        error_cls = " govuk-textarea--error" if self.error else ""
        return super().__ft__(
            fh.Textarea(
                name=self.name,
                rows=self.rows,
                value=self.value,
                id=self._id,
                aria_describedby=f"{self._id}-hint {self._id}-error",
                cls=f"govuk-textarea{error_cls}",
            ),
            **self.kwargs,
        )


class PasswordInput(Field):
    """
    PasswordInput component. Inherits from Field.

    Args:
        *args: Arguments for Field.
        **kwargs: Additional keyword arguments.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def input(self):
        return fh.Input(
            type="password",
            name=self.name,
            id=self._id,
            aria_describedby=f"{self._id}-hint {self._id}-error",
            cls=(
                "govuk-input govuk-password-input__input "
                "govuk-js-password-input-input"
                f"{' govuk-input--error' if self.error else ''}"
            ),
        )

    @property
    def button(self):
        return fh.Button(
            "Show",
            type="button",
            cls=(
                "govuk-button govuk-button--secondary "
                "govuk-password-input__toggle "
                "govuk-js-password-input-toggle"
            ),
            data_module="govuk-password-input__toggle",
            aria_controls=self._id,
            aria_label="Show password",
            hidden=True,
        )

    def __ft__(self, *children, **kwargs) -> fh.FT:
        """
        Renders the password input field as a FastHTML component.

        Args:
            *children: Optional children components.
            **kwargs: Additional keyword arguments.

        Returns:
            FT: FastHTML component for PasswordInput.
        """
        return super().__ft__(
            fh.Div(
                self.input,
                self.button,
                cls="govuk-input__wrapper govuk-password-input__wrapper",
            ),
            cls=" govuk-password-input",
            data_module="govuk-password-input",
            **self.kwargs,
        )


class CharacterCount(Field):
    """
    CharacterCount component. Renders a Textarea with a character/word count message.

    Args:
        *args: Arguments for Field.
        rows (int, optional): Number of rows in the textarea. Defaults to 5.
        maxchars (int, optional): Max characters allowed. Defaults to None.
        maxwords (int, optional): Max words allowed. Defaults to None.
        threshold (int, optional): Threshold percent for showing count message. Defaults to None.
        **kwargs: Additional keyword arguments.
    """

    def __init__(
        self,
        *args,
        rows: int = 5,
        maxchars: int | None = None,
        maxwords: int | None = None,
        threshold: int | None = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.rows = rows
        self.maxchars = maxchars
        self.maxwords = maxwords
        self.threshold = threshold

    @Field.value.setter
    def value(self, value):
        self._value = value
        if self.required and not value:
            self.error = "This field is required."
            return
        if self.maxchars:
            if len(self._value) > self.maxchars:
                self.error = f"Characters exceed limit of {self.maxchars}."
        if self.maxwords:
            words = self._value.split()
            if len(words) > self.maxwords:
                self.error = f"Words exceed limit of {self.maxwords}."

    @property
    def textarea(self):
        """
        Returns the textarea part of CharacterCount.

        Returns:
            FT: FastHTML Textarea component.
        """
        error_cls = " govuk-textarea--error" if self.error else ""
        return fh.Textarea(
            name=self.name,
            rows=self.rows,
            value=self.value,
            id=self._id,
            aria_describedby=f"{self._id}-hint {self._id}-error",
            cls=f"govuk-textarea govuk-js-character-count{error_cls}",
        )

    @property
    def message(self):
        """
        Returns the message part of CharacterCount.

        Returns:
            FT: FastHTML message component.
        """
        message = (
            f"You can enter up to {self.maxchars} characters."
            if self.maxchars
            else f"You can enter up to {self.maxwords} words."
        )
        return fh.Div(
            message,
            cls="govuk-hint govuk-character-count__message",
            id=f"{self._id}-info",
        )

    def __ft__(self, *children, **kwargs) -> fh.FT:
        """
        Renders the character count field as a FastHTML component.

        Args:
            *children: Optional children components.
            **kwargs: Additional keyword arguments.

        Returns:
            FT: FastHTML component for CharacterCount.
        """
        return super().__ft__(
            self.textarea,
            self.message,
            cls=" govuk-character-count",
            data_module="govuk-character-count",
            data_maxlength=self.maxchars,
            data_maxwords=self.maxwords,
            data_threshold=self.threshold,
            **self.kwargs,
        )


class InputWidth(Enum):
    DEFAULT = 0
    W20 = 1
    W10 = 2
    W5 = 3
    W4 = 4
    W3 = 5
    W2 = 6
    WFULL = 7
    W75 = 8
    W66 = 9
    W50 = 10
    W33 = 11
    W25 = 12


class TextInput(Field):
    """
    TextInput component. Inherits from Field.

    Args:
        *args: Arguments for Field.
        width (InputWidth, optional): Width of TextInput. Defaults to InputWidth.DEFAULT.
        prefix (str, optional): Prefix to TextInput. Defaults to "".
        suffix (str, optional): Suffix to TextInput. Defaults to "".
        autocomplete (str, optional): Autocomplete value. Defaults to "".
        numeric (bool, optional): Is TextInput numeric? Defaults to False.
        spellcheck (bool, optional): Enable spellcheck. Defaults to False.
        extra_spacing (bool, optional): Extra letter spacing. Defaults to False.
        **kwargs: Additional keyword arguments.
    """

    def __init__(
        self,
        *args,
        width: InputWidth = InputWidth.DEFAULT,
        prefix: str = "",
        suffix: str = "",
        autocomplete: str = "",
        numeric: bool = False,
        spellcheck: bool = False,
        extra_spacing: bool = False,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.width = width
        self.prefix = prefix
        self.suffix = suffix
        self.autocomplete = autocomplete
        self.numeric = numeric
        self.spellcheck = spellcheck
        self.extra_spacing = extra_spacing
        self.width_cls = {
            InputWidth.DEFAULT: "",
            InputWidth.W20: " govuk-input--width-20",
            InputWidth.W10: " govuk-input--width-10",
            InputWidth.W5: " govuk-input--width-5",
            InputWidth.W4: " govuk-input--width-4",
            InputWidth.W3: " govuk-input--width-3",
            InputWidth.W2: " govuk-input--width-2",
            InputWidth.WFULL: " govuk-!-width-full",
            InputWidth.W75: " govuk-!-width-three-quarters",
            InputWidth.W66: " govuk-!-width-two-thirds",
            InputWidth.W50: " govuk-!-width-one-half",
            InputWidth.W33: " govuk-!-width-one-third",
            InputWidth.W25: " govuk-!-width-one-quarter",
        }

    @property
    def input(self):
        error_cls = " govuk-input--error" if self.error else ""
        spacing_cls = " govuk-input--extra-letter-spacing" if self.extra_spacing else ""
        return fh.Input(
            type="text",
            name=self.name,
            value=self.value,
            id=self._id,
            aria_describedby=f"{self._id}-hint {self._id}-error",
            cls=f"govuk-input{self.width_cls[self.width]}{error_cls}{spacing_cls}",
            inputmode="numeric" if self.numeric else None,
            spellcheck=self.spellcheck,
            autocomplete=self.autocomplete,
        )

    def __ft__(self, *children, **kwargs) -> fh.FT:
        """
        Renders the text input field as a FastHTML component, including prefix/suffix.

        Args:
            *children: Optional children components.
            **kwargs: Additional keyword arguments.

        Returns:
            FT: FastHTML component for TextInput.
        """
        input = self.input
        if self.prefix:
            input = fh.Div(
                fh.Div(self.prefix, cls="govuk-input__prefix", aria_hidden=True),
                self.input,
                cls="govuk-input__wrapper",
            )
        if self.suffix:
            input = fh.Div(
                self.input,
                fh.Div(self.suffix, cls="govuk-input__suffix", aria_hidden=True),
                cls="govuk-input__wrapper",
            )
        return super().__ft__(input, **self.kwargs)


class Checkbox(AbstractField):
    """
    Checkbox component. Used to define individual checkboxes.

    Args:
        name (str): The name of the checkbox element.
        value (str): The value of the checkbox element.
        label (str): Label for the checkbox element.
        hint (str, optional): Hint for the checkbox element. Defaults to "".
        checked (bool, optional): Make this checkbox checked. Defaults to False.
        exclusive (bool, optional): Make this checkbox exclusive. Defaults to False.
        **kwargs: Additional keyword arguments.
    """

    def __init__(
        self,
        name: str,
        value: str,
        label: str,
        hint: str = "",
        checked: bool = False,
        exclusive: bool = False,
        **kwargs,
    ):
        super().__init__()
        self.name = name
        self.value = value
        self.label = label
        self.hint = hint
        self.checked = checked
        self.exclusive = exclusive
        self.kwargs = kwargs

    @property
    def _id(self):
        """
        Computes checkbox id from name and value.

        Returns:
            str: Computed id.
        """
        return f"{mkid(self.name)}-{self.value}"

    @property
    def label_component(self):
        """
        Returns the Label component.

        Returns:
            FT: Label component.
        """
        return Label(self._id, self.label, extra_cls=" govuk-checkboxes__label")

    @property
    def hint_component(self):
        """
        Returns the Hint component.

        Returns:
            FT: Hint component.
        """
        return Hint(self._id, self.hint, extra_cls=" govuk-checkboxes__hint")

    def __ft__(self, *children, **kwargs) -> fh.FT:
        """
        Renders the checkbox as a FastHTML component.

        Args:
            *children: Optional children components.
            **kwargs: Additional keyword arguments.

        Returns:
            FT: FastHTML Checkbox component.
        """
        return fh.Div(
            fh.Input(
                self.label_component,
                self.hint_component if self.hint else "",
                _id=self._id,
                name=self.name,
                type="checkbox",
                value=self.value,
                checked=self.checked,
                cls="govuk-checkboxes__input",
                data_behaviour="exclusive" if self.exclusive else None,
            ),
            cls="govuk-checkboxes__item",
            **self.kwargs,
        )


class Checkboxes(Field):
    """
    Checkboxes component. Renders a checkbox group for multiple select.

    Args:
        *args: Arguments for Field.
        checkboxes (List[Checkbox], optional): List of Checkbox components.
        choices (dict, optional): Shorthand for simple checkboxes.
        small (bool, optional): Renders small Checkboxes. Defaults to False.
        **kwargs: Additional keyword arguments.
    """

    def __init__(
        self,
        *args,
        checkboxes: List[Checkbox] | None = None,
        choices: dict | None = None,
        small: bool = False,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.checkboxes = checkboxes or []
        self.choices = choices or {}
        self.small = small
        if self.choices:
            self.make_checkboxes()

    @property
    async def clean(self):
        for cb in self.checkboxes:
            if cb.value == self.value:
                return cb.label

    def make_checkboxes(self):
        for value, label in self.choices.items():
            cb = Checkbox(self.name, value, label)
            self.checkboxes.append(cb)

    def __ft__(self, *children, **kwargs) -> fh.FT:
        """
        Renders the checkboxes field as a FastHTML component.

        Args:
            *children: Optional children components.
            **kwargs: Additional keyword arguments.

        Returns:
            FT: FastHTML Checkboxes component.
        """
        small_cls = " govuk-checkboxes--small" if self.small else ""
        for check in self.checkboxes:
            check.checked = check.value == self.value
        return super().__ft__(
            fh.Fieldset(
                fh.Div(
                    *self.checkboxes,
                    cls=f"govuk-checkboxes{small_cls}",
                    data_module="govuk-checkboxes",
                ),
                cls="govuk-fieldset",
                aria_describedby=f"{self._id}-hint",
                id=self._id,
            ),
            **self.kwargs,
        )


class Radio(AbstractField):
    """
    Radio component. Used to define individual radios.

    Args:
        name (str): The name of the radio element.
        value (str): The value of the radio element.
        label (str): Label for the radio element.
        hint (str, optional): Hint for the radio element. Defaults to "".
        checked (bool, optional): Make this radio checked. Defaults to False.
        reveal (Field, optional): Field revealed when Radio is selected. Defaults to None.
        **kwargs: Additional keyword arguments.
    """

    def __init__(
        self,
        name: str,
        value: str,
        label: str,
        hint: str = "",
        checked: bool = False,
        reveal: Field | None = None,
        **kwargs,
    ):
        super().__init__()
        self.name = name
        self.value = value
        self.label = label
        self.hint = hint
        self.checked = checked
        self.reveal = reveal
        self.kwargs = kwargs

    @property
    def _id(self):
        """
        Computes radio id from name and value.

        Returns:
            str: Computed id.
        """
        return f"{mkid(self.name)}-{self.value}"

    @property
    def label_component(self):
        """
        Returns the Label component.

        Returns:
            FT: Label component.
        """
        return Label(self._id, self.label, extra_cls=" govuk-radios__label")

    @property
    def hint_component(self):
        """
        Returns the Hint component.

        Returns:
            FT: Hint component.
        """
        return Hint(self._id, self.hint, extra_cls=" govuk-radios__hint")

    @property
    def data_aria_controls(self):
        if self.reveal:
            return f"conditional-{self._id}"
        return None

    @property
    def base_radio(self):
        return fh.Div(
            fh.Input(
                self.label_component,
                self.hint_component if self.hint else "",
                _id=self._id,
                name=self.name,
                type="radio",
                value=self.value,
                checked=self.checked,
                cls="govuk-radios__input",
                data_aria_controls=self.data_aria_controls,
            ),
            cls="govuk-radios__item",
        )

    @property
    def _reveal(self):
        return fh.Div(
            self.reveal,
            cls="govuk-radios__conditional govuk-radios__conditional--hidden",
            id=f"conditional-{self._id}",
        )

    def __ft__(self, *children, **kwargs) -> fh.FT:
        """
        Renders the radio as a FastHTML component.

        Args:
            *children: Optional children components.
            **kwargs: Additional keyword arguments.

        Returns:
            FT: FastHTML Radio component.
        """
        return (
            fh.Div(
                self.base_radio,
                self._reveal,
                **self.kwargs,
            )
            if self.reveal
            else self.base_radio
        )


class Radios(Field):
    """
    Radios component. Renders a radio group for single select.

    Args:
        *args: Arguments for Field.
        radios (List[Radio], optional): List of Radio components.
        choices (dict, optional): Shorthand for simple radios.
        small (bool, optional): Renders small Radios. Defaults to False.
        inline (bool, optional): Renders inline Radios. Defaults to False.
        **kwargs: Additional keyword arguments.
    """

    def __init__(
        self,
        *args,
        radios: List[Radio] | None = None,
        choices: dict | None = None,
        small: bool = False,
        inline: bool = False,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.radios = radios or []
        self.choices = choices or {}
        self.small = small
        self.inline = inline
        if self.choices:
            self.make_radios()

    @property
    async def clean(self):
        for radio in self.radios:
            if radio.value == self.value:
                return radio.label

    def make_radios(self):
        for value, label in self.choices.items():
            radio = Radio(self.name, value, label)
            self.radios.append(radio)

    def insert_divider(self):
        if len(self.radios) <= 2:
            return self.radios
        divider = fh.Div("or", cls="govuk-radios__divider")
        self.radios.insert(-1, divider)
        return self.radios

    def __ft__(self, *children, **kwargs) -> fh.FT:
        """
        Renders the radios field as a FastHTML component.

        Args:
            *children: Optional children components.
            **kwargs: Additional keyword arguments.

        Returns:
            FT: FastHTML Radios component.
        """
        radios = self.insert_divider() or []
        small_cls = " govuk-radios--small" if self.small else ""
        inline_cls = " govuk-radios--inline" if self.inline else ""
        for radio in self.radios:
            radio.checked = radio.value == self.value
        return super().__ft__(
            fh.Fieldset(
                fh.Div(
                    *radios,
                    cls=f"govuk-radios{small_cls}{inline_cls}",
                    data_module="govuk-radios",
                ),
                cls="govuk-fieldset",
                aria_describedby=f"{self._id}-hint",
                id=self._id,
            ),
            **self.kwargs,
        )


class FileUpload(Field):
    """
    FileUpload component. Renders a file upload field.

    Args:
        *args: Arguments for Field.
        **kwargs: Additional keyword arguments.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def valid_file(self):
        filename = getattr(self.value, "filename", None)
        return filename is not None

    @Field.value.setter
    def value(self, value):
        self._value = value
        if self.required and not self.valid_file:
            self.error = "This field is required."
            return

    @property
    async def clean(self):
        # field was not required
        if not self.value:
            return None
        # Sometimes, when field is left empty
        # we get a reference to an empty UploadFile
        # TODO: Figure out when and why this happens
        # and write tests against it.
        if not self.valid_file:
            return None
        try:
            buffer = await self.value.read()
            filename = self.value.filename
            path = Path("media") / filename
            path.write_bytes(buffer)
            return str(path)
        except (ValueError, AttributeError, OSError):
            raise

    def __ft__(self, *children, **kwargs) -> fh.FT:
        """
        Renders the file upload field as a FastHTML component.

        Args:
            *children: Optional children components.
            **kwargs: Additional keyword arguments.

        Returns:
            FT: FastHTML component for FileUpload.
        """
        error_cls = " govuk-file-upload--error" if self.error else ""
        return super().__ft__(
            fh.Div(
                fh.Input(
                    id=self.name,
                    name=self.name,
                    value=self.value,
                    type="file",
                    cls=f"govuk-file-upload{error_cls}",
                    aria_describedby=f"{self._id}-hint {self._id}-error",
                ),
                cls="govuk-drop-zone",
                data_module="govuk-file-upload",
            ),
            **self.kwargs,
        )


def _date_input_item(
    name: str, suffix: str, width: int = 2, value: str = "", error: bool = False
):
    """
    Date Input item e.g. Day, Month, Year.

    Args:
        name (str): Name of the parent DateField.
        suffix (str): Suffix for this field e.g. "day", "month", "year".
        width (int, optional): Width of the field. Defaults to 2.
        value (str, optional): Value to assign to the input. Defaults to "".
        error (bool, optional): Error state. Defaults to False.

    Returns:
        FT: A FastHTML input component.
    """
    _id = f"{mkid(name)}-{suffix}"
    input_id = f"{_id}-input"
    label = Label(input_id, suffix.title(), extra_cls=" govuk-date-input__label")
    date_cls = "govuk-date-input__input"
    width_cls = f" govuk-input--width-{width}"
    error_cls = " govuk-input--error" if error else ""
    input = fh.Input(
        name=name,
        value=value,
        _id=input_id,
        _type="text",
        inputmode="numeric",
        cls=f"govuk-input {date_cls}{width_cls}{error_cls}",
    )
    return fh.Div(
        fh.Div(label, input, cls="govuk-form-group", _id=_id),
        cls="govuk-date-input__item",
    )


class DateInput(Field):
    """
    DateInput component. Renders GDS-style composite field with day, month, year.

    Args:
        *args: Arguments for Field.
        **kwargs: Additional keyword arguments.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def value(self):
        return self._value

    @property
    async def clean(self):
        # Field not required
        if self.value == ["", "", ""]:
            return None
        try:
            day, month, year = self.value
            day, month, year = int(day), int(month), int(year)
            _date = date(day=day, month=month, year=year)
            return _date.isoformat()
        except ValueError:
            raise

    @value.setter
    def value(self, value):
        self._value = value or ("", "", "")
        day, month, year = self._value
        if self.required:
            if (not day or not month or not year):
                self.error = "This field is required."
                return
            try:
                day, month, year = int(day), int(month), int(year)
                _ = date(day=day, month=month, year=year)
            except (ValueError, TypeError):
                self.error = "Invalid values."

    @property
    def day_field(self):
        """
        Returns the day field component of DateInput.

        Returns:
            FT: Day field component.
        """
        return _date_input_item(
            self.name,
            "day",
            error=(self.error != ""),
            value=self.value[0] if self.value else "",
        )

    @property
    def month_field(self):
        """
        Returns the month field component of DateInput.

        Returns:
            FT: Month field component.
        """
        return _date_input_item(
            self.name,
            "month",
            error=(self.error != ""),
            value=self.value[1] if self.value else "",
        )

    @property
    def year_field(self):
        """
        Returns the year field component of DateInput.

        Returns:
            FT: Year field component.
        """
        return _date_input_item(
            self.name,
            "year",
            width=4,
            error=(self.error != ""),
            value=self.value[2] if self.value else "",
        )

    def __ft__(self, *children, **kwargs) -> fh.FT:
        return super().__ft__(
            fh.Fieldset(
                fh.Div(
                    self.day_field,
                    self.month_field,
                    self.year_field,
                    cls="govuk-date-input",
                    _id=self._id,
                ),
                cls="govuk-fieldset",
                role="group",
                aria_describedby=f"{self._id}-hint",
            ),
            **self.kwargs,
        )


class ButtonStyle(Enum):
    PRIMARY = 1
    SECONDARY = 2
    WARNING = 3
    INVERSE = 4


def Button(
    text: str,
    style: ButtonStyle = ButtonStyle.PRIMARY,
    disabled: bool = False,
    prevent_double_click: bool = False,
    **kwargs,
) -> fh.FT:
    """
    Button component.

    Args:
        text (str): The text on the Button component.
        style (ButtonStyle, optional): The style of the Button component. Defaults to ButtonStyle.PRIMARY.
        disabled (bool, optional): Disable the button. Defaults to False.
        prevent_double_click (bool, optional): Prevent accidental double clicks. Defaults to False.
        **kwargs: Any extra args to pass to fh.Button.

    Returns:
        FT: A FastHTML Button component.
    """
    btn_cls = {
        ButtonStyle.PRIMARY: "govuk-button",
        ButtonStyle.SECONDARY: "govuk-button govuk-button--secondary",
        ButtonStyle.WARNING: "govuk-button govuk-button--warning",
        ButtonStyle.INVERSE: "govuk-button govuk-button--inverse",
    }
    return fh.Button(
        text,
        _type="submit",
        disabled=disabled,
        aria_disabled=disabled,
        data_prevent_double_click=prevent_double_click,
        data_module="govuk-button",
        cls=btn_cls[style],
        **kwargs,
    )


def StartButton(text: str, href: str, **kwargs) -> fh.FT:
    """
    StartButton component for call-to-actions. Does not submit form data.

    Args:
        text (str): Text on the Button component.
        href (str): URL of the target page.
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML StartButton component.
    """
    icon = fh.NotStr(
        '<svg class="govuk-button__start-icon" xmlns="http://www.w3.org/2000/svg" width="17.5" '
        'height="19" viewBox="0 0 33 40" aria-hidden="true" focusable="false">'
        '<path fill="currentColor" d="M0 0h13l20 20-20 20H0l20-20z" />'
        "</svg>"
    )
    return fh.A(
        text,
        icon,
        href=href,
        role="button",
        draggable="false",
        cls="govuk-button govuk-button--start",
        data_module="govuk-button",
        **kwargs,
    )


def ButtonGroup(*buttons: fh.FT, **kwargs) -> fh.FT:
    """
    ButtonGroup component.

    Args:
        *buttons (FT): List of Button components.
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML component.
    """
    return fh.Div(
        *buttons,
        cls="govuk-button-group",
        **kwargs,
    )


def CookieBanner(
    service_name: str,
    *content: fh.FT,
    cookie_page_link: str = "/cookies",
    cookie_form_link: str = "/",
    confirmation: bool = False,
    **kwargs,
) -> fh.FT:
    """
    CookieConfirmation component.

    Args:
        service_name (str): Name of the service.
        *content (FT): Content of the CookieConfirmation component.
        cookie_page_link (str, optional): Link to the cookie settings page. Defaults to "/cookies".
        cookie_form_link (str, optional): Link to the cookie form submission page. Defaults to "/".
        confirmation (bool, optional): If True, the cookie confirmation is shown. Defaults to False.
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML CookieConfirmation component.
    """
    banner_buttons = ButtonGroup(
        Button("Accept additional cookies", value="yes", name="cookies[additional]"),
        Button("Reject additional cookies", value="no", name="cookies[additional]"),
        A("View cookies", href=cookie_page_link),
    )
    confirm_buttons = ButtonGroup(
        # TODO: Add some js to hide this when button is pressed
        Button("Hide cookie message", value="hide", name="cookies[additional]"),
    )
    button_group = confirm_buttons if confirmation else banner_buttons
    return fh.Div(
        fh.Div(
            fh.Div(
                fh.Div(
                    H2(f"Cookies for {service_name}"),
                    fh.Div(
                        *content,
                        cls="govuk-cookie-banner__content",
                    ),
                    cls="govuk-grid-column-two-thirds",
                ),
                cls="govuk-grid-row",
            ),
            fh.Form(
                button_group,
                hx_post=cookie_form_link,
                hx_target="#cookie-banner",
                hx_swap="outerHTML",
            ),
            cls="govuk-cookie-banner__message govuk-width-container",
        ),
        cls="govuk-cookie-banner",
        role="region",
        aria_label=f"Cookies on {service_name}",
        data_nosnippet=True,
        id="cookie-banner",
        **kwargs,
    )


class Fieldset(AbstractField):
    """
    Fieldset component.

    Args:
        *fields (Field): Fields to include in the fieldset.
        name (str, optional): Name of the fieldset. Defaults to "".
        legend (str, optional): The legend text for the fieldset.
        heading (str, optional): Heading size. Defaults to "l".
        **kwargs: Additional keyword arguments.
    """

    def __init__(self, *fields: Field, name: str = "", legend: str = "", heading: str = "l", **kwargs):
        self.fields = fields
        self.name = name
        self.legend = legend
        self.heading = heading
        self.kwargs = kwargs

    def __ft__(self):
        """
        Renders the fieldset as a FastHTML component.

        Returns:
            FT: A FastHTML Fieldset component.
        """
        heading_cls = f" govuk-fieldset__legend--{self.heading}" if self.heading else ""
        return fh.Fieldset(
            fh.Legend(
                fh.H1(
                    self.legend,
                    cls="govuk-fieldset__heading",
                ),
                cls=f"govuk-fieldset__legend{heading_cls}",
            ),
            *self.fields,
            cls="govuk-fieldset",
            **self.kwargs,
        )
