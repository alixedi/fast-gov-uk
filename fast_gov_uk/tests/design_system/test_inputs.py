import fasthtml.common as fh
from fast_gov_uk import forms
import pytest

import fast_gov_uk.design_system as ds


@pytest.mark.parametrize(
    "kwargs, expected",
    (
        (
            {"name": "test"},
            ('<div class="govuk-form-group"></div>'),
        ),
        (
            {"name": "test", "label": "Test Label"},
            (
                '<div class="govuk-form-group">'
                '<label for="test" class="govuk-label">Test Label</label>'
                "</div>"
            ),
        ),
        (
            {"name": "test", "label": "Test Label", "heading": "l"},
            (
                '<div class="govuk-form-group">'
                    '<h1 class="govuk-label-wrapper">'
                        '<label for="test" class="govuk-label govuk-label--l">Test Label</label>'
                    "</h1>"
                "</div>"
            ),
        ),
        (
            {"name": "test", "hint": "Test Hint"},
            (
                '<div class="govuk-form-group">'
                    '<div id="test-hint" class="govuk-hint">Test Hint</div>'
                "</div>"
            ),
        ),
        (
            {"name": "test", "error": "Test Error"},
            (
                '<div class="govuk-form-group govuk-form-group--error">'
                    '<p id="test-error" class="govuk-error-message">'
                        '<span class="govuk-visually-hidden">Error: </span>'
                        "Test Error"
                    "</p>"
                "</div>"
            ),
        ),
    ),
)
def test_field(kwargs, expected, html):
    """Test Field with various parameters.
    Args:
        kwargs (dict): The arguments to pass to Field.
        expected (str): The expected HTML output.
    """
    field = ds.Field(**kwargs)
    assert html(field) == html(expected)


def test_field_required(html):
    """Test Field with required attribute."""
    field = ds.Field("test", label="Test")
    field.value = ""
    assert html(field) == html(
        '<div class="govuk-form-group govuk-form-group--error">'
            '<label for="test" class="govuk-label">Test</label>'
            '<p id="test-error" class="govuk-error-message">'
                '<span class="govuk-visually-hidden">Error: </span>'
                "This field is required."
            "</p>"
        "</div>"
    )


def test_field_optional(html):
    """Test Field with required=False."""
    field = ds.Field("test", label="Test", required=False)
    field.value = ""
    assert html(field) == html(
        '<div class="govuk-form-group">'
            '<label for="test" class="govuk-label">Test (Optional)</label>'
        "</div>"
    )


@pytest.mark.parametrize(
    "kwargs, expected",
    (
        (
            {"name": "test", "choices": {"1": "Option 1", "2": "Option 2"}},
            (
                '<div class="govuk-form-group">'
                    '<select name="test" id="test" class="govuk-select">'
                        '<option value="1">Option 1</option>'
                        '<option value="2">Option 2</option>'
                    "</select>"
                "</div>"
            ),
        ),
        (
            {"name": "test", "options": [], "label": "Test Label"},
            (
                '<div class="govuk-form-group">'
                    '<label for="test" class="govuk-label">Test Label</label>'
                    '<select name="test" id="test" class="govuk-select">'
                    "</select>"
                "</div>"
            ),
        ),
        (
            {"name": "test", "options": [], "hint": "Test Hint"},
            (
                '<div class="govuk-form-group">'
                    '<div id="test-hint" class="govuk-hint">Test Hint</div>'
                    '<select name="test" id="test" class="govuk-select">'
                    "</select>"
                "</div>"
            ),
        ),
        (
            {"name": "test", "options": [], "error": "Test Error"},
            (
                '<div class="govuk-form-group govuk-form-group--error">'
                    '<p id="test-error" class="govuk-error-message">'
                        '<span class="govuk-visually-hidden">Error: </span>'
                        "Test Error"
                    "</p>"
                    '<select name="test" id="test" class="govuk-select govuk-select--error">'
                    "</select>"
                "</div>"
            ),
        ),
    ),
)
def test_select(kwargs, expected, html):
    """Test Select with various parameters.
    Args:
        kwargs (dict): The arguments to pass to Select.
        expected (str): The expected HTML output.
    """
    select = ds.Select(**kwargs)
    assert html(select) == html(expected)


def test_select_value(html):
    """Test Select with value."""
    select = ds.Select(
        name="test",
        choices={"yes": "Yes", "no": "No"},
    )
    select.value = "yes"
    assert html(select) == html(
        '<div class="govuk-form-group">'
            '<select name="test" id="test" class="govuk-select">'
                '<option value="yes" selected>Yes</option>'
                '<option value="no">No</option>'
            "</select>"
        "</div>"
    )


@pytest.mark.parametrize(
    "kwargs, expected",
    (
        (
            {"name": "test"},
            (
                '<div class="govuk-form-group">'
                    '<textarea name="test" rows="5" aria-describedby="test-hint test-error" id="test" class="govuk-textarea">'
                    "</textarea>"
                "</div>"
            ),
        ),
        (
            {"name": "test", "label": "Test Label"},
            (
                '<div class="govuk-form-group">'
                    '<label for="test" class="govuk-label">Test Label</label>'
                    '<textarea name="test" rows="5" aria-describedby="test-hint test-error" id="test" class="govuk-textarea">'
                    "</textarea>"
                "</div>"
            ),
        ),
        (
            {"name": "test", "label": "Test Label", "heading": "l"},
            (
                '<div class="govuk-form-group">'
                    '<h1 class="govuk-label-wrapper">'
                        '<label for="test" class="govuk-label govuk-label--l">Test Label</label>'
                    "</h1>"
                    '<textarea name="test" rows="5" aria-describedby="test-hint test-error" id="test" class="govuk-textarea">'
                    "</textarea>"
                "</div>"
            ),
        ),
        (
            {"name": "test", "hint": "Test Hint"},
            (
                '<div class="govuk-form-group">'
                    '<div id="test-hint" class="govuk-hint">Test Hint</div>'
                    '<textarea name="test" rows="5" aria-describedby="test-hint test-error" id="test" class="govuk-textarea">'
                    "</textarea>"
                "</div>"
            ),
        ),
        (
            {"name": "test", "error": "Test Error"},
            (
                '<div class="govuk-form-group govuk-form-group--error">'
                    '<p id="test-error" class="govuk-error-message">'
                        '<span class="govuk-visually-hidden">Error: </span>'
                        "Test Error"
                    "</p>"
                    '<textarea name="test" rows="5" aria-describedby="test-hint test-error" id="test" class="govuk-textarea govuk-textarea--error">'
                    "</textarea>"
                "</div>"
            ),
        ),
        (
            {"name": "test", "rows": 10},
            (
                '<div class="govuk-form-group">'
                    '<textarea name="test" rows="10" aria-describedby="test-hint test-error" id="test" class="govuk-textarea">'
                    "</textarea>"
                "</div>"
            ),
        ),
    ),
)
def test_textarea(kwargs, expected, html):
    """Test Textarea with various parameters.
    Args:
        kwargs (dict): The arguments to pass to Textarea.
        expected (str): The expected HTML output.
    """
    textarea = ds.Textarea(**kwargs)
    assert html(textarea) == html(expected)


