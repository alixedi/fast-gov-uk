import pytest

import fast_gov_uk.design_system as ds


@pytest.mark.parametrize(
    "value",
    (
        "test",
        "1234",
        "@",
        "test@",
    ),
)
def test_emailinput_invalid(value, html):
    """Test EmailInput with various parameters.
    Args:
        value (str): The value to assign to EmailInput.
    """
    field = ds.EmailInput(name="test")
    field.value = value
    assert html(field) == html(
        '<div class="govuk-form-group govuk-form-group--error">'
            '<p id="test-error" class="govuk-error-message">'
                '<span class="govuk-visually-hidden">Error: </span>'
                "Value is not an email."
            "</p>"
            f'<input type="text" name="test" value="{value}" aria-describedby="test-hint test-error" id="test" class="govuk-input govuk-input--error">'
        "</div>"
    )


@pytest.mark.parametrize(
    "value",
    (
        "test@test",
        "@test",
    ),
)
def test_emailinput_valid(value, html):
    """Test EmailInput with various parameters.
    Args:
        value (str): The value to assign to EmailInput.
    """
    field = ds.EmailInput(name="test")
    field.value = value
    assert html(field) == html(
        '<div class="govuk-form-group">'
            f'<input type="text" name="test" value="{value}" aria-describedby="test-hint test-error" id="test" class="govuk-input">'
        "</div>"
    )


@pytest.mark.parametrize(
    "value",
    (
        "test",
        "@",
        "5!",
    ),
)
def test_numberinput_invalid(value, html):
    """Test NumberInput with various parameters.
    Args:
        value (str): The value to assign to NumberInput.
    """
    field = ds.NumberInput(name="test")
    field.value = value
    assert html(field) == html(
        '<div class="govuk-form-group govuk-form-group--error">'
            '<p id="test-error" class="govuk-error-message">'
                '<span class="govuk-visually-hidden">Error: </span>'
                "Value is not a number."
            "</p>"
            f'<input type="text" inputmode="numeric" name="test" value="{value}" aria-describedby="test-hint test-error" id="test" class="govuk-input govuk-input--error">'
        "</div>"
    )


@pytest.mark.parametrize(
    "value",
    (
        "5",
        "0",
    ),
)
def test_numberinput_valid(value, html):
    """Test NumberInput with various parameters.
    Args:
        value (str): The value to assign to NumberInput.
    """
    field = ds.NumberInput(name="test")
    field.value = value
    assert html(field) == html(
        '<div class="govuk-form-group">'
            f'<input type="text" inputmode="numeric" name="test" value="{value}" aria-describedby="test-hint test-error" id="test" class="govuk-input">'
        "</div>"
    )


@pytest.mark.parametrize(
    "value",
    (
        "test",
        "@",
        "5!",
    ),
)
def test_decimalinput_invalid(value, html):
    """Test DecimalInput with various parameters.
    Args:
        value (str): The value to assign to DecimalInput.
    """
    field = ds.DecimalInput(name="test")
    field.value = value
    assert html(field) == html(
        '<div class="govuk-form-group govuk-form-group--error">'
            '<p id="test-error" class="govuk-error-message">'
                '<span class="govuk-visually-hidden">Error: </span>'
                "Value is not a number."
            "</p>"
            f'<input type="text" inputmode="numeric" name="test" value="{value}" aria-describedby="test-hint test-error" id="test" class="govuk-input govuk-input--error">'
        "</div>"
    )


@pytest.mark.parametrize(
    "value",
    (
        "5.0",
        ".0",
        "5",
    ),
)
def test_decimalinput_valid(value, html):
    """Test DecimalInput with various parameters.
    Args:
        value (str): The value to assign to DecimalInput.
    """
    field = ds.DecimalInput(name="test")
    field.value = value
    assert html(field) == html(
        '<div class="govuk-form-group">'
            f'<input type="text" inputmode="numeric" name="test" value="{value}" aria-describedby="test-hint test-error" id="test" class="govuk-input">'
        "</div>"
    )


def test_gbpinput_valid(html):
    """
    Test GBPInput renders £ prefix.
    """
    field = ds.GBPInput(name="test")
    field.value = "5"
    assert html(field) == html(
        '<div class="govuk-form-group">'
            '<div class="govuk-input__wrapper">'
                '<div aria-hidden="" class="govuk-input__prefix">£</div>'
                '<input type="text" inputmode="numeric" name="test" value="5" aria-describedby="test-hint test-error" id="test" class="govuk-input">'
            "</div>"
        "</div>"
    )


