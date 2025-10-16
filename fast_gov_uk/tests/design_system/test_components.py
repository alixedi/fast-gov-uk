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
def test_inset(kwargs, expected, html):
    """Test Inset text with various parameters.
    Args:
        kwargs (dict): The arguments to pass to Inset.
        expected (str): The expected HTML output.
    """
    text = ds.Inset(**kwargs)
    assert html(text) == html(expected)


@pytest.mark.parametrize(
    "content, expected",
    (
        (
            ["Test Content"],
            (
                '<details class="govuk-details">'
                    '<summary class="govuk-details__summary">'
                    '<span class="govuk-details__summary-text">Test</span>'
                    '</summary>'
                    '<div class="govuk-details__text">'
                        'Test Content'
                    '</div>'
                '</details>'
            ),
        ),
        (
            [ds.A("Test Link")],
            (
                '<details class="govuk-details">'
                    '<summary class="govuk-details__summary">'
                        '<span class="govuk-details__summary-text">Test</span>'
                    '</summary>'
                    '<div class="govuk-details__text">'
                        '<a href="#" class="govuk-link">Test Link</a>'
                    '</div>'
                '</details>'
            ),
        ),
        (
            [ds.A("Test Link"), ds.P("Test para")],
            (
                '<details class="govuk-details">'
                    '<summary class="govuk-details__summary">'
                        '<span class="govuk-details__summary-text">Test</span>'
                    '</summary>'
                    '<div class="govuk-details__text">'
                        '<a href="#" class="govuk-link">Test Link</a>'
                        '<p class="govuk-body">Test para</p>'
                    '</div>'
                '</details>'
            ),
        ),
    ),
)
def test_detail(content, expected, html):
    """Test Detail with various parameters.
    Args:
        args (dict): The arguments to pass to Detail.
        expected (str): The expected HTML output.
    """
    detail = ds.Detail("Test", *content)
    assert html(detail) == html(expected)


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
def test_panel(kwargs, expected, html):
    """Test Panel with various parameters.
    Args:
        kwargs (dict): The arguments to pass to Panel.
        expected (str): The expected HTML output.
    """
    content = kwargs.pop("content")
    panel = ds.Panel(*content, **kwargs)
    assert html(panel) == html(expected)


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
def test_tag(kwargs, expected, html):
    """Test Panel with various parameters.
    Args:
        kwargs (dict): The arguments to pass to Tag.
        expected (str): The expected HTML output.
    """
    tag = ds.Tag(**kwargs)
    assert html(tag) == html(expected)


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
def test_warning(kwargs, expected, html):
    """Test Warning with various parameters.
    Args:
        kwargs (dict): The arguments to pass to Warning.
        expected (str): The expected HTML output.
    """
    content = kwargs.pop("content")
    banner = ds.Warning(*content, **kwargs)
    assert html(banner) == html(expected)