@pytest.mark.parametrize(
    "kwargs, expected",
    (
        (
            {"name": "test"},
            (
                '<div data-module="govuk-password-input" class="govuk-form-group govuk-password-input">'
                    '<div class="govuk-input__wrapper govuk-password-input__wrapper">'
                        '<input type="password" name="test" aria-describedby="test-hint test-error" id="test" class="govuk-input govuk-password-input__input govuk-js-password-input-input">'
                        '<button type="button" data-module="govuk-password-input__toggle" aria-controls="test" aria-label="Show password" hidden class="govuk-button govuk-button--secondary govuk-password-input__toggle govuk-js-password-input-toggle">Show</button>'
                    "</div>"
                "</div>"
            ),
        ),
        (
            {"name": "test", "label": "Test Label"},
            (
                '<div data-module="govuk-password-input" class="govuk-form-group govuk-password-input">'
                    '<label for="test" class="govuk-label">Test Label</label>'
                    '<div class="govuk-input__wrapper govuk-password-input__wrapper">'
                        '<input type="password" name="test" aria-describedby="test-hint test-error" id="test" class="govuk-input govuk-password-input__input govuk-js-password-input-input">'
                        '<button type="button" data-module="govuk-password-input__toggle" aria-controls="test" aria-label="Show password" hidden class="govuk-button govuk-button--secondary govuk-password-input__toggle govuk-js-password-input-toggle">Show</button>'
                    "</div>"
                "</div>"
            ),
        ),
        (
            {"name": "test", "hint": "Test Hint"},
            (
                '<div data-module="govuk-password-input" class="govuk-form-group govuk-password-input">'
                    '<div id="test-hint" class="govuk-hint">Test Hint</div>'
                    '<div class="govuk-input__wrapper govuk-password-input__wrapper">'
                        '<input type="password" name="test" aria-describedby="test-hint test-error" id="test" class="govuk-input govuk-password-input__input govuk-js-password-input-input">'
                        '<button type="button" data-module="govuk-password-input__toggle" aria-controls="test" aria-label="Show password" hidden class="govuk-button govuk-button--secondary govuk-password-input__toggle govuk-js-password-input-toggle">Show</button>'
                    "</div>"
                "</div>"
            ),
        ),
        (
            {"name": "test", "error": "Test Error"},
            (
                '<div data-module="govuk-password-input" class="govuk-form-group govuk-password-input govuk-form-group--error">'
                    '<p id="test-error" class="govuk-error-message">'
                        '<span class="govuk-visually-hidden">Error: </span>'
                        "Test Error"
                    "</p>"
                    '<div class="govuk-input__wrapper govuk-password-input__wrapper">'
                        '<input type="password" name="test" aria-describedby="test-hint test-error" id="test" class="govuk-input govuk-password-input__input govuk-js-password-input-input govuk-input--error">'
                        '<button type="button" data-module="govuk-password-input__toggle" aria-controls="test" aria-label="Show password" hidden class="govuk-button govuk-button--secondary govuk-password-input__toggle govuk-js-password-input-toggle">Show</button>'
                    "</div>"
                "</div>"
            ),
        ),
    ),
)
def test_passwordinput(kwargs, expected, html):
    """Test PasswordInput with various parameters.
    Args:
        kwargs (dict): The arguments to pass to PasswordInput.
        expected (str): The expected HTML output.
    """
    password = ds.PasswordInput(**kwargs)
    assert html(password) == html(expected)


def test_fieldset(html):
    """Test Fieldset with various parameters."""
    fieldset = ds.Fieldset(
        fh.P("Test Content 1"),
        fh.P("Test Content 2"),
        legend="Test Legend",
    )
    expected = (
        '<fieldset class="govuk-fieldset">'
            '<legend class="govuk-fieldset__legend govuk-fieldset__legend--l">'
                '<h1 class="govuk-fieldset__heading">Test Legend</h1>'
            "</legend>"
            "<p>Test Content 1</p>"
            "<p>Test Content 2</p>"
        "</fieldset>"
    )
    assert html(fieldset) == html(expected)


@pytest.mark.parametrize(
    "kwargs, expected",
    (
        (
            {"name": "test", "maxchars": 200},
            (
                '<div data-module="govuk-character-count" data-maxlength="200" class="govuk-form-group govuk-character-count">'
                    '<textarea name="test" rows="5" aria-describedby="test-hint test-error" id="test" class="govuk-textarea govuk-js-character-count"></textarea>'
                    '<div id="test-info" class="govuk-hint govuk-character-count__message">'
                        "You can enter up to 200 characters."
                    "</div>"
                "</div>"
            ),
        ),
        (
            {"name": "test", "maxchars": 200, "threshold": 100},
            (
                '<div data-module="govuk-character-count" data-maxlength="200" data-threshold="100" class="govuk-form-group govuk-character-count">'
                    '<textarea name="test" rows="5" aria-describedby="test-hint test-error" id="test" class="govuk-textarea govuk-js-character-count"></textarea>'
                    '<div id="test-info" class="govuk-hint govuk-character-count__message">'
                        "You can enter up to 200 characters."
                    "</div>"
                "</div>"
            ),
        ),
        (
            {"name": "test", "maxwords": 50},
            (
                '<div data-module="govuk-character-count" data-maxwords="50" class="govuk-form-group govuk-character-count">'
                    '<textarea name="test" rows="5" aria-describedby="test-hint test-error" id="test" class="govuk-textarea govuk-js-character-count"></textarea>'
                    '<div id="test-info" class="govuk-hint govuk-character-count__message">'
                        "You can enter up to 50 words."
                    "</div>"
                "</div>"
            ),
        ),
        (
            {"name": "test", "maxwords": 50, "hint": "Test Hint"},
            (
                '<div data-module="govuk-character-count" data-maxwords="50" class="govuk-form-group govuk-character-count">'
                    '<div id="test-hint" class="govuk-hint">Test Hint</div>'
                    '<textarea name="test" rows="5" aria-describedby="test-hint test-error" id="test" class="govuk-textarea govuk-js-character-count"></textarea>'
                    '<div id="test-info" class="govuk-hint govuk-character-count__message">'
                        "You can enter up to 50 words."
                    "</div>"
                "</div>"
            ),
        ),
        (
            {"name": "test", "maxwords": 50, "label": "Test Label"},
            (
                '<div data-module="govuk-character-count" data-maxwords="50" class="govuk-form-group govuk-character-count">'
                    '<label for="test" class="govuk-label">Test Label</label>'
                    '<textarea name="test" rows="5" aria-describedby="test-hint test-error" id="test" class="govuk-textarea govuk-js-character-count"></textarea>'
                    '<div id="test-info" class="govuk-hint govuk-character-count__message">'
                        "You can enter up to 50 words."
                    "</div>"
                "</div>"
            ),
        ),
        (
            {"name": "test", "maxwords": 50, "label": "Test Label", "heading": "l"},
            (
                '<div data-module="govuk-character-count" data-maxwords="50" class="govuk-form-group govuk-character-count">'
                    '<h1 class="govuk-label-wrapper"><label for="test" class="govuk-label govuk-label--l">Test Label</label></h1>'
                    '<textarea name="test" rows="5" aria-describedby="test-hint test-error" id="test" class="govuk-textarea govuk-js-character-count"></textarea>'
                    '<div id="test-info" class="govuk-hint govuk-character-count__message">'
                        "You can enter up to 50 words."
                    "</div>"
                "</div>"
            ),
        ),
    ),
)
def test_charactercount(kwargs, expected, html):
    """Test CharacterCount with various parameters.
    Args:
        kwargs (dict): The arguments to pass to CharacterCount.
        expected (str): The expected HTML output.
    """
    charcount = ds.CharacterCount(**kwargs)
    assert html(charcount) == html(expected)