@pytest.mark.parametrize(
    "kwargs, expected",
    (
        (
            {},
            '<a class="govuk-back-link" href="javascript:history.back()">Back</a>',
        ),
        (
            {"text": "Test"},
            '<a class="govuk-back-link" href="javascript:history.back()">Test</a>',
        ),
        (
            {"inverse": True},
            '<a class="govuk-back-link govuk-back-link--inverse" href="javascript:history.back()">Back</a>',
        ),
    ),
)
def test_backlinkjs(kwargs, expected, html):
    """Test BackLinkJS with various parameters.
    Args:
        kwargs (dict): The arguments to pass to Inset.
        expected (str): The expected HTML output.
    """
    text = ds.BackLinkJS(**kwargs)
    assert html(text) == html(expected)


@pytest.mark.parametrize(
    "value",
    (
        "test",
        "1234",
        "@",
        "test@",
    ),
)
def test_regexinput_invalid(value, html):
    """Test RegexInput with various parameters.
    Args:
        value (str): The value to assign.
    """
    # simplified regex for emails
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    field = ds.RegexInput(name="test", regex=pattern)
    field.value = value
    assert html(field) == html(
        '<div class="govuk-form-group govuk-form-group--error">'
            '<p id="test-error" class="govuk-error-message">'
                '<span class="govuk-visually-hidden">Error: </span>'
                "Value does not match the required format."
            "</p>"
            f'<input type="text" name="test" value="{value}" aria-describedby="test-hint test-error" id="test" class="govuk-input govuk-input--error">'
        "</div>"
    )


@pytest.mark.parametrize(
    "value",
    (
        "test@test.com",
        "test2@test2.net",
    ),
)
def test_regexinput_valid(value, html):
    """Test RegexInput with various parameters.
    Args:
        value (str): The value to assign.
    """
    # simplified regex for emails
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    field = ds.RegexInput(name="test", regex=pattern)
    field.value = value
    assert html(field) == html(
        '<div class="govuk-form-group">'
            f'<input type="text" name="test" value="{value}" aria-describedby="test-hint test-error" id="test" class="govuk-input">'
        "</div>"
    )


@pytest.mark.parametrize(
    "value",
    (
        ["1", "1", "2002"],
        ["1", "1", "1200"],
    ),
)
def test_pastdateinput_valid(value, html):
    """Test PastDateInput with various parameters.
    Args:
        value (str): The value to assign.
    """
    # simplified regex for emails
    field = ds.PastDateInput(name="test")
    field.value = value
    assert html(field) == html(
        '<div class="govuk-form-group">'
            '<fieldset aria-describedby="test-hint" class="govuk-fieldset" role="group">'
                '<div class="govuk-date-input" id="test">'
                    '<div class="govuk-date-input__item">'
                        '<div class="govuk-form-group" id="test-day">'
                            '<label class="govuk-label govuk-date-input__label" for="test-day-input">Day</label>'
                            f'<input class="govuk-input govuk-date-input__input govuk-input--width-2" id="test-day-input" inputmode="numeric" name="test" type="text" value="{value[0]}"/>'
                        "</div>"
                    "</div>"
                    '<div class="govuk-date-input__item">'
                        '<div class="govuk-form-group" id="test-month">'
                            '<label class="govuk-label govuk-date-input__label" for="test-month-input">Month</label>'
                            f'<input class="govuk-input govuk-date-input__input govuk-input--width-2" id="test-month-input" inputmode="numeric" name="test" type="text" value="{value[1]}"/>'
                        "</div>"
                    "</div>"
                    '<div class="govuk-date-input__item">'
                        '<div class="govuk-form-group" id="test-year">'
                            '<label class="govuk-label govuk-date-input__label" for="test-year-input">Year</label>'
                            f'<input class="govuk-input govuk-date-input__input govuk-input--width-4" id="test-year-input" inputmode="numeric" name="test" type="text" value="{value[2]}"/>'
                        "</div>"
                    "</div>"
                "</div>"
            "</fieldset>"
        "</div>"
    )