@pytest.mark.parametrize(
    "kwargs, expected",
    (
        (
            {"title": "Important", "content": ["Test Content"]},
            (
                '<div role="alert" aria-labelledby="govuk-notification-banner-title" data-module="govuk-notification-banner" class="govuk-notification-banner">'
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
            {"title": "Success", "content": ["Test Content"], "success": True},
            (
                '<div role="alert" aria-labelledby="govuk-notification-banner-title" data-module="govuk-notification-banner" class="govuk-notification-banner govuk-notification-banner--success">'
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
            {"title": "Important", "content": [ds.A("Test Link")]},
            (
                '<div role="alert" aria-labelledby="govuk-notification-banner-title" data-module="govuk-notification-banner" class="govuk-notification-banner">'
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
def test_notification(kwargs, expected, html):
    """Test Notification with various parameters.
    Args:
        kwargs (dict): The arguments to pass to Notification.
        expected (str): The expected HTML output.
    """
    content = kwargs.pop("content")
    notification = ds.Notification(*content, **kwargs)
    assert html(notification) == html(expected)


@pytest.mark.parametrize(
    "sections, expected",
    (
        (
            [{"heading": "Test 1", "content": "Test Content"}],
            (
                "<div>"
                    '<div data-module="govuk-accordion" class="govuk-accordion">'
                        '<div class="govuk-accordion__section">'
                            '<div class="govuk-accordion__section-header">'
                                '<h2 class="govuk-accordion__section-heading">'
                                    '<span id="accordion-heading-1" class="govuk-accordion__section-button">'
                                        "Test 1"
                                    "</span>"
                                "</h2>"
                            "</div>"
                            '<div id="accordion-content-1" class="govuk-accordion__section-content">'
                                "Test Content"
                            "</div>"
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
                "<div>"
                    '<div data-module="govuk-accordion" class="govuk-accordion">'
                        '<div class="govuk-accordion__section">'
                            '<div class="govuk-accordion__section-header">'
                                '<h2 class="govuk-accordion__section-heading">'
                                    '<span id="accordion-heading-1" class="govuk-accordion__section-button">'
                                        "Test 1"
                                    "</span>"
                                "</h2>"
                            "</div>"
                            '<div id="accordion-content-1" class="govuk-accordion__section-content">'
                                "Test Content 1"
                            "</div>"
                        "</div>"
                        '<div class="govuk-accordion__section">'
                            '<div class="govuk-accordion__section-header">'
                                '<h2 class="govuk-accordion__section-heading">'
                                    '<span id="accordion-heading-2" class="govuk-accordion__section-button">'
                                        "Test 2"
                                    "</span>"
                                "</h2>"
                            "</div>"
                            '<div id="accordion-content-2" class="govuk-accordion__section-content">'
                                "Test Content 2"
                            "</div>"
                        "</div>"
                    "</div>"
                "</div>"
            ),
        ),
    ),
)
def test_accordion(sections, expected, html):
    """Test accordion with various parameters.
    Args:
        sections (list): The sections to pass to accordion.
        expected (str): The expected HTML output.
    """
    accordion = ds.Div(ds.Accordion(*sections))
    assert html(accordion) == html(expected)


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
                    '<h2 class="govuk-tabs__title"></h2>'
                    '<ul class="govuk-tabs__list">'
                        '<li class="govuk-tabs__list-item govuk-tabs__list-item--selected">'
                            '<a href="#test-1" class="govuk-tabs__tab">Test 1</a>'
                        "</li>"
                        '<li class="govuk-tabs__list-item">'
                            '<a href="#test-2" class="govuk-tabs__tab">Test 2</a>'
                        "</li>"
                    "</ul>"
                    '<div id="test-1" class="govuk-tabs__panel">'
                        '<h2 class="govuk-heading-l">Test 1</h2>'
                        "Test Content 1"
                    "</div>"
                    '<div id="test-2" class="govuk-tabs__panel govuk-tabs__panel--hidden">'
                        '<h2 class="govuk-heading-l">Test 2</h2>'
                        "Test Content 2"
                    "</div>"
                "</div>"
            ),
        ),
    ),
)
def test_tabs(panels, expected, html):
    """Test Tab with various parameters.
    Args:
        panels (list): The panels to pass to Tab.
        expected (str): The expected HTML output.
    """
    tab = ds.Tab(*panels)
    assert html(tab) == html(expected)


def test_errorsummary(html):
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
                    '<ul class="govuk-list govuk-error-summary__list">'
                        '<li><a href="/test1">Test 1</a></li>'
                        '<li><a href="/test2">Test 2</a></li>'
                    "</ul>"
                "</div>"
            "</div>"
        "</div>"
    )
    assert html(summary) == html(expected)


def test_table(html):
    """
    Test Table with various parameters.
    """
    table = ds.Table(
        [
            {"Fruit": "Apple", "Price": "£0.25"},
            {"Fruit": "Orange", "Price": "£0.5"},
            {"Fruit": "Banana", "Price": "£0.1"},
        ],
        caption="Test",
        header_cols=["Fruit"],
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
                    '<th class="govuk-table__header" scope="row">Apple</th>'
                    '<td class="govuk-table__cell">£0.25</td>'
                "</tr>"
                '<tr class="govuk-table__row">'
                    '<th class="govuk-table__header" scope="row">Orange</th>'
                    '<td class="govuk-table__cell">£0.5</td>'
                "</tr>"
                '<tr class="govuk-table__row">'
                    '<th class="govuk-table__header" scope="row">Banana</th>'
                    '<td class="govuk-table__cell">£0.1</td>'
                "</tr>"
            "</tbody>"
        "</table>"
    )
    assert html(table) == html(expected)


@pytest.mark.parametrize(
    "kwargs, expected",
    (
        (
            {"label": "test", "href": "/test"},
            (
                '<li class="govuk-task-list__item govuk-task-list__item--with-link">'
                    '<div class="govuk-task-list__name-and-hint">'
                        '<a href="/test" aria-describedby="test-status" class="govuk-link govuk-task-list__link">test</a>'
                    "</div>"
                    '<div id="test-status" class="govuk-task-list__status">'
                        '<strong class="govuk-tag govuk-tag--blue">Incomplete</strong>'
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
                    "</div>"
                    '<div id="test-status" class="govuk-task-list__status">Completed</div>'
                "</li>"
            ),
        ),
        (
            {"label": "test", "href": "/test", "completed": True, "hint": "Test Hint"},
            (
                '<li class="govuk-task-list__item govuk-task-list__item--with-link">'
                    '<div class="govuk-task-list__name-and-hint">'
                        '<a href="/test" aria-describedby="test-hint test-status" class="govuk-link govuk-task-list__link">test</a>'
                        '<div id="test-hint" class="govuk-task-list__hint">Test Hint</div>'
                    "</div>"
                    '<div id="test-status" class="govuk-task-list__status">Completed</div>'
                "</li>"
            ),
        ),
    ),
)
def test_task(kwargs, expected, html):
    """Test Task with various parameters.
    Args:
        kwargs (dict): The arguments to pass to Task.
        expected (str): The expected HTML output.
    """
    task = ds.Task(**kwargs)
    assert html(task) == html(expected)


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
                        "</div>"
                        '<div id="test-label-1-status" class="govuk-task-list__status">'
                            '<strong class="govuk-tag govuk-tag--blue">Incomplete</strong>'
                        "</div>"
                    "</li>"
                    '<li class="govuk-task-list__item govuk-task-list__item--with-link">'
                        '<div class="govuk-task-list__name-and-hint">'
                            '<a href="/test2" aria-describedby="test-label-2-status" class="govuk-link govuk-task-list__link">Test Label 2</a>'
                        "</div>"
                        '<div id="test-label-2-status" class="govuk-task-list__status">'
                            '<strong class="govuk-tag govuk-tag--blue">Incomplete</strong>'
                        "</div>"
                    "</li>"
                "</ul>"
            ),
        ),
    ),
)
def test_tasklist(args, expected, html):
    """Test TaskList with various parameters.
    Args:
        args (list): The arguments to pass to TaskList.
        expected (str): The expected HTML output.
    """
    tl = ds.TaskList(*args)
    assert html(tl) == html(expected)