@pytest.mark.parametrize(
    "kwargs, error",
    (
        ({"name": "test", "maxchars": 3}, "Characters exceed limit of 3."),
        ({"name": "test", "maxwords": 1}, "Words exceed limit of 1."),
    ),
)
def test_charactercount_invalid(kwargs, error):
    charcount = ds.CharacterCount(**kwargs)
    charcount.value = "A quick brown fox..."
    assert charcount.error == error


@pytest.mark.parametrize(
    "kwargs, expected",
    (
        (
            {"style": ds.ButtonStyle.PRIMARY},
            '<button type="submit" data-module="govuk-button" class="govuk-button">test1</button>'
        ),
        (
            {"style": ds.ButtonStyle.SECONDARY},
            '<button type="submit" data-module="govuk-button" class="govuk-button govuk-button--secondary">test1</button>'
        ),
        (
            {"style": ds.ButtonStyle.WARNING},
            '<button type="submit" data-module="govuk-button" class="govuk-button govuk-button--warning">test1</button>'
        ),
        (
            {"style": ds.ButtonStyle.INVERSE},
            '<button type="submit" data-module="govuk-button" class="govuk-button govuk-button--inverse">test1</button>'
        ),
        (
            {"disabled": True},
            '<button type="submit" disabled aria-disabled data-module="govuk-button" class="govuk-button">test1</button>'
        ),
        (
            {"prevent_double_click": True},
            '<button type="submit" data-prevent-double-click data-module="govuk-button" class="govuk-button">test1</button>'
        ),
    )
)
def test_button(kwargs, expected, html):
    """
    Test Table with various parameters.
    """
    button = ds.Button("test1", **kwargs)
    assert html(button) == html(expected)


def test_start_button(html):
    """
    Test Table with various parameters.
    """
    start = ds.StartButton("Test", "/test")
    expected = (
        '<a href="/test" role="button" draggable="false" data-module="govuk-button" class="govuk-button govuk-button--start">'
            "Test"
            '<svg class="govuk-button__start-icon" xmlns="http://www.w3.org/2000/svg" width="17.5" '
            'height="19" viewBox="0 0 33 40" aria-hidden="true" focusable="false">'
            '<path fill="currentColor" d="M0 0h13l20 20-20 20H0l20-20z" />'
            "</svg>"
        "</a>"
    )
    assert html(start) == html(expected)


@pytest.mark.parametrize(
    "kwargs, expected",
    (
        (
            {"name": "test"},
            (
                '<div class="govuk-form-group">'
                    '<input type="text" name="test" aria-describedby="test-hint test-error" id="test" class="govuk-input">'
                "</div>"
            ),
        ),
        (
            {"name": "test", "label": "Test Label"},
            (
                '<div class="govuk-form-group">'
                    '<label for="test" class="govuk-label">Test Label</label>'
                    '<input type="text" name="test" aria-describedby="test-hint test-error" id="test" class="govuk-input">'
                "</div>"
            ),
        ),
        (
            {"name": "test", "label": "Test Label", "heading": "l"},
            (
                '<div class="govuk-form-group">'
                    '<h1 class="govuk-label-wrapper">'
                        '<label for="test" class="govuk-label govuk-label--l">Test Label</label>'
                    "</h1>"
                    '<input type="text" name="test" aria-describedby="test-hint test-error" id="test" class="govuk-input">'
                "</div>"
            ),
        ),
        (
            {"name": "test", "hint": "Test Hint"},
            (
                '<div class="govuk-form-group">'
                    '<div id="test-hint" class="govuk-hint">Test Hint</div>'
                    '<input type="text" name="test" aria-describedby="test-hint test-error" id="test" class="govuk-input">'
                "</div>"
            ),
        ),
        (
            {"name": "test", "error": "Test Error"},
            (
                '<div class="govuk-form-group govuk-form-group--error">'
                    '<p id="test-error" class="govuk-error-message">'
                        '<span class="govuk-visually-hidden">Error: </span>'
                        "Test Error"
                    "</p>"
                    '<input type="text" name="test" aria-describedby="test-hint test-error" id="test" class="govuk-input govuk-input--error">'
                "</div>"
            ),
        ),
        (
            {"name": "test", "width": ds.InputWidth.W20},
            (
                '<div class="govuk-form-group">'
                    '<input type="text" name="test" aria-describedby="test-hint test-error" id="test" class="govuk-input govuk-input--width-20">'
                "</div>"
            ),
        ),
        (
            {"name": "test", "width": ds.InputWidth.W10},
            (
                '<div class="govuk-form-group">'
                    '<input type="text" name="test" aria-describedby="test-hint test-error" id="test" class="govuk-input govuk-input--width-10">'
                "</div>"
            ),
        ),
        (
            {"name": "test", "width": ds.InputWidth.W5},
            (
                '<div class="govuk-form-group">'
                    '<input type="text" name="test" aria-describedby="test-hint test-error" id="test" class="govuk-input govuk-input--width-5">'
                "</div>"
            ),
        ),
        (
            {"name": "test", "width": ds.InputWidth.W4},
            (
                '<div class="govuk-form-group">'
                    '<input type="text" name="test" aria-describedby="test-hint test-error" id="test" class="govuk-input govuk-input--width-4">'
                "</div>"
            ),
        ),
        (
            {"name": "test", "width": ds.InputWidth.W3},
            (
                '<div class="govuk-form-group">'
                    '<input type="text" name="test" aria-describedby="test-hint test-error" id="test" class="govuk-input govuk-input--width-3">'
                "</div>"
            ),
        ),
        (
            {"name": "test", "width": ds.InputWidth.W2},
            (
                '<div class="govuk-form-group">'
                    '<input type="text" name="test" aria-describedby="test-hint test-error" id="test" class="govuk-input govuk-input--width-2">'
                "</div>"
            ),
        ),
        (
            {"name": "test", "width": ds.InputWidth.WFULL},
            (
                '<div class="govuk-form-group">'
                    '<input type="text" name="test" aria-describedby="test-hint test-error" id="test" class="govuk-input govuk-!-width-full">'
                "</div>"
            ),
        ),
        (
            {"name": "test", "width": ds.InputWidth.W75},
            (
                '<div class="govuk-form-group">'
                    '<input type="text" name="test" aria-describedby="test-hint test-error" id="test" class="govuk-input govuk-!-width-three-quarters">'
                "</div>"
            ),
        ),
        (
            {"name": "test", "width": ds.InputWidth.W66},
            (
                '<div class="govuk-form-group">'
                    '<input type="text" name="test" aria-describedby="test-hint test-error" id="test" class="govuk-input govuk-!-width-two-thirds">'
                "</div>"
            ),
        ),
        (
            {"name": "test", "width": ds.InputWidth.W50},
            (
                '<div class="govuk-form-group">'
                    '<input type="text" name="test" aria-describedby="test-hint test-error" id="test" class="govuk-input govuk-!-width-one-half">'
                "</div>"
            ),
        ),
        (
            {"name": "test", "width": ds.InputWidth.W33},
            (
                '<div class="govuk-form-group">'
                    '<input type="text" name="test" aria-describedby="test-hint test-error" id="test" class="govuk-input govuk-!-width-one-third">'
                "</div>"
            ),
        ),
        (
            {"name": "test", "width": ds.InputWidth.W25},
            (
                '<div class="govuk-form-group">'
                    '<input type="text" name="test" aria-describedby="test-hint test-error" id="test" class="govuk-input govuk-!-width-one-quarter">'
                "</div>"
            ),
        ),
        (
            {"name": "test", "autocomplete": "postal-code"},
            (
                '<div class="govuk-form-group">'
                    '<input type="text" name="test" aria-describedby="test-hint test-error" autocomplete="postal-code" id="test" class="govuk-input">'
                "</div>"
            ),
        ),
        (
            {"name": "test", "numeric": True},
            (
                '<div class="govuk-form-group">'
                    '<input type="text" name="test" aria-describedby="test-hint test-error" inputmode="numeric" id="test" class="govuk-input">'
                "</div>"
            ),
        ),
        (
            {"name": "test", "spellcheck": True},
            (
                '<div class="govuk-form-group">'
                    '<input type="text" name="test" aria-describedby="test-hint test-error" spellcheck id="test" class="govuk-input">'
                "</div>"
            ),
        ),
        (
            {"name": "test", "prefix": "?"},
            (
                '<div class="govuk-form-group">'
                    '<div class="govuk-input__wrapper">'
                        '<div aria-hidden class="govuk-input__prefix">?</div>'
                        '<input type="text" name="test" aria-describedby="test-hint test-error" id="test" class="govuk-input">'
                    "</div>"
                "</div>"
            ),
        ),
        (
            {"name": "test", "suffix": "?"},
            (
                '<div class="govuk-form-group">'
                    '<div class="govuk-input__wrapper">'
                        '<input type="text" name="test" aria-describedby="test-hint test-error" id="test" class="govuk-input">'
                        '<div aria-hidden class="govuk-input__suffix">?</div>'
                    "</div>"
                "</div>"
            ),
        ),
    ),
)
def test_textinput(kwargs, expected, html):
    """Test TextInput with various parameters.
    Args:
        kwargs (dict): The arguments to pass to TextInput.
        expected (str): The expected HTML output.
    """
    input = ds.TextInput(**kwargs)
    assert html(input) == html(expected)


