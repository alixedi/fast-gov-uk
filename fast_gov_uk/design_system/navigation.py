import fasthtml.common as fh

from .utils import Next, Previous


def Backlink(href: str, text: str = "Back", inverse: bool = False, **kwargs) -> fh.FT:
    """
    A back link to the previous page.

    Args:
        href (str): Link to the previous page.
        text (str, optional): The text to display in the link. Defaults to "Back".
        inverse (bool, optional): If True, applies an inverse style. Defaults to False.
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML Backlink component.
    """
    inverse_cls = " govuk-back-link--inverse" if inverse else ""
    return fh.A(
        text,
        href=href,
        cls=f"govuk-back-link{inverse_cls}",
        **kwargs,
    )


def SkipLink(
    href: str,
    text: str = "Skip to main content",
    **kwargs,
) -> fh.FT:
    """
    Skip link component.

    Args:
        href (str): On-page anchor (e.g. #main) for the main content.
        text (str, optional): The text to display in the link. Defaults to "Skip to main content".
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML SkipLink component.
    """
    return fh.A(
        text, href=href, cls="govuk-skip-link", data_module="govuk-skip-link", **kwargs
    )


def Breadcrumbs(
    *links: tuple[str, str],
    collapse_on_mobile: bool = False,
    **kwargs,
) -> fh.FT:
    """
    Breadcrumbs component.

    Args:
        *links (tuple[str, str]): Text & URL for breadcrumb links.
        collapse_on_mobile (bool, optional): Make breadcrumbs responsive. Defaults to False.
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML Breadcrumbs component.
    """
    collapse_cls = (
        " govuk-breadcrumbs--collapse-on-mobile" if collapse_on_mobile else ""
    )
    return fh.Nav(
        fh.Ol(
            *[
                fh.Li(
                    fh.A(text, href=href, cls="govuk-breadcrumbs__link"),
                    cls="govuk-breadcrumbs__list-item",
                )
                for text, href in links
            ],
            cls="govuk-breadcrumbs__list",
        ),
        cls=f"govuk-breadcrumbs{collapse_cls}",
        aria_label="Breadcrumb",
        **kwargs,
    )


def ExitPage(
    text: str = "Exit this page",
    href: str = "https://www.bbc.co.uk/weather",
    **kwargs,
) -> fh.FT:
    """
    Exit Page component.

    Args:
        text (str, optional): The text to display on the ExitPage component. Defaults to "Exit this page".
        href (str, optional): The URL the link points to. Defaults to BBC weather service.
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML ExitPage component.
    """
    return fh.Div(
        fh.A(
            fh.Span(
                "Emergency",
                cls="govuk-visually-hidden",
            ),
            text,
            href=href,
            role="button",
            draggable="false",
            cls=(
                "govuk-button govuk-button--warning"
                " govuk-exit-this-page__button"
                " govuk-js-exit-this-page-button"
            ),
            data_module="govuk-button",
            rel="nofollow noreferrer",
        ),
        cls="govuk-exit-this-page",
        data_module="govuk-exit-this-page",
        **kwargs,
    )


def NavigationLink(
    text: str,
    href: str,
    active: bool = False,
    **kwargs,
) -> fh.FT:
    """
    NavigationLink component.

    Args:
        text (str): Text for the NavigationLink.
        href (str): Link for the NavigationLink.
        active (bool, optional): Is the NavigationLink active? Defaults to False.
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML NavigationLink component.
    """
    return fh.Li(
        fh.A(
            fh.Strong(text, cls="govuk-service-navigation__active-fallback")
            if active
            else text,
            href=href,
            cls="govuk-service-navigation__link",
            aria_current="true" if active else False,
        ),
        cls=(
            "govuk-service-navigation__item"
            f"{' govuk-service-navigation__item--active' if active else ''}"
        ),
        **kwargs,
    )


def Navigation(
    *links: fh.FT,
    service_name: str = "",
    **kwargs,
) -> fh.FT:
    """
    Service Navigation component.

    Args:
        *links (FT): List of NavigationLink components.
        service_name (str, optional): Name of the service. Defaults to "".
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML Navigation component.
    """
    return fh.Section(
        fh.Div(
            fh.Div(
                fh.Span(
                    fh.A(service_name, href="/", cls="govuk-service-navigation__link"),
                    cls="govuk-service-navigation__service-name",
                )
                if service_name
                else "",
                fh.Nav(
                    fh.Button(
                        "Menu",
                        type="button",
                        cls="govuk-service-navigation__toggle govuk-js-service-navigation-toggle",
                        aria_controls="navigation",
                        hidden=True,
                    ),
                    fh.Ul(
                        *links,
                        cls="govuk-service-navigation__list",
                        id="navigation",
                    ),
                    aria_label="Menu",
                    cls="govuk-service-navigation__wrapper",
                ),
                cls="govuk-service-navigation__container",
            ),
            cls="govuk-width-container",
        ),
        cls="govuk-service-navigation",
        aria_label="Service information",
        data_module="govuk-service-navigation",
        **kwargs,
    )