@pytest.mark.parametrize(
    "args, expected",
    (
        (
            [
                ds.SummaryItem("Name", "John Doe"),
                ds.SummaryItem("DOB", "", ds.A("Test Label 1", "/test1")),
                ds.SummaryItem(
                    "Email",
                    "test@test.com",
                    ds.A("Test Label 2", "/test2"), ds.A("Test Label 2", "/test2"),
                ),
            ],
            (
                '<dl class="govuk-summary-list">'
                    '<div class="govuk-summary-list__row govuk-summary-list__row--no-actions">'
                        '<dt class="govuk-summary-list__key">Name</dt>'
                        '<dd class="govuk-summary-list__value">John Doe</dd>'
                    "</div>"
                    '<div class="govuk-summary-list__row">'
                        '<dt class="govuk-summary-list__key">DOB</dt>'
                        '<dd class="govuk-summary-list__value"></dd>'
                        '<dd class="govuk-summary-list__actions">'
                            '<a href="/test1" class="govuk-link">'
                                'Test Label 1 <span class="govuk-visually-hidden">dob</span>'
                            '</a>'
                        "</dd>"
                    "</div>"
                    '<div class="govuk-summary-list__row">'
                        '<dt class="govuk-summary-list__key">Email</dt>'
                        '<dd class="govuk-summary-list__value">test@test.com</dd>'
                        '<dd class="govuk-summary-list__actions">'
                            '<ul class="govuk-summary-list__actions-list">'
                                '<li class="govuk-summary-list__actions-list-item">'
                                    '<a href="/test2" class="govuk-link">'
                                        'Test Label 2 <span class="govuk-visually-hidden">email</span>'
                                    '</a>'
                                "</li>"
                                '<li class="govuk-summary-list__actions-list-item">'
                                    '<a href="/test2" class="govuk-link">'
                                        'Test Label 2 <span class="govuk-visually-hidden">email</span>'
                                    '</a>'
                                "</li>"
                            "</ul>"
                        "</dd>"
                    "</div>"
                "</div>"
            ),
        ),
    ),
)
def test_summary_list(args, expected, html):
    """Test SummaryList with various parameters.
    Args:
        args (list): The arguments to pass to SummaryList.
        expected (str): The expected HTML output.
    """
    summary = ds.SummaryList(*args)
    assert html(summary) == html(expected)