@pytest.mark.parametrize(
    "kwargs, expected",
    (
        (
            {"name": "test", "value": "banana", "label": "Test Label"},
            (
                '<div class="govuk-checkboxes__item">'
                    '<input id="test-banana" name="test" type="checkbox" value="banana" class="govuk-checkboxes__input">'
                    '<label for="test-banana" class="govuk-label govuk-checkboxes__label">Test Label</label>'
                "</div>"
            ),
        ),
        (
            {"name": "test", "value": "banana", "label": "Test Label", "checked": True},
            (
                '<div class="govuk-checkboxes__item">'
                    '<input id="test-banana" name="test" type="checkbox" value="banana" checked class="govuk-checkboxes__input">'
                    '<label for="test-banana" class="govuk-label govuk-checkboxes__label">Test Label</label>'
                "</div>"
            ),
        ),
        (
            {
                "name": "test",
                "value": "banana",
                "label": "Test Label",
                "hint": "Test Hint",
            },
            (
                '<div class="govuk-checkboxes__item">'
                    '<input id="test-banana" name="test" type="checkbox" value="banana" class="govuk-checkboxes__input">'
                    '<label for="test-banana" class="govuk-label govuk-checkboxes__label">Test Label</label>'
                    '<div id="test-banana-hint" class="govuk-hint govuk-checkboxes__hint">Test Hint</div>'
                "</div>"
            ),
        ),
        (
            {
                "name": "test",
                "value": "banana",
                "label": "Test Label",
                "exclusive": True,
            },
            (
                '<div class="govuk-checkboxes__item">'
                    '<input id="test-banana" name="test" type="checkbox" value="banana" data-behaviour="exclusive" class="govuk-checkboxes__input">'
                    '<label for="test-banana" class="govuk-label govuk-checkboxes__label">Test Label</label>'
                "</div>"
            ),
        ),
    ),
)
def test_checkbox(kwargs, expected, html):
    """Test Checkbox with various parameters.
    Args:
        kwargs (dict): The arguments to pass to Checkbox.
        expected (str): The expected HTML output.
    """
    cb = ds.Checkbox(**kwargs)
    assert html(cb) == html(expected)


