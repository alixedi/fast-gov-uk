import fasthtml.common as fh
import pytest

import fast_gov_uk.design_system as ds


@pytest.mark.parametrize(
    "kwargs, expected",
    (
        (
            {"text": "Test"},
            '<div class="govuk-inset-text">Test</div>',
        ),
    ),
)
def test_inset(kwargs, expected):
    """Test Inset text with various parameters.
    Args:
        kwargs (dict): The arguments to pass to Inset.
        expected (str): The expected HTML output.
    """
    text = ds.Inset(**kwargs)
    assert str(text) == expected


@pytest.mark.parametrize(
    "content, expected",
    (
        (
            ["Test Content"],
            (
                '<details class="govuk-details">'
                    '<summary class="govuk-details__summary">Test</summary>'
                    'Test Content'
                '</details>'
            ),
        ),
        (
            [ds.A("Test Link")],
            (
                '<details class="govuk-details">'
                    '<summary class="govuk-details__summary">Test</summary>'
                    '<a href="#" class="govuk-link">Test Link</a>'
                '</details>'
            ),
        ),
        (
            [ds.A("Test Link"), ds.P("Test para")],
            (
                '<details class="govuk-details">'
                    '<summary class="govuk-details__summary">Test</summary>'
                    '<a href="#" class="govuk-link">Test Link</a>'
                    '<p class="govuk-body">Test para</p>'
                '</details>'
            ),
        ),
    ),
)
def test_detail(content, expected):
    """Test Detail with various parameters.
    Args:
        args (dict): The arguments to pass to Detail.
        expected (str): The expected HTML output.
    """
    detail = ds.Detail("Test", *content)
    assert str(detail) == expected


@pytest.mark.parametrize(
    "kwargs, expected",
    (
        (
            {"content": [ds.P("Test Content")]},
            (
                '<div class="govuk-panel govuk-panel--confirmation">'
                    '<div class="govuk-panel__body">'
                        '<p class="govuk-body">Test Content</p>'
                    '</div>'
                '</div>'
            ),
        ),
        (
            {"title": "Test", "content": [ds.P("Test Content")]},
            (
                '<div class="govuk-panel govuk-panel--confirmation">'
                    '<h1 class="govuk-panel__title">Test</h1>'
                    '<div class="govuk-panel__body">'
                        '<p class="govuk-body">Test Content</p>'
                    '</div>'
                '</div>'
            ),
        ),
        (
            {"content": [ds.A("Test Link")]},
            (
                '<div class="govuk-panel govuk-panel--confirmation">'
                    '<div class="govuk-panel__body">'
                        '<a href="#" class="govuk-link">Test Link</a>'
                    '</div>'
                '</div>'
            ),
        ),
        (
            {"content": [ds.A("Test Link"), ds.P("Test Content")]},
            (
                '<div class="govuk-panel govuk-panel--confirmation">'
                    '<div class="govuk-panel__body">'
                        '<a href="#" class="govuk-link">Test Link</a>'
                        '<p class="govuk-body">Test Content</p>'
                    '</div>'
                '</div>'
            ),
        ),
    ),
)
def test_panel(kwargs, expected):
    """Test Panel with various parameters.
    Args:
        kwargs (dict): The arguments to pass to Panel.
        expected (str): The expected HTML output.
    """
    content = kwargs.pop("content")
    panel = ds.Panel(*content, **kwargs)
    assert str(panel) == expected


@pytest.mark.parametrize(
    "kwargs, expected",
    (
        (
            {"text": "Test"},
            '<strong class="govuk-tag">Test</strong>',
        ),
        (
            {"text": "Test", "color": "blue"},
            '<strong class="govuk-tag govuk-tag--blue">Test</strong>',
        ),
        (
            {"text": "Test", "color": "grey"},
            '<strong class="govuk-tag govuk-tag--grey">Test</strong>',
        ),
        (
            {"text": "Test", "color": "red"},
            '<strong class="govuk-tag govuk-tag--red">Test</strong>',
        ),
        (
            {"text": "Test", "color": "green"},
            '<strong class="govuk-tag govuk-tag--green">Test</strong>',
        ),
        (
            {"text": "Test", "color": "yellow"},
            '<strong class="govuk-tag govuk-tag--yellow">Test</strong>',
        ),
    ),
)
def test_tag(kwargs, expected):
    """Test Panel with various parameters.
    Args:
        kwargs (dict): The arguments to pass to Tag.
        expected (str): The expected HTML output.
    """
    tag = ds.Tag(**kwargs)
    assert str(tag) == expected


