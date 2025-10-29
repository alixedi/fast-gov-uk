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
    Link component.

    Args:
        text: The text to display in the link.
        href (str, optional): The URL the link points to. Defaults to "#".
        visited (bool, optional): If True, applies a visited style. Defaults to False.
        inverse (bool, optional): If True, applies an inverse style. Defaults to False.
        newtab (bool, optional): If True, opens the link in a new tab. Defaults to False.
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML link component.
    """
    visited_cls = " govuk-link--visited" if visited else ""
    inverse_cls = " govuk-link--inverse" if inverse else ""
    cls = f"govuk-link{visited_cls}{inverse_cls}"
    newtab_attr = {"target": "_blank", "rel": "noopener noreferrer"} if newtab else {}
    return fh.A(text, href=href, cls=cls, **newtab_attr, **kwargs)


def H1(text, size="l", caption="", **kwargs) -> fh.FT:
    """
    H1 component.

    Args:
        text: The text to display in the header.
        size (str, optional): The size of the header. Defaults to "l".
        caption (str, optional): Caption to go with the heading. Defaults to "".
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML H1 component.
    """
    return fh.H1(
        text,
        fh.Span(caption, cls=f"govuk-caption-{size}") if caption else "",
        cls=f"govuk-heading-{size}",
        **kwargs,
    )


def H2(text, size="m", caption="", **kwargs) -> fh.FT:
    """
    H2 component.

    Args:
        text: The text to display in the header.
        size (str, optional): The size of the header. Defaults to "m".
        caption (str, optional): Caption to go with the heading. Defaults to "".
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML H2 component.
    """
    return fh.H2(
        text,
        fh.Span(caption, cls=f"govuk-caption-{size}") if caption else "",
        cls=f"govuk-heading-{size}",
        **kwargs,
    )


def H3(text, size="s", caption="", **kwargs) -> fh.FT:
    """
    H3 component.

    Args:
        text: The text to display in the header.
        size (str, optional): The size of the header. Defaults to "s".
        caption (str, optional): Caption to go with the heading. Defaults to "".
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML H3 component.
    """
    return fh.H3(
        text,
        fh.Span(caption, cls=f"govuk-caption-{size}") if caption else "",
        cls=f"govuk-heading-{size}",
        **kwargs,
    )


def P(*content, lead=False, small=False, **kwargs) -> fh.FT:
    """
    Paragraph component.

    Args:
        *content: The list of content to display in the paragraph.
        lead (bool, optional): If True, applies a lead style. Defaults to False.
        small (bool, optional): If True, applies a small style. Defaults to False.
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML paragraph component.
    """
    if lead and small:
        raise ValueError("Cannot set both lead and small to True.")
    cls_suffix = "-l" if lead else "-s" if small else ""

    return fh.P(*content, cls=f"govuk-body{cls_suffix}", **kwargs)


def Li(*args, **kwargs) -> fh.FT:
    """
    List item component.

    Args:
        *args: Items to include in the list.
        **kwargs: Additional attributes for the list.

    Returns:
        FT: A FastHTML list item component.
    """
    return fh.Li(*args, **kwargs)


def Ul(*args, bullet=False, numbered=False, spaced=False, **kwargs) -> fh.FT:
    """
    Unordered list component.

    Args:
        *args: Items to include in the list.
        bullet (bool, optional): If True, applies a bullet style. Defaults to False.
        numbered (bool, optional): If True, applies a numbered style. Defaults to False.
        spaced (bool, optional): If True, applies a spaced style. Defaults to False.
        **kwargs: Additional attributes for the list.

    Returns:
        FT: A FastHTML unordered list component.
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