@pytest.mark.parametrize(
    "kwargs, expected",
    (
        (
            {
                "name": "test",
                "label": "Test Label",
                "checkboxes": [ds.Checkbox("test", "label_1", "Label 1")],
            },
            (
                '<div class="govuk-form-group">'
                    '<label for="test" class="govuk-label">Test Label</label>'
                    '<fieldset aria-describedby="test-hint" class="govuk-fieldset" id="test">'
                        '<div data-module="govuk-checkboxes" class="govuk-checkboxes">'
                            '<div class="govuk-checkboxes__item">'
                                '<input id="test-label_1" name="test" type="checkbox" value="label_1" class="govuk-checkboxes__input">'
                                '<label for="test-label_1" class="govuk-label govuk-checkboxes__label">Label 1</label>'
                            "</div>"
                        "</div>"
                    "</fieldset>"
                "</div>"
            ),
        ),
        (
            {
                "name": "test",
                "label": "Test Label",
                "choices": {"label_1": "Label 1"},
            },
            (
                '<div class="govuk-form-group">'
                    '<label for="test" class="govuk-label">Test Label</label>'
                    '<fieldset aria-describedby="test-hint" class="govuk-fieldset" id="test">'
                        '<div data-module="govuk-checkboxes" class="govuk-checkboxes">'
                            '<div class="govuk-checkboxes__item">'
                                '<input id="test-label_1" name="test" type="checkbox" value="label_1" class="govuk-checkboxes__input">'
                                '<label for="test-label_1" class="govuk-label govuk-checkboxes__label">Label 1</label>'
                            "</div>"
                        "</div>"
                    "</fieldset>"
                "</div>"
            ),
        ),
        (
            {
                "name": "test",
                "label": "Test Label",
                "checkboxes": [],
                "hint": "Test Hint",
            },
            (
                '<div class="govuk-form-group">'
                    '<label for="test" class="govuk-label">Test Label</label>'
                    '<div id="test-hint" class="govuk-hint">Test Hint</div>'
                    '<fieldset aria-describedby="test-hint" class="govuk-fieldset" id="test">'
                        '<div data-module="govuk-checkboxes" class="govuk-checkboxes">'
                        "</div>"
                    "</fieldset>"
                "</div>"
            ),
        ),
        (
            {"name": "test", "label": "Test Label", "checkboxes": [], "heading": "l"},
            (
                '<div class="govuk-form-group">'
                    '<h1 class="govuk-label-wrapper">'
                        '<label for="test" class="govuk-label govuk-label--l">Test Label</label>'
                    "</h1>"
                    '<fieldset aria-describedby="test-hint" class="govuk-fieldset" id="test">'
                        '<div data-module="govuk-checkboxes" class="govuk-checkboxes">'
                        "</div>"
                    "</fieldset>"
                "</div>"
            ),
        ),
        (
            {
                "name": "test",
                "label": "Test Label",
                "checkboxes": [],
                "error": "Test Error!",
            },
            (
                '<div class="govuk-form-group govuk-form-group--error">'
                    '<label for="test" class="govuk-label">Test Label</label>'
                    '<p id="test-error" class="govuk-error-message">'
                        '<span class="govuk-visually-hidden">Error: </span>'
                        "Test Error!"
                    "</p>"
                    '<fieldset aria-describedby="test-hint" class="govuk-fieldset" id="test">'
                        '<div data-module="govuk-checkboxes" class="govuk-checkboxes">'
                        "</div>"
                    "</fieldset>"
                "</div>"
            ),
        ),
        (
            {"name": "test", "label": "Test Label", "checkboxes": [], "small": True},
            (
                '<div class="govuk-form-group">'
                    '<label for="test" class="govuk-label">Test Label</label>'
                    '<fieldset aria-describedby="test-hint" class="govuk-fieldset" id="test">'
                        '<div data-module="govuk-checkboxes" class="govuk-checkboxes govuk-checkboxes--small">'
                        "</div>"
                    "</fieldset>"
                "</div>"
            ),
        ),
    ),
)
def test_checkboxes(kwargs, expected, html):
    """Test Checkboxes with various parameters.
    Args:
        kwargs (dict): The kwargs to pass to Checkboxes.
        expected (str): The expected HTML output.
    """
    cbs = ds.Checkboxes(**kwargs)
    assert html(cbs) == html(expected)


def test_checkboxes_value(html):
    """Test Checkboxes with value."""
    checks = ds.Checkboxes(
        name="test",
        checkboxes=[ds.Checkbox("test", "yes", "Yes"), ds.Checkbox("test", "no", "No")],
    )
    checks.value = "yes"
    assert html(checks) == html(
        '<div class="govuk-form-group">'
            '<fieldset aria-describedby="test-hint" class="govuk-fieldset" id="test">'
                '<div data-module="govuk-checkboxes" class="govuk-checkboxes">'
                    '<div class="govuk-checkboxes__item">'
                        '<input id="test-yes" name="test" type="checkbox" value="yes" checked class="govuk-checkboxes__input">'
                        '<label for="test-yes" class="govuk-label govuk-checkboxes__label">Yes</label>'
                    "</div>"
                    '<div class="govuk-checkboxes__item">'
                        '<input id="test-no" name="test" type="checkbox" value="no" class="govuk-checkboxes__input">'
                        '<label for="test-no" class="govuk-label govuk-checkboxes__label">No</label>'
                    "</div>"
                "</div>"
            "</fieldset>"
        "</div>"
    )


@pytest.mark.parametrize(
    "kwargs, expected",
    (
        (
            {"name": "test", "value": "banana", "label": "Test Label"},
            (
                '<div class="govuk-radios__item">'
                    '<input id="test-banana" name="test" type="radio" value="banana" class="govuk-radios__input">'
                    '<label for="test-banana" class="govuk-label govuk-radios__label">Test Label</label>'
                "</div>"
            ),
        ),
        (
            {"name": "test", "value": "banana", "label": "Test Label", "checked": True},
            (
                '<div class="govuk-radios__item">'
                    '<input id="test-banana" name="test" type="radio" value="banana" checked class="govuk-radios__input">'
                    '<label for="test-banana" class="govuk-label govuk-radios__label">Test Label</label>'
                "</div>"
            ),
        ),
        (
            {
                "name": "test",
                "value": "banana",
                "label": "Test Label",
                "hint": "Test Hint",
            },
            (
                '<div class="govuk-radios__item">'
                    '<input id="test-banana" name="test" type="radio" value="banana" class="govuk-radios__input">'
                    '<label for="test-banana" class="govuk-label govuk-radios__label">Test Label</label>'
                    '<div id="test-banana-hint" class="govuk-hint govuk-radios__hint">Test Hint</div>'
                "</div>"
            ),
        ),
    ),
)
def test_radio(kwargs, expected, html):
    """Test Radio with various parameters.
    Args:
        kwargs (dict): The arguments to pass to Radio.
        expected (str): The expected HTML output.
    """
    radio = ds.Radio(**kwargs)
    assert html(radio) == html(expected)


