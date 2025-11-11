import pytest

import fast_gov_uk.design_system as ds
from fast_gov_uk.design_system import Next, Previous


@pytest.mark.parametrize(
    "kwargs, expected",
    (
        (
            {"text": "Test", "href": "/test"},
            '<a href="/test" class="govuk-back-link">Test</a>',
        ),
        (
            {"text": "Test", "href": "/test", "inverse": True},
            '<a href="/test" class="govuk-back-link govuk-back-link--inverse">Test</a>',
        ),
        (
            {"text": "", "href": "/test"},
            '<a href="/test" class="govuk-back-link"></a>',
        ),
        (
            {
                "href": "/test",
            },
            '<a href="/test" class="govuk-back-link">Back</a>',
        ),
    ),
)
def test_backlink(kwargs, expected, html):
    """Test backlink with various parameters.
    Args:
        kwargs (dict): The arguments to pass to backlink.
        expected (str): The expected HTML output.
    """
    backlink = ds.BackLink(**kwargs)
    assert html(backlink) == html(expected)


@pytest.mark.parametrize(
    "kwargs, expected",
    (
        (
            {"text": "Test", "href": "/test"},
            '<a href="/test" data-module="govuk-skip-link" class="govuk-skip-link">Test</a>',
        ),
    ),
)
def test_skip_link(kwargs, expected, html):
    """Test SkipLink with various parameters.
    Args:
        kwargs (dict): The arguments to pass to SkipLink.
        expected (str): The expected HTML output.
    """
    link = ds.SkipLink(**kwargs)
    assert html(link) == html(expected)


@pytest.mark.parametrize(
    "args, expected",
    (
        (
            [("Home", "/"), ("Test", "/test")],
            (
                '<nav aria-label="Breadcrumb" class="govuk-breadcrumbs">'
                    '<ol class="govuk-breadcrumbs__list">'
                        '<li class="govuk-breadcrumbs__list-item">'
                            '<a href="/" class="govuk-breadcrumbs__link">Home</a>'
                        "</li>"
                        '<li class="govuk-breadcrumbs__list-item">'
                            '<a href="/test" class="govuk-breadcrumbs__link">Test</a>'
                        "</li>"
                    "</ol>"
                "</nav>"
            ),
        ),
    ),
)
def test_breadcrumb(args, expected, html):
    """Test Breadcrumb with various parameters.
    Args:
        args (list): The args to pass to Breadcrumb.
        expected (str): The expected HTML output.
    """
    bc = ds.Breadcrumbs(*args)
    assert html(bc) == html(expected)


@pytest.mark.parametrize(
    "kwargs, expected",
    (
        (
            {},
            (
                '<div data-module="govuk-exit-this-page" class="govuk-exit-this-page">'
                    '<a href="https://www.bbc.co.uk/weather" role="button" draggable="false" data-module="govuk-button" rel="nofollow noreferrer" class="govuk-button govuk-button--warning govuk-exit-this-page__button govuk-js-exit-this-page-button">'
                        '<span class="govuk-visually-hidden">Emergency</span>'
                        "Exit this page"
                    "</a>"
                "</div>"
            ),
        ),
        (
            {"text": "Test", "href": "/test"},
            (
                '<div data-module="govuk-exit-this-page" class="govuk-exit-this-page">'
                    '<a href="/test" role="button" draggable="false" data-module="govuk-button" rel="nofollow noreferrer" class="govuk-button govuk-button--warning govuk-exit-this-page__button govuk-js-exit-this-page-button">'
                        '<span class="govuk-visually-hidden">Emergency</span>'
                        "Test"
                    "</a>"
                "</div>"
            ),
        ),
    ),
)
def test_exit_page(kwargs, expected, html):
    """Test Exit Page with various parameters.
    Args:
        kwargs (dict): The arguments to pass to ExitPage.
        expected (str): The expected HTML output.
    """
    exit = ds.ExitPage(**kwargs)
    assert html(exit) == html(expected)