@pytest.mark.parametrize(
    "value, error",
    (
        (["1", "1", "2032"], "The date must be in the past."),
        (["1", "1", "3000"], "The date must be in the past."),
        (["", "1", "2000"], "This field is required."),
        (["1", "", "2000"], "This field is required."),
        (["1", "2", ""], "This field is required."),
        (["not-number", "1", "2000"], "Invalid values."),
        (["1", "not-number", "2000"], "Invalid values."),
        (["1", "1", "not-number"], "Invalid values."),
    ),
)
def test_pastdateinput_invalid(value, error, html):
    """Test PastDateInput with various parameters.
    Args:
        value (str): The value to assign.
    """
    # simplified regex for emails
    field = ds.PastDateInput(name="test")
    field.value = value
    v0 = f'value="{field.value[0]}"' if field.value[0] else ""
    v1 = f'value="{field.value[1]}"' if field.value[1] else ""
    v2 = f'value="{field.value[2]}"' if field.value[2] else ""
    assert html(field) == html(
        '<div class="govuk-form-group govuk-form-group--error">'
            '<p class="govuk-error-message" id="test-error">'
                '<span class="govuk-visually-hidden">Error:</span>'
                f"{error}"
            "</p>"
            '<fieldset aria-describedby="test-hint" class="govuk-fieldset" role="group">'
                '<div class="govuk-date-input" id="test">'
                    '<div class="govuk-date-input__item">'
                        '<div class="govuk-form-group" id="test-day">'
                            '<label class="govuk-label govuk-date-input__label" for="test-day-input">Day</label>'
                            f'<input class="govuk-input govuk-date-input__input govuk-input--width-2 govuk-input--error" id="test-day-input" inputmode="numeric" name="test" type="text" {v0}/>'
                        "</div>"
                    "</div>"
                    '<div class="govuk-date-input__item">'
                        '<div class="govuk-form-group" id="test-month">'
                            '<label class="govuk-label govuk-date-input__label" for="test-month-input">Month</label>'
                            f'<input class="govuk-input govuk-date-input__input govuk-input--width-2 govuk-input--error" id="test-month-input" inputmode="numeric" name="test" type="text" {v1}/>'
                        "</div>"
                    "</div>"
                    '<div class="govuk-date-input__item">'
                        '<div class="govuk-form-group" id="test-year">'
                            '<label class="govuk-label govuk-date-input__label" for="test-year-input">Year</label>'
                            f'<input class="govuk-input govuk-date-input__input govuk-input--width-4 govuk-input--error" id="test-year-input" inputmode="numeric" name="test" type="text" {v2}/>'
                        "</div>"
                    "</div>"
                "</div>"
            "</fieldset>"
        "</div>"
    )


@pytest.mark.parametrize(
    "value",
    (
        ["1", "1", "2032"],
        ["1", "1", "3000"],
    ),
)
def test_futuredateinput_valid(value, html):
    """Test FutureDateInput with various parameters.
    Args:
        value (str): The value to assign.
    """
    # simplified regex for emails
    field = ds.FutureDateInput(name="test")
    field.value = value
    assert html(field) == html(
        '<div class="govuk-form-group">'
            '<fieldset aria-describedby="test-hint" class="govuk-fieldset" role="group">'
                '<div class="govuk-date-input" id="test">'
                    '<div class="govuk-date-input__item">'
                        '<div class="govuk-form-group" id="test-day">'
                            '<label class="govuk-label govuk-date-input__label" for="test-day-input">Day</label>'
                            f'<input class="govuk-input govuk-date-input__input govuk-input--width-2" id="test-day-input" inputmode="numeric" name="test" type="text" value="{value[0]}"/>'
                        "</div>"
                    "</div>"
                    '<div class="govuk-date-input__item">'
                        '<div class="govuk-form-group" id="test-month">'
                            '<label class="govuk-label govuk-date-input__label" for="test-month-input">Month</label>'
                            f'<input class="govuk-input govuk-date-input__input govuk-input--width-2" id="test-month-input" inputmode="numeric" name="test" type="text" value="{value[1]}"/>'
                        "</div>"
                    "</div>"
                    '<div class="govuk-date-input__item">'
                        '<div class="govuk-form-group" id="test-year">'
                            '<label class="govuk-label govuk-date-input__label" for="test-year-input">Year</label>'
                            f'<input class="govuk-input govuk-date-input__input govuk-input--width-4" id="test-year-input" inputmode="numeric" name="test" type="text" value="{value[2]}"/>'
                        "</div>"
                    "</div>"
                "</div>"
            "</fieldset>"
        "</div>"
    )


