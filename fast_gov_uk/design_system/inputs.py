from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from pathlib import Path
from typing import List, Optional, Tuple

import fasthtml.common as fh

from .typography import H2, A
from .utils import mkid


def Label(
    field_id: str,
    text: str,
    heading: bool = False,
    required: bool = True,
    extra_cls: str = "",
) -> fh.FT:
    """
    Label component. Generally attached to a Field.
    Args:
        field_id (str): HTML id of the field this label is for.
        text (str): Text to be displayed in the label.
        heading (bool): Is this label a heading? Defaults to False.
        required (book): Is this for a field that is required? Defaults to True.
    Returns:
        FT: A FastHTML label component.
    """
    optional = "" if required else " (Optional)"
    heading_cls = " govuk-label--l" if heading else ""
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
    Returns:
        FT: A FastHTML hint component.
    """
    return fh.Div(text, cls=f"govuk-hint{extra_cls}", id=f"{field_id}-hint")


def Error(field_id: str, text: str, extra_cls: str = "") -> fh.FT:
    """
    Error component. Generally attached to a Field.
    Args:
        field_id (str): HTML id of the field this hint is for.
        text (str): Text to be displayed as hint.
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


@dataclass
class Field(AbstractField):
    """
    Baseclass for form fields.
    Args:
        name (str): The name of the field.
        label (str): Label for the field.
        hint (str): Hint for the field. Defaults to "".
        error (str): Error message for the field. Defaults to "".
        heading (bool): Make label a heading? Defaults to False.
        required (book): Is this field required? Defaults to True.
    """

    name: str
    label: str = ""
    hint: str = ""
    error: str = ""
    heading: bool = False
    required: bool = True
    _value = None

    @property
    def value(self):
        return self._value

    @property
    async def clean(self):
        return self.value

    @value.setter
    def value(self, value):
        """
        This setter is how you assign a value to a field. It takes the
        value, runs some validation to generate errors and then assign the
        value to the self._value attribute while also assigning any
        validation errros to self.error.
        """
        if self.required and not value:
            self.error = "This field is required."
        self._value = value

    @property
    def _id(self):
        """
        Name is a required attribute for fields. We should be able to
        compute a good id from the name.
        """
        return mkid(self.name)

    @property
    def annotations(self):
        """
        Includes labels, hints and errors - not the field itself but
        information about the field that makes it usable.
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
        Render the field as a FastHTML component.
        Args:
            children (FT): Optional children components to include.
            extra_cls (str): Additional CSS classes to apply.
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


@dataclass
class Select(Field):
    """
    Select component. Renders the usual dropdown. Inherits from `Field`.
    Args (in addition to Field):
        options (list): Tuple with (<value>, <label>) for options.
    """

    options: List[Tuple[str, str]] = field(default_factory=list)

    def __ft__(self, *children, **kwargs) -> fh.FT:
        """
        Render the field as a FastHTML component.
        Returns:
            FT: FastHTML Select component.
        """
        error_cls = " govuk-select--error" if self.error else ""
        return super().__ft__(
            fh.Select(
                name=self.name,
                *[
                    fh.Option(text, value=value, selected=(value == self.value))
                    for value, text in self.options
                ],
                _id=self._id,
                cls=f"govuk-select{error_cls}",
            ),
        )


@dataclass
class Textarea(Field):
    """
    Textarea component. Inherits from `Field`.
    Args (in addition to Field):
        rows (int): Number of rows in the textarea.
    """

    rows: int = 5

    def __ft__(self, *children, **kwargs) -> fh.FT:
        """
        Render the field as a FastHTML component.
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
        )


@dataclass
class PasswordInput(Field):
    """
    PasswordInput component. Inherits from `Field`.
    """

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
        Render the field as a FastHTML component.
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
        )


@dataclass
class CharacterCount(Field):
    """
    CharacterCount component. Renders a Textarea with a message
    that display either the number of characters or the number of
    words left. Inherits from `Field`.
    Args:
        rows (int): Number of rows in the textarea.
        maxchars (int): Max characters allowed. Defaults to None.
        maxwords (int): Max words allowed. Defaults to None.
        threshold (int): Display the count message when the length
            of text passes a certain threshold in percent.
            Defaults to None.
    """

    rows: int = 5
    maxchars: Optional[int] = None
    maxwords: Optional[int] = None
    threshold: Optional[int] = None

    @Field.value.setter
    def value(self, value):
        self._value = value
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
        Textarea part of CharacterCount.
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
        Message part of CharacterCount.
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
        Render the field as a FastHTML component.
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