@pytest.mark.parametrize(
    "kwargs, expected",
    (
        (
            {"content": [ds.P("You can be fined up to £5,000 if you do not register.")]},
            (
                '<div class="govuk-warning-text">'
                    '<span aria-hidden="true" class="govuk-warning-text__icon">!</span>'
                        '<strong class="govuk-warning-text__text">'
                            '<span class="govuk-visually-hidden">Warning</span>'
                            '<p class="govuk-body">You can be fined up to £5,000 if you do not register.</p>'
                        "</strong>"
                "</div>"
            ),
        ),
    ),
)
def test_warning(kwargs, expected):
    """Test Warning with various parameters.
    Args:
        kwargs (dict): The arguments to pass to Warning.
        expected (str): The expected HTML output.
    """
    content = kwargs.pop("content")
    banner = ds.Warning(*content, **kwargs)
    assert str(banner) == expected


@pytest.mark.parametrize(
    "kwargs, expected",
    (
        (
            {"title": "Important", "content": "Test Content"},
            (
                '<div role="region" aria-labelledby="govuk-notification-banner-title" data-module="govuk-notification-banner" class="govuk-notification-banner">'
                    '<div class="govuk-notification-banner__header">'
                        '<h2 id="govuk-notification-banner-title" class="govuk-notification-banner__title">Important</h2>'
                    "</div>"
                    '<div class="govuk-notification-banner__content">'
                        "Test Content"
                    "</div>"
                "</div>"
            ),
        ),
        (
            {"title": "Success", "content": "Test Content", "success": True},
            (
                '<div role="region" aria-labelledby="govuk-notification-banner-title" data-module="govuk-notification-banner" class="govuk-notification-banner govuk-notification-banner--success">'
                    '<div class="govuk-notification-banner__header">'
                        '<h2 id="govuk-notification-banner-title" class="govuk-notification-banner__title">Success</h2>'
                    "</div>"
                    '<div class="govuk-notification-banner__content">'
                        "Test Content"
                    "</div>"
                "</div>"
            ),
        ),
        (
            {"title": "Important", "content": ds.A("Test Link")},
            (
                '<div role="region" aria-labelledby="govuk-notification-banner-title" data-module="govuk-notification-banner" class="govuk-notification-banner">'
                    '<div class="govuk-notification-banner__header">'
                        '<h2 id="govuk-notification-banner-title" class="govuk-notification-banner__title">Important</h2>'
                    "</div>"
                    '<div class="govuk-notification-banner__content">'
                        '<a href="#" class="govuk-link">Test Link</a>'
                    "</div>"
                "</div>"
            ),
        ),
    ),
)
def test_notification(kwargs, expected):
    """Test Notification with various parameters.
    Args:
        kwargs (dict): The arguments to pass to Notification.
        expected (str): The expected HTML output.
    """
    notification = ds.Notification(**kwargs)
    assert str(notification) == expected


