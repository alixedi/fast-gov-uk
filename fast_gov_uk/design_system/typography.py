"""
GOV.UK typography components - paragraphs, headings and lists etc.
"""

import fasthtml.common as fh


def A(
    text,
    href: str = "#",
    visited: bool = False,
    inverse=False,
    newtab=False,
    **kwargs,
) -> fh.FT:
    """
    `GOV.UK Link`_ component. Links are blue and underlined by default.

    Examples:

        >>> a = ds.A("test")
        >>> str(a)
        '<a href="#" class="govuk-link">test</a>'
        >>> a = ds.A("test", href="/test")
        >>> str(a)
        '<a href="/test" class="govuk-link">test</a>'

    Args:
        text: The text to display in the link.
        href (str, optional): The URL the link points to. Defaults to "#".
        visited (bool, optional): If True, applies a visited style. Defaults to False.
        inverse (bool, optional): If True, applies an inverse style. Defaults to False.
        newtab (bool, optional): If True, opens the link in a new tab. Defaults to False.
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML link component.

    .. _GOV.UK Link: https://design-system.service.gov.uk/styles/links/
    """
    visited_cls = " govuk-link--visited" if visited else ""
    inverse_cls = " govuk-link--inverse" if inverse else ""
    cls = f"govuk-link{visited_cls}{inverse_cls}"
    newtab_attr = {"target": "_blank", "rel": "noopener noreferrer"} if newtab else {}
    return fh.A(text, href=href, cls=cls, **newtab_attr, **kwargs)


def H1(text, size="l", caption="", **kwargs) -> fh.FT:
    """
    `GOV.UK H1`_ component.

    Examples:

        >>> h1 = ds.H1("Test")
        >>> str(h1)
        '<h1 class="govuk-heading-l">Test</h1>'
        >>> h1 = ds.H1("Test", size="xl")
        >>> str(h1)
        '<h1 class="govuk-heading-xl">Test</h1>'
        >>> h1 = ds.H1("Test", caption="test caption")
        >>> str(h1)
        '<h1 class="govuk-heading-l">Test<span class="govuk-caption-l">test caption</span></h1>'

    Args:
        text: The text to display in the header.
        size (str, optional): The size of the header. Defaults to "l".
        caption (str, optional): Caption to go with the heading. Defaults to "".
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML H1 component.

    .. _GOV.UK H1: https://design-system.service.gov.uk/styles/headings/
    """
    return fh.H1(
        text,
        fh.Span(caption, cls=f"govuk-caption-{size}") if caption else "",
        cls=f"govuk-heading-{size}",
        **kwargs,
    )


def H2(text, size="m", caption="", **kwargs) -> fh.FT:
    """
    `GOV.UK H2`_ component.

    Examples:

        >>> h2 = ds.H2("Test")
        >>> str(h2)
        '<h2 class="govuk-heading-l">Test</h2>'
        >>> h2 = ds.H2("Test", size="xl")
        >>> str(h2)
        '<h2 class="govuk-heading-xl">Test</h2>'
        >>> h2 = ds.H2("Test", caption="test caption")
        >>> str(h2)
        '<h2 class="govuk-heading-l">Test<span class="govuk-caption-l">test caption</span></h2>'

    Args:
        text: The text to display in the header.
        size (str, optional): The size of the header. Defaults to "l".
        caption (str, optional): Caption to go with the heading. Defaults to "".
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML H2 component.

    .. _GOV.UK H2: https://design-system.service.gov.uk/styles/headings/
    """
    return fh.H2(
        text,
        fh.Span(caption, cls=f"govuk-caption-{size}") if caption else "",
        cls=f"govuk-heading-{size}",
        **kwargs,
    )