@pytest.mark.parametrize(
    "kwargs, expected",
    (
        (
            {"text": "test", "href": "/test"},
            (
                '<li class="govuk-service-navigation__item">'
                    '<a href="/test" class="govuk-service-navigation__link">test</a>'
                "</li>"
            ),
        ),
        (
            {"text": "test", "href": "/test", "active": True},
            (
                '<li class="govuk-service-navigation__item govuk-service-navigation__item--active">'
                    '<a href="/test" aria-current="true" class="govuk-service-navigation__link">'
                        '<strong class="govuk-service-navigation__active-fallback">test</strong>'
                    "</a>"
                "</li>"
            ),
        ),
    ),
)
def test_navigation_link(kwargs, expected, html):
    """Test NavigationLink with various parameters.
    Args:
        kwargs (dict): The arguments to pass to NvigationLink.
        expected (str): The expected HTML output.
    """
    link = ds.NavigationLink(**kwargs)
    assert html(link) == html(expected)


@pytest.mark.parametrize(
    "args, expected",
    (
        (
            [
                ds.NavigationLink("Test Label 1", "/test1"),
                ds.NavigationLink("Test Label 2", "/test2"),
            ],
            (
                '<section aria-label="Service information" data-module="govuk-service-navigation" class="govuk-service-navigation">'
                    '<div class="govuk-width-container">'
                        '<div class="govuk-service-navigation__container">'
                            '<span class="govuk-service-navigation__service-name">'
                                '<a href="/" class="govuk-service-navigation__link">Test</a>'
                            "</span>"
                            '<nav aria-label="Menu" class="govuk-service-navigation__wrapper">'
                                '<button type="button" aria-controls="navigation" hidden class="govuk-service-navigation__toggle govuk-js-service-navigation-toggle">Menu</button>'
                                '<ul id="navigation" class="govuk-service-navigation__list">'
                                    '<li class="govuk-service-navigation__item">'
                                        '<a href="/test1" class="govuk-service-navigation__link">Test Label 1</a>'
                                    "</li>"
                                    '<li class="govuk-service-navigation__item">'
                                        '<a href="/test2" class="govuk-service-navigation__link">Test Label 2</a>'
                                    "</li>"
                                "</ul>"
                            "</nav>"
                        "</div>"
                    "</div>"
                "</section>"
            ),
        ),
    ),
)
def test_navigation(args, expected, html):
    """Test Navigation with various parameters.
    Args:
        args (list): The arguments to pass to Navigation.
        expected (str): The expected HTML output.
    """
    nav = ds.Navigation(*args, service_name="Test")
    assert html(nav) == html(expected)