@pytest.mark.parametrize(
    "kwargs, expected",
    (
        (
            {
                "name": "test",
                "label": "Test Label",
                "radios": [ds.Radio("test", "label_1", "Label 1")],
            },
            (
                '<div class="govuk-form-group">'
                    '<label for="test" class="govuk-label">Test Label</label>'
                    '<fieldset aria-describedby="test-hint" class="govuk-fieldset" id="test">'
                        '<div data-module="govuk-radios" class="govuk-radios">'
                            '<div class="govuk-radios__item">'
                                '<input id="test-label_1" name="test" type="radio" value="label_1" class="govuk-radios__input">'
                                '<label for="test-label_1" class="govuk-label govuk-radios__label">Label 1</label>'
                            "</div>"
                        "</div>"
                    "</fieldset>"
                "</div>"
            ),
        ),
        (
            {
                "name": "test",
                "label": "Test Label",
                "choices": {"label_1": "Label 1"},
            },
            (
                '<div class="govuk-form-group">'
                    '<label for="test" class="govuk-label">Test Label</label>'
                    '<fieldset aria-describedby="test-hint" class="govuk-fieldset" id="test">'
                        '<div data-module="govuk-radios" class="govuk-radios">'
                            '<div class="govuk-radios__item">'
                                '<input id="test-label_1" name="test" type="radio" value="label_1" class="govuk-radios__input">'
                                '<label for="test-label_1" class="govuk-label govuk-radios__label">Label 1</label>'
                            "</div>"
                        "</div>"
                    "</fieldset>"
                "</div>"
            ),
        ),
        (
            {"name": "test", "label": "Test Label", "radios": [], "hint": "Test Hint"},
            (
                '<div class="govuk-form-group">'
                    '<label for="test" class="govuk-label">Test Label</label>'
                    '<div id="test-hint" class="govuk-hint">Test Hint</div>'
                    '<fieldset aria-describedby="test-hint" class="govuk-fieldset" id="test">'
                        '<div data-module="govuk-radios" class="govuk-radios">'
                        "</div>"
                    "</fieldset>"
                "</div>"
            ),
        ),
        (
            {"name": "test", "label": "Test Label", "radios": [], "heading": "l"},
            (
                '<div class="govuk-form-group">'
                    '<h1 class="govuk-label-wrapper">'
                        '<label for="test" class="govuk-label govuk-label--l">Test Label</label>'
                    "</h1>"
                    '<fieldset aria-describedby="test-hint" class="govuk-fieldset" id="test">'
                        '<div data-module="govuk-radios" class="govuk-radios">'
                    "</div>"
                    "</fieldset>"
                "</div>"
            ),
        ),
        (
            {
                "name": "test",
                "label": "Test Label",
                "radios": [],
                "error": "Test Error!",
            },
            (
                '<div class="govuk-form-group govuk-form-group--error">'
                    '<label for="test" class="govuk-label">Test Label</label>'
                    '<p id="test-error" class="govuk-error-message">'
                        '<span class="govuk-visually-hidden">Error: </span>'
                        "Test Error!"
                    "</p>"
                    '<fieldset aria-describedby="test-hint" class="govuk-fieldset" id="test">'
                        '<div data-module="govuk-radios" class="govuk-radios">'
                        "</div>"
                    "</fieldset>"
                "</div>"
            ),
        ),
        (
            {"name": "test", "label": "Test Label", "radios": [], "small": True},
            (
                '<div class="govuk-form-group">'
                    '<label for="test" class="govuk-label">Test Label</label>'
                    '<fieldset aria-describedby="test-hint" class="govuk-fieldset" id="test">'
                        '<div data-module="govuk-radios" class="govuk-radios govuk-radios--small">'
                        "</div>"
                    "</fieldset>"
                "</div>"
            ),
        ),
        (
            {"name": "test", "label": "Test Label", "radios": [], "inline": True},
            (
                '<div class="govuk-form-group">'
                    '<label for="test" class="govuk-label">Test Label</label>'
                    '<fieldset aria-describedby="test-hint" class="govuk-fieldset" id="test">'
                        '<div data-module="govuk-radios" class="govuk-radios govuk-radios--inline">'
                        "</div>"
                    "</fieldset>"
                "</div>"
            ),
        ),
    ),
)
def test_radios(kwargs, expected, html):
    """Test Radios with various parameters.
    Args:
        name (str): name to pass to Radios.
        label (str): label to pass to Radios.
        radios (list): list of Radio items to pass in here.
        kwargs (dict): The kwargs to pass to Radios.
        expected (str): The expected HTML output.
    """
    radios = ds.Radios(**kwargs)
    assert html(radios) == html(expected)


def test_radios_value(html):
    """Test Radios with value."""
    radios = ds.Radios(
        name="test",
        radios=[ds.Radio("test", "yes", "Yes"), ds.Radio("test", "no", "No")],
    )
    radios.value = "yes"
    assert html(radios) == html(
        '<div class="govuk-form-group">'
            '<fieldset aria-describedby="test-hint" class="govuk-fieldset" id="test">'
                '<div data-module="govuk-radios" class="govuk-radios">'
                    '<div class="govuk-radios__item">'
                        '<input id="test-yes" name="test" type="radio" value="yes" checked class="govuk-radios__input">'
                        '<label for="test-yes" class="govuk-label govuk-radios__label">Yes</label>'
                    "</div>"
                    '<div class="govuk-radios__item">'
                        '<input id="test-no" name="test" type="radio" value="no" class="govuk-radios__input">'
                        '<label for="test-no" class="govuk-label govuk-radios__label">No</label>'
                    "</div>"
                "</div>"
            "</fieldset>"
        "</div>"
    )


@pytest.mark.parametrize(
    "kwargs, expected",
    (
        (
            {"name": "test", "label": "Test Label"},
            (
                '<div class="govuk-form-group">'
                    '<label for="test" class="govuk-label">Test Label</label>'
                        '<div data-module="govuk-file-upload" class="govuk-drop-zone">'
                        '<input name="test" type="file" aria-describedby="test-hint test-error" id="test" class="govuk-file-upload">'
                    "</div>"
                "</div>"
            ),
        ),
        (
            {"name": "test", "label": "Test Label", "hint": "Test hint"},
            (
                '<div class="govuk-form-group">'
                    '<label for="test" class="govuk-label">Test Label</label>'
                    '<div id="test-hint" class="govuk-hint">Test hint</div>'
                        '<div data-module="govuk-file-upload" class="govuk-drop-zone">'
                        '<input name="test" type="file" aria-describedby="test-hint test-error" id="test" class="govuk-file-upload">'
                    "</div>"
                "</div>"
            ),
        ),
        (
            {"name": "test", "label": "Test Label", "error": "Test error"},
            (
                '<div class="govuk-form-group govuk-form-group--error">'
                    '<label for="test" class="govuk-label">Test Label</label>'
                        '<p id="test-error" class="govuk-error-message">'
                            '<span class="govuk-visually-hidden">Error: </span>'
                            "Test error"
                        "</p>"
                    '<div data-module="govuk-file-upload" class="govuk-drop-zone">'
                        '<input name="test" type="file" aria-describedby="test-hint test-error" id="test" class="govuk-file-upload govuk-file-upload--error">'
                    "</div>"
                "</div>"
            ),
        ),
        (
            {"name": "test", "label": "Test Label", "heading": "l"},
            (
                '<div class="govuk-form-group">'
                    '<h1 class="govuk-label-wrapper">'
                        '<label for="test" class="govuk-label govuk-label--l">Test Label</label>'
                    "</h1>"
                    '<div data-module="govuk-file-upload" class="govuk-drop-zone">'
                        '<input name="test" type="file" aria-describedby="test-hint test-error" id="test" class="govuk-file-upload">'
                    "</div>"
                "</div>"
            ),
        ),
    ),
)
def test_fileupload(kwargs, expected, html):
    """Test FileUpload with various parameters.
    Args:
        kwargs (dict): The arguments to pass to FileUpload.
        expected (str): The expected HTML output.
    """
    fu = ds.FileUpload(**kwargs)
    assert html(fu) == html(expected)