def H3(text, size="s", caption="", **kwargs) -> fh.FT:
    """
    `GOV.UK H2`_ component.

    Examples:

        >>> h2 = ds.H2("Test")
        >>> str(h2)
        '<h2 class="govuk-heading-l">Test</h2>'
        >>> h2 = ds.H2("Test", size="xl")
        >>> str(h2)
        '<h2 class="govuk-heading-xl">Test</h2>'
        >>> h2 = ds.H2("Test", caption="test caption")
        >>> str(h2)
        '<h2 class="govuk-heading-l">Test<span class="govuk-caption-l">test caption</span></h2>'

    Args:
        text: The text to display in the header.
        size (str, optional): The size of the header. Defaults to "l".
        caption (str, optional): Caption to go with the heading. Defaults to "".
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML H2 component.

    .. _GOV.UK H2: https://design-system.service.gov.uk/styles/headings/
    """
    return fh.H3(
        text,
        fh.Span(caption, cls=f"govuk-caption-{size}") if caption else "",
        cls=f"govuk-heading-{size}",
        **kwargs,
    )


def P(*content, lead=False, small=False, **kwargs) -> fh.FT:
    """
    `GOV.UK Paragraph`_ component. The default paragraph font size is 19px.

    Examples:

        >>> p = ds.P("test")
        >>> str(p)
        '<p class="govuk-body">test</p>'
        >>> p = ds.P("test", lead=True)
        >>> str(p)
        '<p class="govuk-body-l">test</p>'
        >>> p = ds.P("test", small=True)
        >>> str(p)
        '<p class="govuk-body-s">test</p>'

    Args:
        *content: The list of content to display in the paragraph.
        lead (bool, optional): If True, applies a lead style. Defaults to False.
        small (bool, optional): If True, applies a small style. Defaults to False.
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML paragraph component.

    .. _GOV.UK Paragraph: https://design-system.service.gov.uk/styles/paragraphs/
    """
    if lead and small:
        raise ValueError("Cannot set both lead and small to True.")
    cls_suffix = "-l" if lead else "-s" if small else ""

    return fh.P(*content, cls=f"govuk-body{cls_suffix}", **kwargs)


def Li(*args, **kwargs) -> fh.FT:
    """
    `GOV.UK list item` component. Used to pass-in list items into :py:meth:`Ul`.

    Args:
        *args: Items to include in the list.
        **kwargs: Additional attributes for the list.

    Returns:
        FT: A FastHTML list item component.

    .. _GOV.UK list item: https://design-system.service.gov.uk/styles/lists/
    """
    return fh.Li(*args, **kwargs)


def Ul(*args, bullet=False, numbered=False, spaced=False, **kwargs) -> fh.FT:
    """
    `GOV.UK unordered list`_ component. Use lists to make blocks of text easier to read, and to
    break information into manageable chunks.

    Examples:

        >>> li = ds.Li("test")
        >>> ul = ds.Ul(li)
        >>> str(ul)
        '<ul class="govuk-list"><li>test</li></ul>'
        >>> ul = ds.Ul(li, bullet=True)
        >>> str(ul)
        '<ul class="govuk-list govuk-list--bullet"><li>test</li></ul>'
        >>> ul = ds.Ul(li, numbered=True)
        >>> str(ul)
        '<ul class="govuk-list govuk-list--number"><li>test</li></ul>'

    Args:
        *args: Items to include in the list.
        bullet (bool, optional): If True, applies a bullet style. Defaults to False.
        numbered (bool, optional): If True, applies a numbered style. Defaults to False.
        spaced (bool, optional): If True, applies a spaced style. Defaults to False.
        **kwargs: Additional attributes for the list.

    Returns:
        FT: A FastHTML unordered list component.

    .. _GOV.UK unordered list: https://design-system.service.gov.uk/styles/lists/
    """
    if bullet and numbered:
        raise ValueError("Cannot set both bullet and numbered to True.")
    if bullet:
        cls = "govuk-list govuk-list--bullet"
    elif numbered:
        cls = "govuk-list govuk-list--number"
    else:
        cls = "govuk-list"
    if spaced:
        cls += " govuk-list--spaced"
    return fh.Ul(*args, cls=cls, **kwargs)