@pytest.mark.parametrize(
    "kwargs, expected",
    (
        (
            {
                "links":
                    [
                        ds.PaginationLink("1", "/test?page=1", active=True),
                        ds.PaginationLink("2", "/test?page=2"),
                        ds.PaginationLink("3", "/test?page=3"),
                    ],
                    "next_link": "/test?page=2",
            },
            (
                '<nav aria-label="Pagination" class="govuk-pagination">'
                    '<ul class="govuk-pagination__list">'
                        '<li class="govuk-pagination__item govuk-pagination__item--current">'
                            '<a href="/test?page=1" aria-label="Page 1" aria-current="page" class="govuk-link govuk-pagination__link">1</a>'
                        "</li>"
                        '<li class="govuk-pagination__item">'
                            '<a href="/test?page=2" aria-label="Page 2" class="govuk-link govuk-pagination__link">2</a>'
                        "</li>"
                        '<li class="govuk-pagination__item">'
                            '<a href="/test?page=3" aria-label="Page 3" class="govuk-link govuk-pagination__link">3</a>'
                        "</li>"
                    "</ul>"
                    '<div class="govuk-pagination__next">'
                        '<a href="/test?page=2" rel="next" class="govuk-link govuk-pagination__link">'
                            '<span class="govuk-pagination__link-title">Next<span class="govuk-visually-hidden"> page</span></span>'
                            f"{Next()}"
                        "</a>"
                    "</div>"
                "</nav>"
            ),
        ),
        (
            {
                "links":
                    [
                        ds.PaginationLink("1", "/test?page=1"),
                        ds.PaginationLink("2", "/test?page=2", active=True),
                        ds.PaginationLink("3", "/test?page=3"),
                    ],
                    "prev_link": "/test?page=1",
                    "next_link": "/test?page=3",
            },
            (
                '<nav aria-label="Pagination" class="govuk-pagination">'
                    '<div class="govuk-pagination__prev">'
                        '<a href="/test?page=1" rel="prev" class="govuk-link govuk-pagination__link">'
                            f"{Previous()}"
                            '<span class="govuk-pagination__link-title">Previous<span class="govuk-visually-hidden"> page</span></span>'
                        "</a>"
                    "</div>"
                    '<ul class="govuk-pagination__list">'
                        '<li class="govuk-pagination__item">'
                            '<a href="/test?page=1" aria-label="Page 1" class="govuk-link govuk-pagination__link">1</a>'
                        "</li>"
                        '<li class="govuk-pagination__item govuk-pagination__item--current">'
                            '<a href="/test?page=2" aria-label="Page 2" aria-current="page" class="govuk-link govuk-pagination__link">2</a>'
                        "</li>"
                        '<li class="govuk-pagination__item">'
                            '<a href="/test?page=3" aria-label="Page 3" class="govuk-link govuk-pagination__link">3</a>'
                        "</li>"
                    "</ul>"
                    '<div class="govuk-pagination__next">'
                        '<a href="/test?page=3" rel="next" class="govuk-link govuk-pagination__link">'
                        '<span class="govuk-pagination__link-title">Next<span class="govuk-visually-hidden"> page</span></span>'
                            f"{Next()}"
                        "</a>"
                    "</div>"
                "</nav>"
            ),
        ),
        (
            {
                "links":
                    [
                        ds.PaginationLink("1", "/test?page=1"),
                        ds.PaginationLink("2", "/test?page=2"),
                        ds.PaginationLink("3", "/test?page=3", active=True),
                    ],
                    "prev_link": "/test?page=2",
            },
            (
                '<nav aria-label="Pagination" class="govuk-pagination">'
                    '<div class="govuk-pagination__prev">'
                        '<a href="/test?page=2" rel="prev" class="govuk-link govuk-pagination__link">'
                            f"{Previous()}"
                            '<span class="govuk-pagination__link-title">Previous<span class="govuk-visually-hidden"> page</span></span>'
                        "</a>"
                    "</div>"
                    '<ul class="govuk-pagination__list">'
                        '<li class="govuk-pagination__item">'
                            '<a href="/test?page=1" aria-label="Page 1" class="govuk-link govuk-pagination__link">1</a>'
                        "</li>"
                        '<li class="govuk-pagination__item">'
                            '<a href="/test?page=2" aria-label="Page 2" class="govuk-link govuk-pagination__link">2</a>'
                        "</li>"
                        '<li class="govuk-pagination__item govuk-pagination__item--current">'
                            '<a href="/test?page=3" aria-label="Page 3" aria-current="page" class="govuk-link govuk-pagination__link">3</a>'
                        "</li>"
                    "</ul>"
                "</nav>"
            ),
        ),
    ),
)
def test_pagination(kwargs, expected, html):
    """Test Pagination with various parameters.
    Args:
        kwargs (dict): The kwargs to pass to Pagination.
        expected (str): The expected HTML output.
    """
    links = kwargs.pop("links")
    page = ds.Pagination(*links, **kwargs)
    assert html(page) == html(expected)


@pytest.mark.parametrize("component", (
    ds.BackLink("/", hx_test="foo"),
    ds.SkipLink("/", hx_test="foo"),
    ds.Breadcrumbs(("test", "/"), hx_test="foo"),
    ds.ExitPage(hx_test="foo"),
    ds.NavigationLink("test", "/", hx_test="foo"),
    ds.Navigation(hx_test="foo"),
    ds.Pagination(hx_test="foo"),
))
def test_html_attribute(component, html):
    """
    Test that passes an html attribute to components - that is not
    explicitly handled but should be passed through to the
    underlying FT.
    """
    assert 'hx-test="foo"' in html(component)