@pytest.mark.parametrize(
    "sections, expected",
    (
        (
            [{"heading": "Test 1", "content": "Test Content"}],
            (
                '<div data-module="govuk-accordion" class="govuk-accordion">'
                    '<div class="govuk-accordion__section">'
                        '<div class="govuk-accordion__section-header">'
                            '<h2 class="govuk-accordion__section-heading">'
                                '<span id="accordion-section-heading-1" class="govuk-accordion__section-button">'
                                    "Test 1"
                                "</span>"
                            "</h2>"
                        "</div>"
                        '<div id="accordion-section-content-1" class="govuk-accordion__section-content">'
                            "Test Content"
                        "</div>"
                    "</div>"
                "</div>"
            ),
        ),
        (
            [
                {"heading": "Test 1", "content": "Test Content 1"},
                {"heading": "Test 2", "content": "Test Content 2"},
            ],
            (
                '<div data-module="govuk-accordion" class="govuk-accordion">'
                    '<div class="govuk-accordion__section">'
                        '<div class="govuk-accordion__section-header">'
                            '<h2 class="govuk-accordion__section-heading">'
                                '<span id="accordion-section-heading-1" class="govuk-accordion__section-button">'
                                    "Test 1"
                                "</span>"
                            "</h2>"
                        "</div>"
                        '<div id="accordion-section-content-1" class="govuk-accordion__section-content">'
                            "Test Content 1"
                        "</div>"
                    "</div>"
                    '<div class="govuk-accordion__section">'
                        '<div class="govuk-accordion__section-header">'
                            '<h2 class="govuk-accordion__section-heading">'
                                '<span id="accordion-section-heading-2" class="govuk-accordion__section-button">'
                                    "Test 2"
                                "</span>"
                            "</h2>"
                        "</div>"
                        '<div id="accordion-section-content-2" class="govuk-accordion__section-content">'
                            "Test Content 2"
                        "</div>"
                    "</div>"
                "</div>"
            ),
        ),
    ),
)
def test_accordian(sections, expected):
    """Test Accordian with various parameters.
    Args:
        sections (list): The sections to pass to Accordian.
        expected (str): The expected HTML output.
    """
    accordian = ds.Accordian(*sections)
    assert str(accordian) == expected


@pytest.mark.parametrize(
    "panels, expected",
    (
        (
            [
                {"heading": "Test 1", "content": "Test Content 1"},
                {"heading": "Test 2", "content": "Test Content 2"},
            ],
            (
                '<div data-module="govuk-tabs" class="govuk-tabs">'
                    '<ul class="govuk-tabs__list">'
                        '<li class="govuk-tabs__list-item govuk-tabs__list-item--selected">'
                            '<a href="#tab-panel-0" class="govuk-tabs__tab">Test 1</a>'
                        "</li>"
                        '<li class="govuk-tabs__list-item">'
                            '<a href="#tab-panel-1" class="govuk-tabs__tab">Test 2</a>'
                        "</li>"
                    "</ul>"
                    '<div id="tab-panel-0" class="govuk-tabs__panel">'
                        '<h2 class="govuk-heading-l">Test 1</h2>'
                        "Test Content 1"
                    "</div>"
                    '<div id="tab-panel-1" class="govuk-tabs__panel govuk-tabs__panel--hidden">'
                        '<h2 class="govuk-heading-l">Test 2</h2>'
                        "Test Content 2"
                    "</div>"
                "</div>"
            ),
        ),
    ),
)
def test_tabs(panels, expected):
    """Test Tab with various parameters.
    Args:
        panels (list): The panels to pass to Tab.
        expected (str): The expected HTML output.
    """
    tab = ds.Tab(*panels)
    assert str(tab) == expected


def test_errorsummary():
    """Test ErrorSummary with various parameters."""
    summary = ds.ErrorSummary(
        "Test Legend",
        fh.A("Test 1", href="/test1"),
        fh.A("Test 2", href="/test2"),
    )
    expected = (
        '<div data-module="govuk-error-summary" class="govuk-error-summary">'
            '<div role="alert">'
                '<h2 class="govuk-error-summary__title">Test Legend</h2>'
                '<div class="govuk-error-summary__body">'
                    "<ul>"
                        '<li><a href="/test1">Test 1</a></li>'
                        '<li><a href="/test2">Test 2</a></li>'
                    "</ul>"
                "</div>"
            "</div>"
        "</div>"
    )
    assert str(summary) == expected


def test_table():
    """
    Test Table with various parameters.
    """
    table = ds.Table(
        "Test",
        [
            {"Fruit": "Apple", "Price": "£0.25"},
            {"Fruit": "Orange", "Price": "£0.5"},
            {"Fruit": "Banana", "Price": "£0.1"},
        ],
        row_headers=["Fruit"],
    )
    expected = (
        '<table class="govuk-table">'
            '<caption class="govuk-table__caption govuk-table__caption--m">Test</caption>'
            '<thead class="govuk-table__head">'
                '<tr class="govuk-table__row">'
                    '<th scope="col" class="govuk-table__header">Fruit</th>'
                    '<th scope="col" class="govuk-table__header">Price</th>'
                "</tr>"
            "</thead>"
            '<tbody class="govuk-table__body">'
                '<tr class="govuk-table__row">'
                    '<th class="govuk-table__header">Apple</th>'
                    '<td class="govuk-table__cell">£0.25</td>'
                "</tr>"
                '<tr class="govuk-table__row">'
                    '<th class="govuk-table__header">Orange</th>'
                    '<td class="govuk-table__cell">£0.5</td>'
                "</tr>"
                '<tr class="govuk-table__row">'
                    '<th class="govuk-table__header">Banana</th>'
                    '<td class="govuk-table__cell">£0.1</td>'
                "</tr>"
            "</tbody>"
        "</table>"
    )
    assert str(table) == expected


