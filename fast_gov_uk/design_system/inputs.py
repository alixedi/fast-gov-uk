"""
GOV.UK Design System form input components including TextInput, Textarea,
Select, Checkboxes, Radios etc.

These components are subclasses of :py:class:`Field` which provides common
functionality like rendering labels, hints, errors, setting values, and
validating required fields.
"""

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
    Used by the :py:class:`Field` component to render a label.

    Handles whether the label is a heading, whether the field is required etc.

    Use this if you are creating a custom field.

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
    Used by the :py:class:`Field` component to render a hint.

    Use this if you are creating a custom field.

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
    Used by the :py:class:`Field` component to render error message.

    Use this if you are creating a custom field.

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
    """
    Every form field is a subclass of this type.

    This is useful when e.g. we are having to distinguish fields in a
    form that contains fields as well as non-field elements like H1 and P.

    These types of mixed forms are quite common in question pages.
    """
    pass


class Field(AbstractField):
    """
    Baseclass for form inputs. Provides scaffolding for -

        - rendering labels
        - rendering hints
        - rendering errors
        - setting field values
        - validation for required fields

    If you are want to implement a custom GOV.UK input, this is a good
    base class to inherit from.

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
        """
        Get "clean" data from a field when a form is being processed
        by a form Backend.
        """
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
    `GOV.UK Select`_ component. Renders a dropdown. Inherits from Field.

    This component should only be used as a last resort in public-facing services because research
    shows that some users find selects very difficult to use.

    Use Checkbox or Radio components instead.

    Examples:

        >>> ds.Select("question", choices={"yes": "Yes", "no": "No"})
        # Renders a dropdown select with the given options - "Yes" and "No.
        # Note the values for these options are "yes" and "no" respectively

    Args:
        *args: Arguments for Field.
        choices (dict, optional): Choices for the select. Defaults to None.
        **kwargs: Additional keyword arguments.

    .. _GOV.UK Select: https://design-system.service.gov.uk/components/select/
    """

    def __init__(self, *args, choices: dict | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = choices or {}

    @property
    async def clean(self):
        """
        Get "clean" data from a field when a form is being processed
        by a form Backend.
        """
        for val, text in self.choices.items():
            if val == self.value:
                return text

    @property
    def options(self):
        """
        Convert the choices dict into a list of <option> to be
        inserted into the Select component.
        """
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
    `GOV.UK Textarea`_ component. Inherits from Field.

    Use this component when you need to let users enter more than a single line of text.

    Examples:

        >>> ds.Textarea('test')
        # Renders a text area with the default 5 rows

    Args:
        *args: Arguments for Field.
        rows (int, optional): Number of rows in the textarea. Defaults to 5.
        **kwargs: Additional keyword arguments.

    .. _GOV.UK Textarea: https://design-system.service.gov.uk/components/textarea/
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
    `GOV.UK Password input`_ component. Inherits from Field.

    Use this component when you need users to type a password.

    Examples:

        >>> ds.PasswordInput('test')
        # Renders a password input

    Args:
        *args: Arguments for Field.
        **kwargs: Additional keyword arguments.

    .. _GOV.UK Password input: https://design-system.service.gov.uk/components/password-input/
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def input(self):
        """
        Input part for this component.
        """
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
        """
        Button part for this component
        """
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
    `GOV.UK Character count`_ component. Renders a Textarea with a character/word count message.

    Help users know how much text they can enter when there is a limit on the number of characters.

    It is recommended to always test your service without a character count first and to only use the
    character count component when there is a good reason for limiting the number of characters users
    can enter.

    Examples:

        >>> ds.CharacterCount('test')
        # Renders a text area
        >>> ds.CharacterCount('test', maxchars=100)
        # Renders a text area with a limit of 100 characters max
        >>> ds.CharacterCount('test', maxwords=10)
        # Renders a text area with a limit of 10 words max
        >>> ds.CharacterCount('test', maxwords=10, threshold=50)
        # Renders a text area with a limit of 10 words max but the message that says
        # "You have X words left" only appears after 50% of the limit is crossed.

    Args:
        *args: Arguments for Field.
        rows (int, optional): Number of rows in the textarea. Defaults to 5.
        maxchars (int, optional): Max characters allowed. Defaults to None.
        maxwords (int, optional): Max words allowed. Defaults to None.
        threshold (int, optional): Threshold percent for showing count message. Defaults to None.
        **kwargs: Additional keyword arguments.

    .. _GOV.UK Character count: https://design-system.service.gov.uk/components/character-count/
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
        """
        Assign error if user have exceeded maxchars or maxwords.
        """
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
    """
    Enum to define GOV.UK supported input widths to be passed into
    :py:class:`TextInput` as `width` param.
    """
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
    `GOV.UK Text Input`_ component. Inherits from Field.

    Use the text input component when you need to let users enter text that is no longer than a
    single line, such as their name or email address.

    Examples:

        >>> ds.TextInput('test')
        # Renders a standard text input
        >>> ds.TextInput('test', width=InputWidth.W50)
        # Renders a text input with a width of 50%
        >>> ds.TextInput('test', prefix="£")
        # Renders a text input with a prefix of "£"
        >>> ds.TextInput('test', suffix="%")
        # Renders a text input with a suffix of "%"
        >>> ds.TextInput('test', autocomplete="postal-code")
        # Renders a text input that uses the autocomplete features in
        # modern browsers to fill-in the postcode
        >>> ds.TextInput('test', numeric=True)
        # Renders a text input that uses the numeric keypad on devices
        # with on-screen keyboards.
        >>> ds.TextInput('test', spellcheck=True)
        # Renders a text input with the spellcheck turned on
        >>> ds.TextInput('test', extraspacing=True)
        # Renders a text input with extra spacing

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

    .. _GOV.UK Text Input: https://design-system.service.gov.uk/components/text-input/
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
        """
        Input part of this component.
        """
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
    Checkbox component. Used to define individual checkboxes to be passed into
    the :py:class:`Checkboxes` component.

    Note that this inherits from :py:class:`AbstractField` instead of :py:class:`Field` because
    it is only meant to be used inside the :py:class:`Checkboxes` component - which inherits from
    :py:class:`Field`.

    Examples:

        >>> cb = ds.Checkbox('test', 'test', 'Test Label')
        # Renders a Checkbox called "test" with a label "Test Label"
        >>> cb = ds.Checkbox('test', 'test', 'Test Label', checked=True)
        # Renders the same Checkbox but its checked by default
        >>> cb = ds.Checkbox('test', 'test', 'Test Label', checked=True)
        # Renders the same Checkbox but its checked by default
        >>> cb = ds.Checkbox('test', 'test', 'Test Label', exclusive=True)
        # Renders the same Checkbox when this checkbox it clicked, it unchecks all other
        # checkboxes - handy for options like "None of the above"

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
        Checkbox id from name and value.
        """
        return f"{mkid(self.name)}-{self.value}"

    @property
    def label_component(self):
        """
        Label component.
        """
        return Label(self._id, self.label, extra_cls=" govuk-checkboxes__label")

    @property
    def hint_component(self):
        """
        Hint component.
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
    `GOV.UK Checkboxes`_ component. Let users select one or more options by using the checkboxes
    component.

    Use the checkboxes component when you need to help users: select multiple options from a list
    or to toggle a single option on or off.

    Use the handy "choices" parameter as a shortcut to quickly define standard checkbox groups.

    Examples:

        >>> ds.Checkboxes("question", choices={"yes": "Yes!", "no": "Maybe later.."})
        # Renders checkboxes called "question" with values "yes" and "no" with texts
        # "Yes!" and "Maybe later.." respectively
        >>> ds.Checkboxes("question", choices={"yes": "Yes!", "no": "Maybe later.."}, small=True)
        # Renders the same checkbox with more compact styling
        >>> cb_yes = ds.Checkbox("question", "yes", "Yes!")
        >>> cb_no = ds.Checkbox("question", "no", "Maybe later..")
        >>> ds.Checkboxes("question", cb_yes, cb_no)
        # Renders the same checkboxes but by defining individual components, we can use
        # all of the underlying configurations

    Args:
        *args: Arguments for Field.
        checkboxes (List[Checkbox], optional): List of Checkbox components.
        choices (dict, optional): Shorthand for simple checkboxes.
        small (bool, optional): Renders small Checkboxes. Defaults to False.
        **kwargs: Additional keyword arguments.

    .. _GOV.UK Checkboxes: https://design-system.service.gov.uk/components/checkboxes/
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
        """
        Get "clean" data from a field when a form is being processed
        by a form Backend.
        """
        for cb in self.checkboxes:
            if cb.value == self.value:
                return cb.label

    def make_checkboxes(self):
        """
        Make checkboxes from choices.
        """
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
    Radio component. Used to define individual radioes to be passed into
    the :py:class:`Radios` component.

    Note that this inherits from :py:class:`AbstractField` instead of :py:class:`Field` because
    it is only meant to be used inside the :py:class:`Radios` component - which inherits from
    :py:class:`Field`.

    Examples:

        >>> cb = ds.Radio('test', 'test', 'Test Label')
        # Renders a radio called "test" with a label "Test Label"
        >>> cb = ds.Radio('test', 'test', 'Test Label', checked=True)
        # Renders the same radio but its checked by default
        >>> cb = ds.Radio('test', 'test', 'Test Label', checked=True)
        # Renders the same radio but its checked by default

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
        """
        return f"{mkid(self.name)}-{self.value}"

    @property
    def label_component(self):
        """
        Label component.
        """
        return Label(self._id, self.label, extra_cls=" govuk-radios__label")

    @property
    def hint_component(self):
        """
        Hint component.
        """
        return Hint(self._id, self.hint, extra_cls=" govuk-radios__hint")

    @property
    def data_aria_controls(self):
        """
        Aria-controls component.
        """
        if self.reveal:
            return f"conditional-{self._id}"
        return None

    @property
    def base_radio(self):
        """
        Base radio component.
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
                data_aria_controls=self.data_aria_controls,
            ),
            cls="govuk-radios__item",
        )

    @property
    def _reveal(self):
        """
        Reveal component.
        """
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
    `GOV.UK Radios`_ component. Use the radios component when users can only select one option
    from a list.

    Use the handy "choices" parameter as a shortcut to quickly define standard radio groups.

    Examples:

        >>> ds.Radios("question", choices={"yes": "Yes!", "no": "Maybe later.."})
        # Renders radios called "question" with values "yes" and "no" with texts
        # "Yes!" and "Maybe later.." respectively
        >>> ds.Radios("question", choices={"yes": "Yes!", "no": "Maybe later.."}, small=True)
        # Renders the same checkbox with more compact styling
        >>> ds.Radios("question", choices={"yes": "Yes!", "no": "Maybe later.."}, inline=True)
        # Renders the same checkbox with inline styling
        >>> yes = ds.Radio("question", "yes", "Yes!")
        >>> no = ds.Radio("question", "no", "Maybe later..")
        >>> ds.Radios("question", yes, no)
        # Renders the same radios but by defining individual components, we can use
        # all of the underlying configurations

    Args:
        *args: Arguments for Field.
        radios (List[Radio], optional): List of Radio components.
        choices (dict, optional): Shorthand for simple radios.
        small (bool, optional): Renders small Radios. Defaults to False.
        inline (bool, optional): Renders inline Radios. Defaults to False.
        **kwargs: Additional keyword arguments.

    .. _GOV.UK Radios: https://design-system.service.gov.uk/components/radios/
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
        """
        Get "clean" data from a field when a form is being processed
        by a form Backend.
        """
        for radio in self.radios:
            if radio.value == self.value:
                return radio.label

    def make_radios(self):
        """
        Make radios from choices.
        """
        for value, label in self.choices.items():
            radio = Radio(self.name, value, label)
            self.radios.append(radio)

    def insert_divider(self):
        """
        Insert "or" if there are more than 2 radios.
        """
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
    `GOV.UK File upload`_ component. Renders a file upload field to help users select and
    upload a file.

    To upload a file, the user can either: use the "Choose file" button or drag and drop a
    file into the file upload input area.

    It is recommended that you should only ask users to upload something if it's critical to
    the delivery of your service.

    Examples:

        >>> ds.FileUpload("test")
        # Renders a file upload field called "test"

    Args:
        *args: Arguments for Field.
        **kwargs: Additional keyword arguments.

    .. _GOV.UK File upload: https://design-system.service.gov.uk/components/radios/
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def valid_file(self):
        """
        Is the uploaded file valid?
        """
        filename = getattr(self.value, "filename", None)
        return filename is not None

    @Field.value.setter
    def value(self, value):
        """
        Checks if the file is valid and assign error accordingly.
        """
        self._value = value
        if self.required and not self.valid_file:
            self.error = "This field is required."
            return

    @property
    async def clean(self):
        """
        Get "clean" data from a field when a form is being processed
        by a form Backend.
        """
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
    Date Input item e.g. Day, Month or Year used to produce underlying inputs
    in the composite field that is the :py:class:`DateInput` component.

    TODO: This should probably be a property in DateInput.

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
    `GOV.UK Date input`_ component. Renders GDS-style composite field with day, month, year.

    You should use the date input component to help users enter a memorable date or one they
    can easily look up.

    Examples:

        >>> ds.DateInput("dob")
        # Renders the classic GOV.UK 3-input - Day, Month, Year - date field.

    See :py:class:`fast_gov_uk.design_system.contrib.PastDateInput` and
    :py:class:`fast_gov_uk.design_system.contrib.FutureDateInput` for fields
    that validate whether the date should be in the past or future respectively.

    Args:
        *args: Arguments for Field.
        **kwargs: Additional keyword arguments.

    .. _GOV.UK Date input: https://design-system.service.gov.uk/components/date-input/
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def value(self):
        return self._value

    @property
    async def clean(self):
        """
        Get "clean" data from a field when a form is being processed
        by a form Backend.
        """
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
        """
        Sets date value as well as error if the date value is invalid.
        """
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
        Day field component.
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
        Month field component.
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
        Year field component.
        """
        return _date_input_item(
            self.name,
            "year",
            width=4,
            error=(self.error != ""),
            value=self.value[2] if self.value else "",
        )

    def __ft__(self, *children, **kwargs) -> fh.FT:
        """
        Renders the date input field as a FastHTML component.
        Args:
            *children: Optional children components.
            **kwargs: Additional keyword arguments.
        Returns:
            FT: FastHTML component for DateInput.
        """
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
    """
    Enum to define GOV.UK supported button styles to be passed into
    :py:class:`Button` as `style` param.
    """
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
    `GOV.UK Button`_ component used to help users carry out an action like starting an
    application or saving their information.

    Write button text in sentence case, describing the action it performs. For example:

    - "Start now" at the start of your service
    - "Sign in" to an account a user has already created
    - "Continue" when the service does not save a user"s information
    - "Save and continue" when the service does save a user"s information
    - "Save and come back later" when a user can save their information and come back later
    - "Add another" to add another item to a list or group
    - "Pay" to make a payment
    - "Confirm and send" on a Check answers page that does not have any legal content a user must agree to
    - "Accept and send" on a Check answers page that has legal content a user must agree to
    - "Sign out" when a user is signed in to an account

    Examples:

        >>> ds.Button("Submit")
        # Renders a default button called "Submit"
        >>> ds.Button("Cancel", ButtonStyle.WARNING)
        # Renders a warning button
        >>> ds.Button("Cancel", disabled=True)
        # Renders a disabled button
        >>> ds.Button("Cancel", prevent_double_click=True)
        # Renders a button with some js that prevents double clicks - useful for payments

    Args:
        text (str): The text on the Button component.
        style (ButtonStyle, optional): The style of the Button component. Defaults to ButtonStyle.PRIMARY.
        disabled (bool, optional): Disable the button. Defaults to False.
        prevent_double_click (bool, optional): Prevent accidental double clicks. Defaults to False.
        **kwargs: Any extra args to pass to fh.Button.

    Returns:
        FT: A FastHTML Button component.

    .. _GOV.UK Button: https://design-system.service.gov.uk/components/button/
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
    `GOV.UK Start Button`_ component for call-to-actions. Does not submit form data.

    Examples:

        >>> ds.StartButton("Lets go")
        # Renders a start button with the label "Lets go"
        # This button acts more like a link - it results in a GET request instead of POST

    Args:
        text (str): Text on the Button component.
        href (str): URL of the target page.
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML StartButton component.

    .. _GOV.UK Start Button: https://design-system.service.gov.uk/components/button/
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
    `GOV.UK Button Group`_ component.

    Use a button group when two or more buttons are placed together.

    Examples:

        >>> continue = ds.Button("Continue")
        >>> cancel = ds.Button("Cancel")
        >>> ds.ButtonGroup(contiue, cancel)
        # Renders a button group

    Args:
        *buttons (FT): List of Button components.
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML component.

    .. _GOV.UK Button Group: https://design-system.service.gov.uk/components/button/
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
    cookie_form_link: str = "/cookie-banner",
    confirmation: bool = False,
    **kwargs,
) -> fh.FT:
    """
    `GOV.UK Cookie Banner`_ component.

    Allow users to accept or reject cookies which are not essential to making your service work.

    This component needs links to 2 endpoints on the service -

        1. `cookie_page_link` is a link to the cookies page for your service.
        2. `cookie_form_link` is a link to the cookies form that processes the data when a user submits their cookie preferences through this component.

    Fast-gov-uk comes out of the box with default, minimal implementations of both. In fact,
    fast-gov-uk comes out of the box with a cookie banner for essentail cookies.

    In view of the above, you would only use this component if you are creating a custom cookie
    banner for your service.

    Examples:

        >>> ds.CookieBanner("Test")
        # Renders a standard cookie banner for essential cookies that works out of the box

    Args:
        service_name (str): Name of the service.
        *content (FT): Content of the CookieConfirmation component.
        cookie_page_link (str, optional): Link to the cookie settings page. Defaults to "/cookies".
        cookie_form_link (str, optional): Link to the cookie form submission page. Defaults to "/".
        confirmation (bool, optional): If True, the cookie confirmation is shown. Defaults to False.
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML CookieConfirmation component.

    .. _GOV.UK Cookie Banner: https://design-system.service.gov.uk/components/cookie-banner/
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
    `GOV.UK Fieldset`_ component used to group related form fields.

    Use the fieldset component when you need to show a relationship between multiple form inputs.
    For example, you may need to group a set of text inputs into a single fieldset when asking for
    an address in your service.

    Examples:

        >>> address1 = ds.TextInput("address1", label="Address line 1")
        >>> address2 = ds.TextInput("address2", label="Address line 2")
        >>> town = ds.TextInput("town", label="Town or city")
        >>> postcode = ds.TextInput("postcode", label="Postcode")
        >>> ds.Fieldset(address1, address2, town, postcode)
        # Renders an address fieldset containing multiple, related fields

    Args:
        *fields (Field): Fields to include in the fieldset.
        name (str, optional): Name of the fieldset. Defaults to "".
        legend (str, optional): The legend text for the fieldset.
        heading (str, optional): Heading size. Defaults to "l".
        **kwargs: Additional keyword arguments.

    .. _GOV.UK Fieldset: https://design-system.service.gov.uk/components/fieldset/
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