@pytest.mark.parametrize(
    "kwargs, expected",
    (
        (
            {"name": "test", "label": "Test Label"},
            (
                '<div class="govuk-form-group">'
                    '<label for="test" class="govuk-label">Test Label</label>'
                    '<fieldset role="group" aria-describedby="test-hint" class="govuk-fieldset">'
                        '<div id="test" class="govuk-date-input">'
                            '<div class="govuk-date-input__item">'
                                '<div id="test-day" class="govuk-form-group">'
                                    '<label for="test-day-input" class="govuk-label govuk-date-input__label">Day</label>'
                                    '<input name="test" id="test-day-input" type="text" inputmode="numeric" class="govuk-input govuk-date-input__input govuk-input--width-2">'
                                "</div>"
                            "</div>"
                            '<div class="govuk-date-input__item">'
                                '<div id="test-month" class="govuk-form-group">'
                                    '<label for="test-month-input" class="govuk-label govuk-date-input__label">Month</label>'
                                    '<input name="test" id="test-month-input" type="text" inputmode="numeric" class="govuk-input govuk-date-input__input govuk-input--width-2">'
                                "</div>"
                            "</div>"
                            '<div class="govuk-date-input__item">'
                                '<div id="test-year" class="govuk-form-group">'
                                    '<label for="test-year-input" class="govuk-label govuk-date-input__label">Year</label>'
                                    '<input name="test" id="test-year-input" type="text" inputmode="numeric" class="govuk-input govuk-date-input__input govuk-input--width-4">'
                                "</div>"
                            "</div>"
                        "</div>"
                    "</fieldset>"
                "</div>"
            ),
        ),
        (
            {"name": "test", "label": "Test Label", "heading": "l"},
            (
                '<div class="govuk-form-group">'
                    '<h1 class="govuk-label-wrapper"><label for="test" class="govuk-label govuk-label--l">Test Label</label></h1>'
                    '<fieldset role="group" aria-describedby="test-hint" class="govuk-fieldset">'
                        '<div id="test" class="govuk-date-input">'
                            '<div class="govuk-date-input__item">'
                                '<div id="test-day" class="govuk-form-group">'
                                    '<label for="test-day-input" class="govuk-label govuk-date-input__label">Day</label>'
                                    '<input name="test" id="test-day-input" type="text" inputmode="numeric" class="govuk-input govuk-date-input__input govuk-input--width-2">'
                                "</div>"
                            "</div>"
                            '<div class="govuk-date-input__item">'
                                '<div id="test-month" class="govuk-form-group">'
                                    '<label for="test-month-input" class="govuk-label govuk-date-input__label">Month</label>'
                                    '<input name="test" id="test-month-input" type="text" inputmode="numeric" class="govuk-input govuk-date-input__input govuk-input--width-2">'
                                "</div>"
                            "</div>"
                            '<div class="govuk-date-input__item">'
                                '<div id="test-year" class="govuk-form-group">'
                                    '<label for="test-year-input" class="govuk-label govuk-date-input__label">Year</label>'
                                    '<input name="test" id="test-year-input" type="text" inputmode="numeric" class="govuk-input govuk-date-input__input govuk-input--width-4">'
                                "</div>"
                            "</div>"
                        "</div>"
                    "</fieldset>"
                "</div>"
            ),
        ),
        (
            {"name": "test", "label": "Test Label", "hint": "Test Hint"},
            (
                '<div class="govuk-form-group">'
                    '<label for="test" class="govuk-label">Test Label</label>'
                    '<div id="test-hint" class="govuk-hint">Test Hint</div>'
                    '<fieldset role="group" aria-describedby="test-hint" class="govuk-fieldset">'
                        '<div id="test" class="govuk-date-input">'
                            '<div class="govuk-date-input__item">'
                                '<div id="test-day" class="govuk-form-group">'
                                    '<label for="test-day-input" class="govuk-label govuk-date-input__label">Day</label>'
                                    '<input name="test" id="test-day-input" type="text" inputmode="numeric" class="govuk-input govuk-date-input__input govuk-input--width-2">'
                                "</div>"
                            "</div>"
                            '<div class="govuk-date-input__item">'
                                '<div id="test-month" class="govuk-form-group">'
                                    '<label for="test-month-input" class="govuk-label govuk-date-input__label">Month</label>'
                                    '<input name="test" id="test-month-input" type="text" inputmode="numeric" class="govuk-input govuk-date-input__input govuk-input--width-2">'
                                "</div>"
                            "</div>"
                            '<div class="govuk-date-input__item">'
                                '<div id="test-year" class="govuk-form-group">'
                                    '<label for="test-year-input" class="govuk-label govuk-date-input__label">Year</label>'
                                    '<input name="test" id="test-year-input" type="text" inputmode="numeric" class="govuk-input govuk-date-input__input govuk-input--width-4">'
                                "</div>"
                            "</div>"
                        "</div>"
                    "</fieldset>"
                "</div>"
            ),
        ),
        (
            {"name": "test", "label": "Test Label", "error": "Test Error"},
            (
                '<div class="govuk-form-group govuk-form-group--error">'
                    '<label for="test" class="govuk-label">Test Label</label>'
                    '<p id="test-error" class="govuk-error-message"><span class="govuk-visually-hidden">Error: </span>Test Error</p>'
                    '<fieldset role="group" aria-describedby="test-hint" class="govuk-fieldset">'
                        '<div id="test" class="govuk-date-input">'
                            '<div class="govuk-date-input__item">'
                                '<div id="test-day" class="govuk-form-group">'
                                    '<label for="test-day-input" class="govuk-label govuk-date-input__label">Day</label>'
                                    '<input name="test" id="test-day-input" type="text" inputmode="numeric" class="govuk-input govuk-date-input__input govuk-input--width-2 govuk-input--error">'
                                "</div>"
                            "</div>"
                            '<div class="govuk-date-input__item">'
                                '<div id="test-month" class="govuk-form-group">'
                                    '<label for="test-month-input" class="govuk-label govuk-date-input__label">Month</label>'
                                    '<input name="test" id="test-month-input" type="text" inputmode="numeric" class="govuk-input govuk-date-input__input govuk-input--width-2 govuk-input--error">'
                                "</div>"
                            "</div>"
                            '<div class="govuk-date-input__item">'
                                '<div id="test-year" class="govuk-form-group">'
                                    '<label for="test-year-input" class="govuk-label govuk-date-input__label">Year</label>'
                                    '<input name="test" id="test-year-input" type="text" inputmode="numeric" class="govuk-input govuk-date-input__input govuk-input--width-4 govuk-input--error">'
                                "</div>"
                            "</div>"
                        "</div>"
                    "</fieldset>"
                "</div>"
            ),
        ),
    ),
)
def test_date_input(kwargs, expected, html):
    """Test DateInput with various parameters.
    Args:
        kwargs (dict): The arguments to pass to DateInput.
        expected (str): The expected HTML output.
    """
    dateinput = ds.DateInput(**kwargs)
    assert html(dateinput) == html(expected)