@pytest.mark.parametrize(
    "kwargs, expected",
    (
        (
            {"label": "test", "href": "/test"},
            (
                '<li class="govuk-task-list__item govuk-task-list__item--with-link">'
                    '<div class="govuk-task-list__name-and-hint">'
                        '<a href="/test" aria-describedby="test-status" class="govuk-link govuk-task-list__link">test</a>'
                        '<div id="test-status" class="govuk-task-list__status">'
                            '<strong class="govuk-tag govuk-tag--blue">Incomplete</strong>'
                        "</div>"
                    "</div>"
                "</li>"
            ),
        ),
        (
            {"label": "test", "href": "/test", "completed": True},
            (
                '<li class="govuk-task-list__item govuk-task-list__item--with-link">'
                    '<div class="govuk-task-list__name-and-hint">'
                        '<a href="/test" aria-describedby="test-status" class="govuk-link govuk-task-list__link">test</a>'
                        '<div id="test-status" class="govuk-task-list__status">Completed</div>'
                    "</div>"
                "</li>"
            ),
        ),
        (
            {"label": "test", "href": "/test", "completed": True, "hint": "Test Hint"},
            (
                '<li class="govuk-task-list__item govuk-task-list__item--with-link">'
                    '<div class="govuk-task-list__name-and-hint">'
                        '<a href="/test" aria-describedby="test-status" class="govuk-link govuk-task-list__link">test</a>'
                        '<div id="test-hint" class="govuk-task-list__hint">Test Hint</div>'
                        '<div id="test-status" class="govuk-task-list__status">Completed</div>'
                    "</div>"
                "</li>"
            ),
        ),
    ),
)
def test_task(kwargs, expected):
    """Test Task with various parameters.
    Args:
        kwargs (dict): The arguments to pass to Task.
        expected (str): The expected HTML output.
    """
    task = ds.Task(**kwargs)
    assert str(task) == expected


@pytest.mark.parametrize(
    "args, expected",
    (
        (
            [ds.Task("Test Label 1", "/test1"), ds.Task("Test Label 2", "/test2")],
            (
                '<ul class="govuk-task-list">'
                    '<li class="govuk-task-list__item govuk-task-list__item--with-link">'
                        '<div class="govuk-task-list__name-and-hint">'
                            '<a href="/test1" aria-describedby="test-label-1-status" class="govuk-link govuk-task-list__link">Test Label 1</a>'
                            '<div id="test-label-1-status" class="govuk-task-list__status">'
                                '<strong class="govuk-tag govuk-tag--blue">Incomplete</strong>'
                            "</div>"
                        "</div>"
                    "</li>"
                    '<li class="govuk-task-list__item govuk-task-list__item--with-link">'
                        '<div class="govuk-task-list__name-and-hint">'
                            '<a href="/test2" aria-describedby="test-label-2-status" class="govuk-link govuk-task-list__link">Test Label 2</a>'
                            '<div id="test-label-2-status" class="govuk-task-list__status">'
                                '<strong class="govuk-tag govuk-tag--blue">Incomplete</strong>'
                            "</div>"
                        "</div>"
                    "</li>"
                "</ul>"
            ),
        ),
    ),
)
def test_tasklist(args, expected):
    """Test TaskList with various parameters.
    Args:
        args (list): The arguments to pass to TaskList.
        expected (str): The expected HTML output.
    """
    tl = ds.TaskList(*args)
    assert str(tl) == expected