@pytest.mark.parametrize(
    "args, expected",
    (
        (
            [
                ds.SummaryItem(
                    "Email",
                    "test@test.com",
                    ds.A("Test Label 1", "/test1"),
                    ds.A("Test Label 2", "/test2"),
                ),
            ],
            (
                '<div class="govuk-summary-card">'
                    '<div class="govuk-summary-card__title-wrapper">'
                        '<h2 class="govuk-summary-card__title">Test</h2>'
                        '<ul class="govuk-summary-card__actions">'
                            '<li class="govuk-summary-card__action">'
                                '<a href="/test1" class="govuk-link">'
                                    'Test Action 1 <span class="govuk-visually-hidden">(Test)</span>'
                                '</a>'
                            "</li>"
                        "</ul>"
                    "</div>"
                    '<div class="govuk-summary-card__content">'
                        '<dl class="govuk-summary-list">'
                            '<div class="govuk-summary-list__row">'
                                '<dt class="govuk-summary-list__key">Email</dt>'
                                '<dd class="govuk-summary-list__value">test@test.com</dd>'
                                '<dd class="govuk-summary-list__actions">'
                                    '<ul class="govuk-summary-list__actions-list">'
                                        '<li class="govuk-summary-list__actions-list-item">'
                                            '<a href="/test1" class="govuk-link">'
                                                'Test Label 1 <span class="govuk-visually-hidden">email</span>'
                                            '</a>'
                                        "</li>"
                                        '<li class="govuk-summary-list__actions-list-item">'
                                            '<a href="/test2" class="govuk-link">'
                                                'Test Label 2 <span class="govuk-visually-hidden">email</span>'
                                            '</a>'
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
def test_summary_card(args, expected, html):
    """Test SummaryCard with various parameters.
    Args:
        args (list): The arguments to pass to SummaryCard.
        expected (str): The expected HTML output.
    """
    summary = ds.SummaryCard(
        title="Test",
        summary_list=ds.SummaryList(*args),
        actions=[ds.A("Test Action 1", "/test1")],
    )
    assert html(summary) == html(expected)


@pytest.mark.parametrize("component", (
    ds.Inset("test", hx_test="foo"),
    ds.Detail("test", hx_test="foo"),
    ds.Panel(hx_test="foo"),
    ds.Tag("test", hx_test="foo"),
    ds.Warning(hx_test="foo"),
    ds.Notification(hx_test="foo"),
    ds.Accordion(hx_test="foo"),
    ds.Tab(hx_test="foo"),
    ds.ErrorSummary("test", hx_test="foo"),
    ds.Table(data=[{}], hx_test="foo"),
    ds.Task("test", "/", hx_test="foo"),
    ds.TaskList(hx_test="foo"),
    ds.SummaryItem("test", "test", hx_test="foo"),
    ds.SummaryList(hx_test="foo"),
    ds.SummaryCard("test", ds.P(""), hx_test="foo"),
))
def test_html_attribute(component, html):
    """
    Test that passes an html attribute to components - that is not
    explicitly handled but should be passed through to the
    underlying FT.
    """
    assert 'hx-test="foo"' in html(component)
