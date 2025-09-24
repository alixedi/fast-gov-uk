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
    email = ds.EmailInput(name="test")
    email.value = value
    assert html(email) == html(
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
    email = ds.EmailInput(name="test")
    email.value = value
    assert html(email) == html(
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
    email = ds.NumberInput(name="test")
    email.value = value
    assert html(email) == html(
        '<div class="govuk-form-group govuk-form-group--error">'
            '<p id="test-error" class="govuk-error-message">'
                '<span class="govuk-visually-hidden">Error: </span>'
                "Value is not a number."
            "</p>"
            f'<input type="text" name="test" value="{value}" aria-describedby="test-hint test-error" id="test" class="govuk-input govuk-input--error">'
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
    email = ds.NumberInput(name="test")
    email.value = value
    assert html(email) == html(
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
def test_decimalinput_invalid(value, html):
    """Test DecimalInput with various parameters.
    Args:
        value (str): The value to assign to DecimalInput.
    """
    email = ds.DecimalInput(name="test")
    email.value = value
    assert html(email) == html(
        '<div class="govuk-form-group govuk-form-group--error">'
            '<p id="test-error" class="govuk-error-message">'
                '<span class="govuk-visually-hidden">Error: </span>'
                "Value is not a number."
            "</p>"
            f'<input type="text" name="test" value="{value}" aria-describedby="test-hint test-error" id="test" class="govuk-input govuk-input--error">'
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
    email = ds.DecimalInput(name="test")
    email.value = value
    assert html(email) == html(
        '<div class="govuk-form-group">'
            f'<input type="text" name="test" value="{value}" aria-describedby="test-hint test-error" id="test" class="govuk-input">'
        "</div>"
    )