@pytest.mark.parametrize(
    "value, error",
    (
        (["1", "1", "2020"], "The date must be in the future."),
        (["1", "1", "1900"], "The date must be in the future."),
        (["", "1", "2000"], "This field is required."),
        (["1", "", "2000"], "This field is required."),
        (["1", "2", ""], "This field is required."),
        (["not-number", "1", "2000"], "Invalid values."),
        (["1", "not-number", "2000"], "Invalid values."),
        (["1", "1", "not-number"], "Invalid values."),
    ),
)
def test_futuredateinput_invalid(value, error, html):
    """Test PastDateInput with various parameters.
    Args:
        value (str): The value to assign.
    """
    # simplified regex for emails
    field = ds.FutureDateInput(name="test")
    field.value = value
    v0 = f'value="{field.value[0]}"' if field.value[0] else ""
    v1 = f'value="{field.value[1]}"' if field.value[1] else ""
    v2 = f'value="{field.value[2]}"' if field.value[2] else ""
    assert html(field) == html(
        '<div class="govuk-form-group govuk-form-group--error">'
            '<p class="govuk-error-message" id="test-error">'
                '<span class="govuk-visually-hidden">Error:</span>'
                f"{error}"
            "</p>"
            '<fieldset aria-describedby="test-hint" class="govuk-fieldset" role="group">'
                '<div class="govuk-date-input" id="test">'
                    '<div class="govuk-date-input__item">'
                        '<div class="govuk-form-group" id="test-day">'
                            '<label class="govuk-label govuk-date-input__label" for="test-day-input">Day</label>'
                            f'<input class="govuk-input govuk-date-input__input govuk-input--width-2 govuk-input--error" id="test-day-input" inputmode="numeric" name="test" type="text" {v0}/>'
                        "</div>"
                    "</div>"
                    '<div class="govuk-date-input__item">'
                        '<div class="govuk-form-group" id="test-month">'
                            '<label class="govuk-label govuk-date-input__label" for="test-month-input">Month</label>'
                            f'<input class="govuk-input govuk-date-input__input govuk-input--width-2 govuk-input--error" id="test-month-input" inputmode="numeric" name="test" type="text" {v1}/>'
                        "</div>"
                    "</div>"
                    '<div class="govuk-date-input__item">'
                        '<div class="govuk-form-group" id="test-year">'
                            '<label class="govuk-label govuk-date-input__label" for="test-year-input">Year</label>'
                            f'<input class="govuk-input govuk-date-input__input govuk-input--width-4 govuk-input--error" id="test-year-input" inputmode="numeric" name="test" type="text" {v2}/>'
                        "</div>"
                    "</div>"
                "</div>"
            "</fieldset>"
        "</div>"
    )


@pytest.mark.parametrize("field", (
    ds.EmailInput,
    ds.NumberInput,
    ds.DecimalInput,
    ds.GBPInput,
    ds.RegexInput,
    ds.PastDateInput,
    ds.FutureDateInput,
))
def test_html_attribute(field, html):
    """
    Test that passes an html attribute to all fields - that is not
    explicitly handled but should be passed through to the
    underlying component.
    """
    f = field(name="test", label="Test Label", hx_test="foo")
    # TODO: assert exact errors :/
    assert 'hx-test="foo"' in html(f)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "field, value, clean",
    (
        (ds.NumberInput, "123", 123),
        (ds.NumberInput, "", None),
        (ds.DecimalInput, "12.3", 12.3),
        (ds.DecimalInput, "", None),
    )
)
async def test_clean(field, value, clean):
    """
    Test that assigns a value to the field and checks if the
    clean aatribute returns the right data and type.
    """
    f = field(name="test", label="Test Label")
    f.value = value
    assert await f.clean == clean


@pytest.mark.parametrize("field, value", (
    (ds.EmailInput, ""),
    (ds.NumberInput, ""),
    (ds.DecimalInput, ""),
    (ds.GBPInput, ""),
    (ds.RegexInput, ""),
    (ds.PastDateInput, ["", "", ""]),
    (ds.FutureDateInput, ["", "", ""]),
))
def test_required_error(field, value):
    """
    Test that when we assign no value to a required field,
    the right error is set.
    """
    f = field(name="test", label="Test Label")
    f.value = value
    assert f.error == "This field is required."