@dataclass
class TextInput(Field):
    width: InputWidth = InputWidth.DEFAULT
    prefix: str = ""
    suffix: str = ""
    autocomplete: str = ""
    numeric: bool = False
    spellcheck: bool = False
    extra_spacing: bool = False
    width_cls = {
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
        Render the field as a FastHTML component.
        Returns:
            FT: FastHTML component for TextInput - including
            prefix and suffix if defined.
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
        return super().__ft__(input)


@dataclass
class Checkbox(AbstractField):
    """
    Checkbox component. This component does not inherit from Field because
    (at this moment), the primary usage for this is as an API to define
    individual checkboxes and pass them to the Checkboxes component -
    which is a Field.
    Args:
        name (str): The name of the checkbox element.
        value (str): The value of the checkbox element.
        label (str): Label for the checkbox element.
        hint (str): Hint for the checkbox element. Defaults to "".
        checked (bool): Make this checkbox checked. Defaults to False.
        exclusive (bool): Make this checkbox eclusive? Defaults to False.
    """

    name: str
    value: str
    label: str
    hint: str = ""
    checked: bool = False
    exclusive: bool = False

    @property
    def _id(self):
        """
        Compute checkbox id from name + value.
        """
        return f"{mkid(self.name)}-{self.value}"

    @property
    def label_component(self):
        """
        Returns: Label component.
        """
        return Label(self._id, self.label, extra_cls=" govuk-checkboxes__label")

    @property
    def hint_component(self):
        """
        Returns: Hint component.
        """
        return Hint(self._id, self.hint, extra_cls=" govuk-checkboxes__hint")

    def __ft__(self, *children, **kwargs) -> fh.FT:
        """
        Render the field as a FastHTML component.
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
        )


@dataclass
class Checkboxes(Field):
    """
    Checkboxes component. Renders the usual checkbox group for multiple
    select. Inherits from `Field`.
    Args (in addition to Field):
        checkboxes (list): List of Checkbox components.
        choices (list): Labels - shorthand for simple checkboxes.
        small (bool): Renders small Checkboxes. Defaults to False.
    """

    checkboxes: List[Checkbox] = field(default_factory=list)
    choices: List[str] = field(default_factory=list)
    small: bool = False

    def make_checkboxes(self):
        for choice in self.choices:
            choice_tokens = choice.lower().split()
            value = "_".join(choice_tokens)
            cb = Checkbox(self.name, value, choice)
            self.checkboxes.append(cb)

    def __ft__(self, *children, **kwargs) -> fh.FT:
        """
        Render the field as a FastHTML component.
        Returns:
            FT: FastHTML Checkboxes component.
        """
        if not self.checkboxes:
            self.make_checkboxes()
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
            ),
        )


@dataclass
class Radio(AbstractField):
    """
    Radio component. This component does not inherit from Field because
    (at this moment), the primary usage for this is as an API to define
    individual radios and pass them to the Radios component -
    which is a Field.
    Args:
        name (str): The name of the radio element.
        value (str): The value of the radio element.
        label (str): Label for the radio element.
        hint (str): Hint for the radio element. Defaults to "".
        checked (bool): Make this radio checked. Defaults to False.
    """

    name: str
    value: str
    label: str
    hint: str = ""
    checked: bool = False

    @property
    def _id(self):
        """
        Compute radio id from the name + value.
        """
        return f"{mkid(self.name)}-{self.value}"

    @property
    def label_component(self):
        """
        Returns: Label component.
        """
        return Label(self._id, self.label, extra_cls=" govuk-radios__label")

    @property
    def hint_component(self):
        """
        Returns: Hint component.
        """
        return Hint(self._id, self.hint, extra_cls=" govuk-radios__hint")

    def __ft__(self, *children, **kwargs) -> fh.FT:
        """
        Render the field as a FastHTML component.
        Returns:
            FT: FastHTML Radio component.
        """
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
            ),
            cls="govuk-radios__item",
        )


@dataclass
class Radios(Field):
    """
    Radios component. Renders the usual radio group for single
    select. Inherits from `Field`.
    Args (in addition to Field):
        radios (list): List of Radio components.
        choices (list): Labels - shorthand for simple radios
        small (bool): Renders small Radios. Defaults to False.
        inline (bool): Renders inline Radios. Defaults to False.
    """

    radios: List[Radio] = field(default_factory=list)
    choices: List[str] = field(default_factory=list)
    small: bool = False
    inline: bool = False

    def make_radios(self):
        for choice in self.choices:
            choice_tokens = choice.lower().split()
            value = "_".join(choice_tokens)
            radio = Radio(self.name, value, choice)
            self.radios.append(radio)

    def __ft__(self, *children, **kwargs) -> fh.FT:
        if not self.radios:
            self.make_radios()
        small_cls = " govuk-radios--small" if self.small else ""
        inline_cls = " govuk-radios--inline" if self.inline else ""
        for radio in self.radios:
            radio.checked = radio.value == self.value
        return super().__ft__(
            fh.Fieldset(
                fh.Div(
                    *self.radios,
                    cls=f"govuk-radios{small_cls}{inline_cls}",
                    data_module="govuk-radios",
                ),
                cls="govuk-fieldset",
                aria_describedby=f"{self._id}-hint",
            ),
        )


@dataclass
class FileUpload(Field):
    """
    FileUpload component. Renders a file upload field.
    Inherits from `Field`.
    """

    @property
    async def clean(self):
        if self.value:
            buffer = await self.value.read()
            filename = self.value.filename
            path = Path("media") / filename
            path.write_bytes(buffer)
            return str(path)

    def __ft__(self, *children, **kwargs) -> fh.FT:
        """
        Render the field as a FastHTML component.
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
        )


