"""
GOV.UK Design System components for navigation elements such as back link, skip link, exit this page
as well as breadcrumbs, service navigation and pagination.
"""

import fasthtml.common as fh

from .utils import Next, Previous


def BackLink(href: str, text: str = "Back", inverse: bool = False, **kwargs) -> fh.FT:
    """
    The `GOV.UK back link`_ component to help users navigate to the previous page
    in a multi-page transaction.

    Examples:

        >>> backlink = ds.BackLink(href="/back", text="Go back")
        >>> str(backlink)
        '<a href="/back" class="govuk-back-link">Go back</a>'

    Args:
        href (str): Link to the previous page.
        text (str, optional): The text to display in the link. Defaults to "Back".
        inverse (bool, optional): If True, applies an inverse style. Defaults to False.
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML BackLink component.

    .. _GOV.UK back link: https://design-system.service.gov.uk/components/back-link/
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
    `GOV.UK skip link`_ component to help keyboard-only users skip to the main content on a page.

    Examples:
        >>> skip_link = ds.SkipLink(href="#main")
        >>> str(skip_link)
        '<a href="#main" data-module="govuk-skip-link" class="govuk-skip-link">Skip to main content</a>'

    Args:
        href (str): On-page anchor (e.g. #main) for the main content.
        text (str, optional): The text to display in the link. Defaults to "Skip to main content".
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML SkipLink component.

    .. _GOV.UK skip link: https://design-system.service.gov.uk/components/skip-link/
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
    `GOV.UK breadcrumbs`_ component to help users understand where they are within a website's structure
    and move between levels.

    Examples:

        >>> ds.Breadcrumbs(
        ...     ("Home", "/"),
        ...     ("Section", "/section"),
        ... )
        # Home > Section

    Args:
        *links (tuple[str, str]): Text & URL for breadcrumb links.
        collapse_on_mobile (bool, optional): Make breadcrumbs responsive. Defaults to False.
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML Breadcrumbs component.

    .. _GOV.UK Breadcrumbs: https://design-system.service.gov.uk/components/breadcrumbs/
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
    `GOV.UK exit page`_ component to give users a way to quickly and safely exit a service,
    website or application.

    Examples:

        >>> ds.ExitPage()
        # An Exit this page button linking to BBC weather service.
        >>> ds.ExitPage(text="Leave now", href="https://google.com")
        # An Exit this page button with the text "Leave now" linking to Google.

    Args:
        text (str, optional): The text to display on the ExitPage component. Defaults to "Exit this page".
        href (str, optional): The URL the link points to. Defaults to BBC weather service.
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML ExitPage component.

    .. _GOV.UK exit page: https://design-system.service.gov.uk/components/exit-this-page/
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
    Navigation link to pass into the :py:meth:`Navigation` component.

    Examples:

        >>> nav_link = ds.NavigationLink(text="Home", href="/")
        >>> str(nav_link)
        '<li class="govuk-service-navigation__item">'
            '<a href="/" class="govuk-service-navigation__link">home</a>'
        '</li>'

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
    `GOV.UK Service Navigation`_ component to help users understand that they're using
    your service and lets them navigate around your service.

    You can pass it a list of :py:meth:`NavigationLink` components to build the
    navigation menu.

    Optionally, you can provide a `service_name` to display the name of your service
    on the navigation menu.

    Examples:

        >>> nav = ds.Navigation(
        ...     ds.NavigationLink(text="Home", href="/", active=True),
        ...     ds.NavigationLink(text="About", href="/about"),
        ...     service_name="My Service",
        ... )
        # *Home* | About

    Args:
        *links (FT): List of NavigationLink components.
        service_name (str, optional): Name of the service. Defaults to "".
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML Navigation component.

    .. _GOV.UK Service Navigation: https://design-system.service.gov.uk/components/service-navigation/
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
    Previous link for pagination that looks like a left arrow.

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
    Next link for pagination that looks like a right arrow.

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
    Pagination link to pass into the :py:meth:`Pagination` component.

    Examples:

        >>> page_link = ds.PaginationLink(label="2", href="/page/2")
        >>> str(page_link)
        '<li class="govuk-pagination__item">'
            '<a href="/2" aria-label="Page 1" class="govuk-link govuk-pagination__link">1</a>'
        '</li>'

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
    `GOV.UK Pagination`_ component to help users navigate forwards and backwards
    through a series of pages.

    You can pass it a list of :py:meth:`PaginationLink` components to build the
    Pagination.

    `prev_link` and `next_link` are optional links for previous and next pages.


    Examples:

        >>> pagination = ds.Pagination(
        ...     ds.PaginationLink(label="1", href="/page/1"),
        ...     ds.PaginationLink(label="2", href="/page/2", active=True),
        ...     ds.PaginationLink(label="3", href="/page/3"),
        ...     prev_link="/page/1",
        ...     next_link="/page/3",
        ... )
        # ← Previous 1 *2* 3 Next →

    Args:
        *links (FT): List of PaginationLink components.
        prev_link (str, optional): Link for previous page. Defaults to "".
        next_link (str, optional): Link for next page. Defaults to "".
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML Pagination component.

    .. _GOV.UK Pagination: https://design-system.service.gov.uk/components/pagination/
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
    `GOV.UK block-style pagination`_ component to let users navigate through related content
    that has been split across multiple pages.

    Examples:

        >>> pagination = ds.PaginationBlock(
        ...     prev=("Previous page", "/previous"),
        ...     next=("Next page", "/next"),
        ... )
        # ← Previous: Previous page
        #   Next: Next page →

    Args:
        prev (tuple): Text and Link for previous page.
        next (tuple): Text and Link for next page.
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML Pagination component.

    .. _GOV.UK block-style pagination: https://design-system.service.gov.uk/components/pagination/
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