@pytest.mark.parametrize(
    "args, expected",
    (
        (
            [
                ("Name", "John Doe", []),
                ("DOB", "", [ds.A("Test Label 1", "/test1")]),
                (
                    "Email",
                    "test@test.com",
                    [ds.A("Test Label 2", "/test2"), ds.A("Test Label 2", "/test2")],
                ),
            ],
            (
                '<div class="govuk-summary-list">'
                    '<div class="govuk-summary-list__row">'
                        '<dt class="govuk-summary-list__key">Name</dt>'
                        '<dd class="govuk-summary-list__value">John Doe</dd>'
                        '<dd class="govuk-summary-list__actions">'
                            '<ul class="govuk-summary-list__actions-list"></ul>'
                        "</dd>"
                    "</div>"
                    '<div class="govuk-summary-list__row">'
                        '<dt class="govuk-summary-list__key">DOB</dt>'
                        '<dd class="govuk-summary-list__value"></dd>'
                        '<dd class="govuk-summary-list__actions">'
                            '<ul class="govuk-summary-list__actions-list">'
                                '<li class="govuk-summary-list__actions-list-item">'
                                    '<a href="/test1" class="govuk-link">Test Label 1</a>'
                                "</li>"
                            "</ul>"
                        "</dd>"
                    "</div>"
                    '<div class="govuk-summary-list__row">'
                        '<dt class="govuk-summary-list__key">Email</dt>'
                        '<dd class="govuk-summary-list__value">test@test.com</dd>'
                        '<dd class="govuk-summary-list__actions">'
                            '<ul class="govuk-summary-list__actions-list">'
                                '<li class="govuk-summary-list__actions-list-item">'
                                    '<a href="/test2" class="govuk-link">Test Label 2</a>'
                                "</li>"
                                '<li class="govuk-summary-list__actions-list-item">'
                                    '<a href="/test2" class="govuk-link">Test Label 2</a>'
                                "</li>"
                            "</ul>"
                        "</dd>"
                    "</div>"
                "</div>"
            ),
        ),
    ),
)
def test_summary_list(args, expected):
    """Test SummaryList with various parameters.
    Args:
        args (list): The arguments to pass to SummaryList.
        expected (str): The expected HTML output.
    """
    summary = ds.SummaryList(args)
    assert str(summary) == expected


@pytest.mark.parametrize(
    "args, expected",
    (
        (
            [
                (
                    "Email",
                    "test@test.com",
                    [ds.A("Test Label 2", "/test2"), ds.A("Test Label 2", "/test2")],
                ),
            ],
            (
                '<div class="govuk-summary-card">'
                    '<div class="govuk-summary-card__title-wrapper">'
                        '<h2 class="govuk-summary-card__title">Test</h2>'
                        '<ul class="govuk-summary-card__actions">'
                            '<li class="govuk-summary-card__actio">'
                                '<a href="/test1" class="govuk-link">Test Action 1</a>'
                            "</li>"
                        "</ul>"
                    "</div>"
                    '<div class="govuk-summary-card__content">'
                        '<div class="govuk-summary-list">'
                            '<div class="govuk-summary-list__row">'
                                '<dt class="govuk-summary-list__key">Email</dt>'
                                '<dd class="govuk-summary-list__value">test@test.com</dd>'
                                '<dd class="govuk-summary-list__actions">'
                                    '<ul class="govuk-summary-list__actions-list">'
                                        '<li class="govuk-summary-list__actions-list-item">'
                                            '<a href="/test2" class="govuk-link">Test Label 2</a>'
                                        "</li>"
                                        '<li class="govuk-summary-list__actions-list-item">'
                                            '<a href="/test2" class="govuk-link">Test Label 2</a>'
                                        "</li>"
                                    "</ul>"
                                "</dd>"
                            "</div>"
                        "</div>"
                    "</div>"
                "</div>"
            ),
        ),
    ),
)
def test_summary_card(args, expected):
    """Test SummaryCard with various parameters.
    Args:
        args (list): The arguments to pass to SummaryCard.
        expected (str): The expected HTML output.
    """
    summary = ds.SummaryCard(
        title="Test",
        summary_list=ds.SummaryList(args),
        actions=[ds.A("Test Action 1", "/test1")],
    )
    assert str(summary) == expected