def _date_input_item(
    name: str, suffix: str, width: int = 2, value: str = "", error: bool = False
):
    """
    Date Input item e.g. Day, Month, Year.
    Args:
        name (str): Name of the parent DateField.
        suffix (str): Suffix for this field e.g. "day", "month", "year"
        width (int): Width of the field. Defaults to 2.
        value (str): Value to assign to the input. Defaults to "".
        error (bool): Error message. Defaults to False.
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


@dataclass
class DateInput(Field):
    """
    DateInput component. Renders GDS-style composite field with
    separate TextInputs for day, month and year. Inherits Field.
    TODO: Support errors for individual fields.
    """

    @property
    def value(self):
        return self._value

    @property
    async def clean(self):
        try:
            day, month, year = self.value
            day, month, year = int(day), int(month), int(year)
            _date = date(day=day, month=month, year=year)
            return _date.isoformat()
        except ValueError:
            return None

    @value.setter
    def value(self, value):
        self._value = value
        day, month, year = self._value
        if not day or not month or not year:
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
        Returns day field component of DateInput.
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
        Returns month field component of DateInput.
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
        Returns year field component of DateInput.
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
        style (ButtonStyle): The style of the Button component. Default: ButtonStyle.PRIMARY.
        disabled (bool): Disable the button. Default: False.
        prevent_double_click (bool): Prevent accidental double clicks. Default: False.
        **kwargs (dict): Any extra args to pass to fh.Button.
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


def StartButton(text: str, href: str) -> fh.FT:
    """
    StartButton component for call-to-actions. StartButtons don't submit
    any form data.
    Args:
        text (str): Text on the Button component.
        href (str): URL of the target page.
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
    )


def ButtonGroup(*buttons: fh.FT) -> fh.FT:
    """
    ButtonGroup component.
    Args:
        buttons (list): List of Button components.
    Returns:
        FT: A FastHTML component.
    """
    return fh.Div(
        *buttons,
        cls="govuk-button-group",
    )


def CookieBanner(
    service_name: str,
    *content: fh.FT,
    cookie_page_link: str = "/cookies",
    cookie_form_link: str = "/",
    confirmation: bool = False,
) -> fh.FT:
    """
    CookieConfirmation component.
    Args:
        service_name (str): Name of the service.
        content (list): Content of the CookieConfirmation component.
        cookie_page_link (str): Link to the cookie settings page. Defaults to "/cookies".
        cookie_form_link (str): Link to the cookie form submission page. Defaults to "/".
        confirmaton (bool): If True, the cookie confirmation is shown. Defaults to False.
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
            fh.Form(button_group, hx_post=cookie_form_link, hx_target="#cookie-banner"),
            cls="govuk-cookie-banner__message govuk-width-container",
        ),
        cls="govuk-cookie-banner",
        role="region",
        aria_label=f"Cookies on {service_name}",
        data_nosnippet=True,
        id="cookie-banner",
    )


class Fieldset(AbstractField):
    """
    Fieldset component.
    Args:
        fields (list): Fields to include in the fieldset.
        legend (str): The legend text for the fieldset.
    Returns:
        FT: A FastHTML Fieldset component.
    """

    def __init__(self, *fields: Field, legend: str = ""):
        self.fields = fields
        self.legend = legend

    def __ft__(self):
        return fh.Fieldset(
            fh.Legend(
                fh.H1(
                    self.legend,
                    cls="govuk-fieldset__heading",
                ),
                cls="govuk-fieldset__legend govuk-fieldset__legend--l",
            ),
            *self.fields,
            cls="govuk-fieldset",
        )