@pytest.mark.parametrize(
    "kwargs, expected",
    (
        (
            {},
            (
                "<div>"
                    '<div role="region" aria-label="Cookies on Test Service" data-nosnippet id="cookie-banner" class="govuk-cookie-banner">'
                        '<div class="govuk-cookie-banner__message govuk-width-container">'
                            '<div class="govuk-grid-row">'
                                '<div class="govuk-grid-column-two-thirds">'
                                    '<h2 class="govuk-heading-m">Cookies for Test Service</h2>'
                                    '<div class="govuk-cookie-banner__content"></div>'
                                "</div>"
                            "</div>"
                            '<form enctype="multipart/form-data" hx-post="/cookie-banner" hx-target="#cookie-banner" hx-swap="outerHTML">'
                                '<div class="govuk-button-group">'
                                    '<button type="submit" data-module="govuk-button" value="yes" name="cookies[additional]" class="govuk-button">Accept additional cookies</button>'
                                    '<button type="submit" data-module="govuk-button" value="no" name="cookies[additional]" class="govuk-button">Reject additional cookies</button>'
                                    '<a href="/cookies" class="govuk-link">View cookies</a>'
                                "</div>"
                            "</form>"
                        "</div>"
                    "</div>"
                "</div>"
            ),
        ),
        (
            {"confirmation": True},
            (
                "<div>"
                    '<div role="region" aria-label="Cookies on Test Service" data-nosnippet id="cookie-banner" class="govuk-cookie-banner">'
                        '<div class="govuk-cookie-banner__message govuk-width-container">'
                            '<div class="govuk-grid-row">'
                                '<div class="govuk-grid-column-two-thirds">'
                                    '<h2 class="govuk-heading-m">Cookies for Test Service</h2>'
                                    '<div class="govuk-cookie-banner__content"></div>'
                                "</div>"
                            "</div>"
                            '<form enctype="multipart/form-data" hx-post="/cookie-banner" hx-target="#cookie-banner" hx-swap="outerHTML">'
                                '<div class="govuk-button-group">'
                                    '<button type="submit" data-module="govuk-button" value="hide" name="cookies[additional]" class="govuk-button">Hide cookie message</button>'
                                "</div>"
                            "</form>"
                        "</div>"
                    "</div>"
                "</div>"
            ),
        ),
    ),
)
def test_cookie_banner(kwargs, expected, html):
    """Test CookieBanner with various parameters.
    Args:
        kwargs (dict): The arguments to pass to CookieBanner.
        expected (str): The expected HTML output.
    """
    banner = ds.Div(ds.CookieBanner("Test Service", **kwargs))
    assert html(banner) == html(expected)


@pytest.mark.parametrize("field", (
    ds.Select,
    ds.Textarea,
    ds.PasswordInput,
    ds.CharacterCount,
    ds.TextInput,
    ds.Checkboxes,
    ds.Radios,
    ds.FileUpload,
    ds.DateInput,
    ds.EmailInput,
    ds.NumberInput,
    ds.DecimalInput,
))
def test_required(field):
    """Test that all input fields can be marked as required."""
    f = field(name="test", label="Test Label", required=True)
    form = forms.Form("test", f, data={})
    assert not form.valid
    assert form.errors == {"test": "This field is required."}


@pytest.mark.parametrize("field", (
    ds.Select,
    ds.Textarea,
    ds.PasswordInput,
    ds.CharacterCount,
    ds.TextInput,
    ds.Checkboxes,
    ds.Radios,
    ds.FileUpload,
    ds.DateInput,
    ds.EmailInput,
    ds.NumberInput,
    ds.DecimalInput,
    ds.GBPInput,
    ds.RegexInput,
    ds.PastDateInput,
    ds.FutureDateInput,
))
def test_not_required(field):
    """Test that all input fields can be marked as not required."""
    f = field(name="test", label="Test Label", required=False)
    form = forms.Form("test", f, data={})
    # TODO: assert exact errors :/
    assert form.errors == {}


def test_radio_reveal(html):
    """Test Radios with reveal field."""
    radios = ds.Radios(
        name="test",
        radios=[
            ds.Radio("test", "yes", "Yes", reveal=ds.TextInput("test1", "Test 1")),
            ds.Radio("test", "no", "No", reveal=ds.TextInput("test1", "Test 1"))
        ],
    )
    assert html(radios) == html(
        '<div class="govuk-form-group">'
            '<fieldset aria-describedby="test-hint" class="govuk-fieldset" id="test">'
                '<div data-module="govuk-radios" class="govuk-radios">'
                    "<div>"
                        '<div class="govuk-radios__item">'
                            '<input id="test-yes" name="test" type="radio" value="yes" class="govuk-radios__input" data-aria-controls="conditional-test-yes">'
                            '<label for="test-yes" class="govuk-label govuk-radios__label">Yes</label>'
                        "</div>"
                        '<div class="govuk-radios__conditional govuk-radios__conditional--hidden" id="conditional-test-yes">'
                            '<div class="govuk-form-group">'
                                '<label class="govuk-label" for="test1">Test 1</label>'
                                '<input aria-describedby="test1-hint test1-error" class="govuk-input" id="test1" name="test1" type="text"/>'
                            "</div>"
                        "</div>"
                    "</div>"
                    "<div>"
                        '<div class="govuk-radios__item">'
                            '<input id="test-no" name="test" type="radio" value="no" class="govuk-radios__input" data-aria-controls="conditional-test-no">'
                            '<label for="test-no" class="govuk-label govuk-radios__label">No</label>'
                        "</div>"
                        '<div class="govuk-radios__conditional govuk-radios__conditional--hidden" id="conditional-test-no">'
                            '<div class="govuk-form-group">'
                                '<label class="govuk-label" for="test1">Test 1</label>'
                                '<input aria-describedby="test1-hint test1-error" class="govuk-input" id="test1" name="test1" type="text"/>'
                            "</div>"
                        "</div>"
                    "</div>"
                "</div>"
            "</fieldset>"
        "</div>"
    )


@pytest.mark.parametrize("field", (
    ds.Select,
    ds.Textarea,
    ds.PasswordInput,
    ds.CharacterCount,
    ds.TextInput,
    ds.Checkboxes,
    ds.Radios,
    ds.FileUpload,
    ds.DateInput,
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
        (ds.Textarea, "test", "test"),
        (ds.Textarea, "", None),
        (ds.PasswordInput, "test", "test"),
        (ds.PasswordInput, "", None),
        (ds.CharacterCount, "test", "test"),
        (ds.CharacterCount, "", None),
        (ds.TextInput, "test", "test"),
        (ds.TextInput, "", None),
        (ds.DateInput, ["10", "10", "1990"], "1990-10-10"),
        (ds.DateInput, ["", "", ""], None),
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


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "field, value, clean",
    (
        (ds.Select, "test1", "Test 1"),
        (ds.Checkboxes, "test1", "Test 1"),
        (ds.Radios, "test1", "Test 1"),
    )
)
async def test_clean_choice(field, value, clean):
    """
    Test that assigns a value to the field and checks if the
    clean aatribute returns the right data and type.
    """
    f = field(name="test", label="Test Label", choices={"test1": "Test 1", "test2": "Test 2"})
    f.value = value
    data = await f.clean
    assert data == clean


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "field, value",
    (
        (ds.DateInput, ["10", "10", "not-a-number"]),
    ),
)
async def test_clean_with_invalid_values(field, value):
    with pytest.raises(ValueError):
        f = field(name="test", label="Test Label", choices={"test1": "Test 1", "test2": "Test 2"})
        f.value = value
        await f.clean
