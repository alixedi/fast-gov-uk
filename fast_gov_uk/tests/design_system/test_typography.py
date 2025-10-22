import pytest

from fast_gov_uk.design_system import H1, H2, H3, A, Li, P, Ul


@pytest.mark.parametrize(
    "kwargs, expected",
    (
        (
            {"text": "Test"},
            '<a href="#" class="govuk-link">Test</a>',
        ),
        (
            {"text": "Test", "href": "/test"},
            '<a href="/test" class="govuk-link">Test</a>',
        ),
        (
            {"text": "Test", "inverse": True},
            '<a href="#" class="govuk-link govuk-link--inverse">Test</a>',
        ),
        (
            {"text": "Test", "visited": True},
            '<a href="#" class="govuk-link govuk-link--visited">Test</a>',
        ),
        (
            {"text": "Test", "newtab": True},
            '<a href="#" target="_blank" rel="noopener noreferrer" class="govuk-link">Test</a>',
        ),
    ),
)
def test_a(kwargs, expected):
    """Test A with various parameters.
    Args:
        kwargs (dict): The arguments to pass to A.
        expected (str): The expected HTML output.
    """
    link = A(**kwargs)
    assert str(link) == expected


@pytest.mark.parametrize(
    "kwargs, expected",
    (
        (
            {"text": "Test"},
            '<h1 class="govuk-heading-l">Test</h1>',
        ),
        (
            {"text": "Test", "size": "m"},
            '<h1 class="govuk-heading-m">Test</h1>',
        ),
        (
            {"text": "Test", "caption": "Caption"},
            '<h1 class="govuk-heading-l">Test<span class="govuk-caption-l">Caption</span></h1>',
        ),
    ),
)
def test_h1(kwargs, expected):
    """Test H1 with various parameters.
    Args:
        kwargs (dict): The arguments to pass to H1.
        expected (str): The expected HTML output.
    """
    heading = H1(**kwargs)
    assert str(heading) == expected


@pytest.mark.parametrize(
    "kwargs, expected",
    (
        (
            {"text": "Test"},
            '<h2 class="govuk-heading-m">Test</h2>',
        ),
        (
            {"text": "Test", "size": "s"},
            '<h2 class="govuk-heading-s">Test</h2>',
        ),
        (
            {"text": "Test", "caption": "Caption"},
            '<h2 class="govuk-heading-m">Test<span class="govuk-caption-m">Caption</span></h2>',
        ),
    ),
)
def test_h2(kwargs, expected):
    """Test H2 with various parameters.
    Args:
        kwargs (dict): The arguments to pass to H2.
        expected (str): The expected HTML output.
    """
    heading = H2(**kwargs)
    assert str(heading) == expected


@pytest.mark.parametrize(
    "kwargs, expected",
    (
        (
            {"text": "Test"},
            '<h3 class="govuk-heading-s">Test</h3>',
        ),
        (
            {"text": "Test", "size": "m"},
            '<h3 class="govuk-heading-m">Test</h3>',
        ),
        (
            {"text": "Test", "caption": "Caption"},
            '<h3 class="govuk-heading-s">Test<span class="govuk-caption-s">Caption</span></h3>',
        ),
    ),
)
def test_h3(kwargs, expected):
    """Test H3 with various parameters.
    Args:
        kwargs (dict): The arguments to pass to H3.
        expected (str): The expected HTML output.
    """
    heading = H3(**kwargs)
    assert str(heading) == expected


@pytest.mark.parametrize(
    "kwargs, expected",
    (
        (
            {"content": "Test"},
            '<p class="govuk-body">Test</p>',
        ),
        (
            {"content": "Test", "lead": True},
            '<p class="govuk-body-l">Test</p>',
        ),
        (
            {"content": "Test", "small": True},
            '<p class="govuk-body-s">Test</p>',
        ),
        (
            {"content": ["Test ", A("a link", "/")]},
            '<p class="govuk-body">Test <a href="/" class="govuk-link">a link</a></p>',
        ),
    ),
)
def test_p(kwargs, expected):
    """Test P with various parameters.
    Args:
        kwargs (dict): The arguments to pass to P.
        expected (str): The expected HTML output.
    """
    para = P(*kwargs.pop("content"), **kwargs)
    assert str(para) == expected


@pytest.mark.parametrize(
    "args, kwargs, expected",
    (
        (
            (Li("Item 1"), Li("Item 2")),
            {},
            '<ul class="govuk-list"><li>Item 1</li><li>Item 2</li></ul>',
        ),
        (
            (Li("Item 1"), Li("Item 2")),
            {"bullet": True},
            '<ul class="govuk-list govuk-list--bullet"><li>Item 1</li><li>Item 2</li></ul>',
        ),
        (
            (Li("Item 1"), Li("Item 2")),
            {"numbered": True},
            '<ul class="govuk-list govuk-list--number"><li>Item 1</li><li>Item 2</li></ul>',
        ),
        (
            (Li("Item 1"), Li("Item 2")),
            {"spaced": True},
            '<ul class="govuk-list govuk-list--spaced"><li>Item 1</li><li>Item 2</li></ul>',
        ),
    ),
)
def test_ul(args, kwargs, expected):
    """Test UL with various parameters.
    Args:
        args (list): The Lis to pass to Ul.
        kwargs (dict): The arguments to pass to Ul.
        expected (str): The expected HTML output.
    """
    list = Ul(*args, **kwargs)
    assert str(list) == expected


@pytest.mark.parametrize("component", (
    A("test", hx_test="foo"),
    H1("test", hx_test="foo"),
    H2("test", hx_test="foo"),
    H3("test", hx_test="foo"),
    P("test", hx_test="foo"),
    Ul("test", hx_test="foo"),
))
def test_html_attribute(component, html):
    """
    Test that passes an html attribute to components - that is not
    explicitly handled but should be passed through to the
    underlying FT.
    """
    assert 'hx-test="foo"' in html(component)


def test_p_error():
    with pytest.raises(ValueError, match="Cannot set both lead and small to True."):
        P("test", lead=True, small=True)


def test_ul_error():
    with pytest.raises(ValueError, match="Cannot set both bullet and numbered to True."):
        Ul("test", bullet=True, numbered=True)