def _pagination_prev(href: str) -> fh.FT:
    """
    Previous link for pagination.

    Args:
        href (str): URL for the previous page.

    Returns:
        FT: A FastHTML previous page component.
    """
    return fh.Div(
        fh.A(
            fh.NotStr(Previous()),
            fh.Span(
                "Previous",
                fh.Span(" page", cls="govuk-visually-hidden"),
                cls="govuk-pagination__link-title",
            ),
            href=href,
            cls="govuk-link govuk-pagination__link",
            rel="prev",
        ),
        cls="govuk-pagination__prev",
    )


def _pagination_next(href: str) -> fh.FT:
    """
    Next link for pagination.

    Args:
        href (str): URL for the next page.

    Returns:
        FT: A FastHTML next page component.
    """
    return fh.Div(
        fh.A(
            fh.Span(
                "Next",
                fh.Span(" page", cls="govuk-visually-hidden"),
                cls="govuk-pagination__link-title",
            ),
            fh.NotStr(Next()),
            href=href,
            cls="govuk-link govuk-pagination__link",
            rel="next",
        ),
        cls="govuk-pagination__next",
    )


def PaginationLink(
    label: str,
    href: str,
    active: bool = False,
    **kwargs,
) -> fh.FT:
    """
    Link for pagination.

    Args:
        label (str): Label for the link.
        href (str): URL for the page.
        active (bool, optional): Is this the current page? Defaults to False.
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML component.
    """
    active_cls = " govuk-pagination__item--current" if active else ""
    return fh.Li(
        fh.A(
            label,
            href=href,
            cls="govuk-link govuk-pagination__link",
            aria_label=f"Page {label}",
            aria_current="page" if active else "",
        ),
        cls=f"govuk-pagination__item{active_cls}",
        **kwargs,
    )


def Pagination(
    *links: fh.FT,
    prev_link: str = "",
    next_link: str = "",
    **kwargs,
) -> fh.FT:
    """
    Pagination component.

    Args:
        *links (FT): List of PaginationLink components.
        prev_link (str, optional): Link for previous page. Defaults to "".
        next_link (str, optional): Link for next page. Defaults to "".
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML Pagination component.
    """
    return fh.Nav(
        _pagination_prev(prev_link) if prev_link else "",
        fh.Ul(
            *links,
            cls="govuk-pagination__list",
        ),
        _pagination_next(next_link) if next_link else "",
        cls="govuk-pagination",
        aria_label="Pagination",
        **kwargs,
    )


def PaginationBlock(
    prev: tuple[str, str],
    next: tuple[str, str],
    **kwargs,
) -> fh.FT:
    """
    PaginationBlock component.

    Args:
        prev (tuple): Text and Link for previous page.
        next (tuple): Text and Link for next page.
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML Pagination component.
    """
    prev_label, prev_link = prev
    prev_component = fh.Div(
        fh.A(
            fh.NotStr(Previous()),
            fh.Span(
                "Previous",
                fh.Span(" page", cls="govuk-visually-hidden"),
                cls="govuk-pagination__link-title",
            ),
            fh.Span(":", cls="govuk-visually-hidden"),
            fh.Span(prev_label, cls="govuk-pagination__link-label"),
            href=prev_link,
            cls="govuk-link govuk-pagination__link",
            rel="prev",
        ),
        cls="govuk-pagination__prev",
    )
    next_label, next_link = next
    next_component = fh.Div(
        fh.A(
            fh.NotStr(Next()),
            fh.Span(
                "Next",
                fh.Span(" page", cls="govuk-visually-hidden"),
                cls="govuk-pagination__link-title",
            ),
            fh.Span(":", cls="govuk-visually-hidden"),
            fh.Span(next_label, cls="govuk-pagination__link-label"),
            href=next_link,
            cls="govuk-link govuk-pagination__link",
            rel="next",
        ),
        cls="govuk-pagination__next",
    )
    return fh.Nav(
        prev_component,
        next_component,
        cls="govuk-pagination govuk-pagination--block",
        aria_label="Pagination",
        **kwargs,
    )
