"""
GOV.UK Design System components for page elements such as Header, Footer and PhaseBanner.

Includes the generic :py:meth:`Page` component that renders a standard GOV.UK Page wth
a GOV.UK Header, a GOV.UK PhaseBanner and a GOV.UK Footer and of course - whatever content
you might want to add to it.

Also includes a generic :py:meth:`Cookies` component that renders a standard GOV.UK Cookies
Page that you can customise for your service.
"""

import fasthtml.common as fh

from .components import Table
from .typography import H1, H2, P
from .utils import OGL, Crown, Logo


def Header(title: str = "", homepage: str = "/", **kwargs) -> fh.FT:
    """
    `GOV.UK Header`_ component that supports a title (name of your service)
    that is also a link to your homepage.

    If you are trying to render a standard GOV.UK page, you should probably
    use the :py:meth:`Page` component - which includes a header.

    Example:

        >>> ds.Header()
        # The basic GOV.UK header without a title or a link
        >>> ds.Header("MyService")
        # GOV.UK header with the title "MyService" that links to the page "/"
        >>> ds.Header("MyService", "/foo")
        # GOV.UK header with the title "MyService" that links to the page "/foo"

    Args:
        title (str, optional): The title of the header. Defaults to "".
        homepage (str, optional): The URL of the homepage. Defaults to "/".
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML Header component.

    .. _GOV.UK Header: https://design-system.service.gov.uk/components/header/
    """
    return fh.Header(
        fh.Div(
            fh.Div(
                fh.A(
                    fh.NotStr(Logo()),
                    fh.Span(title, cls="govuk-header__product-name"),
                    href=homepage,
                    cls="govuk-header__link govuk-header__link--homepage",
                    aria_label="Home",
                ),
                cls="govuk-header__logo",
            ),
            cls="govuk-header__container govuk-width-container",
        ),
        cls="govuk-header",
        data_module="govuk-header",
        **kwargs,
    )


def FooterLink(
    text: str,
    href: str,
    **kwargs,
) -> fh.FT:
    """
    A link in the `GOV.UK Footer`_ component.

    Unless you are trying to build your own footer, you should probably use
    the :py:meth:`Footer` component.

    Examples:

        >>> ds.FooterLink("Home", "/")
        # Renders a footer link to the home page

    Args:
        text (str): The text to display in the link.
        href (str): The URL the link points to.
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML FooterLink component.

    .. _GOV.UK Footer: https://design-system.service.gov.uk/components/footer/
    """
    return fh.A(
        text,
        href=href,
        cls="govuk-footer__link",
        **kwargs,
    )


def Footer(*links: tuple[str, str], **kwargs) -> fh.FT:
    """
    `GOV.UK Footer`_ component with optional links.

    If you are trying to render a standard GOV.UK page, you should probably
    use the :py:meth:`Page` component.

    The :py:meth:`Page` component pulls in the `Footer` from the `/footer`
    endpoint so that there is one and only one place with the definition for
    the Footer of your service.

    Examples:

        >>> ds.Footer(("Home", "/"), ("Feedback", "/feedback"))
        # Renders a GOV.UK Footer with links to the home page and the feedback page

    Args:
        *links (tuple[str, str]): Footer links as (text, href).
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML Footer component.

    .. _GOV.UK Footer: https://design-system.service.gov.uk/components/footer/
    """
    return fh.Footer(
        fh.Div(
            fh.NotStr(Crown()),
            fh.Div(
                fh.Div(
                    fh.H2("Support links", cls="govuk-visually-hidden")
                    if links
                    else "",
                    fh.Ul(
                        *[
                            fh.Li(
                                FooterLink(text, href),
                                cls="govuk-footer__inline-list-item",
                            )
                            for text, href in links
                        ],
                        cls="govuk-footer__inline-list",
                    )
                    if links
                    else "",
                    fh.NotStr(OGL()),
                    fh.Span(
                        "All content is available under the",
                        fh.A(
                            "Open Government Licence v3.0",
                            cls="govuk-footer__link",
                            href="https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
                            rel="license",
                        ),
                        cls="govuk-footer__licence-description",
                    ),
                    cls="govuk-footer__meta-item govuk-footer__meta-item--grow",
                ),
                fh.Div(
                    fh.A(
                        "© Crown copyright",
                        href="https://www.nationalarchives.gov.uk/information-management/re-using-public-sector-information/uk-government-licensing-framework/crown-copyright/",
                        cls="govuk-footer__link govuk-footer__copyright-logo",
                    ),
                    cls="govuk-footer__meta-item",
                ),
                cls="govuk-footer__meta",
            ),
            cls="govuk-width-container",
        ),
        cls="govuk-footer",
        **kwargs,
    )


def PhaseBanner(
    *content: fh.FT,
    phase: str = "Alpha",
    **kwargs,
) -> fh.FT:
    """
    A `GOV.UK Phase Banner`_ component - specifying if your service is e.g. "Alpha" or "Beta".

    If you are trying to render a standard GOV.UK page, you should probably
    use the :py:meth:`Page` component.

    The :py:meth:`Page` component pulls in the `PhaseBanner` from the `/phase`
    endpoint so that there is one and only one place with the definition for
    the PhaseBanner of your service.

    Examples:

        >>> ds.PhaseBanner("This is a new service")
        # Renders a GOV.UK PhaseBanner with the message "This is a new service"
        >>> ds.PhaseBanner("This is a new service", phase="Beta")
        # Renders the same PhaseBanner but with a "Beta" tag instead of "Alpha"

    Args:
        *content (FT): The content to display in the phase banner.
        phase (str, optional): The phase of the project. Defaults to "Alpha".
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML PhaseBanner component.

    .. _GOV.UK Phase Banner: https://design-system.service.gov.uk/components/phase-banner/
    """
    return fh.Div(
        fh.Div(
            fh.P(
                fh.Strong(
                    phase,
                    cls="govuk-tag govuk-phase-banner__content__tag",
                ),
                fh.Span(
                    *content,
                    cls="govuk-phase-banner__text",
                ),
                cls="govuk-phase-banner__content",
            ),
            cls="govuk-phase-banner",
        ),
        cls="govuk-width-container",
        **kwargs,
    )


def Page(*content, navigation=None, sidebar=None) -> fh.FT:
    """
    A standard `GOV.UK Page`_ component with a GOV.UK Header, a GOV.UK Phase Banner,
    a GOV.UK Footer and - whatever content you might want to add to it.

    The Phase Banner and the Footer are loaded from `/phase` and `/footer` endpoints
    respectively using `htmx-get` directives.

    This is to ensure that there is one and only one definition of a Phase Banner
    and a Footer in your codebase.

    Examples:

        >>> ds.Page("Hello World!")
        # Renders a page with GOV.UK Header and the text "Hello World!"
        # Footer and Phase Banner are loaded dynamically
        >>> ds.Page(ds.H1("Hello World!"))
        # Renders a page with the heading - "Hello World!"
        >>> nav = ds.Navigation("/", "/feedback")
        >>> ds.Page(navigation=nav)
        # Renders a page with the given service navigation component
        >>> ds.Page(sidebar="Hello World!")
        # Renders a page with a sidebar that contains the text - "Hello World!"

    Args:
        *content: List of content for the Page.
        navigation (optional): Navigation component. Defaults to None.
        sidebar (optional): Sidebar content. Defaults to None.

    Returns:
        FT: A FastHTML Page component.

    .. _GOV.UK Page: https://design-system.service.gov.uk/styles/page-template/
    """
    return fh.Body(
        fh.Script(
            "document.body.className += ' js-enabled' + ('noModule' in HTMLScriptElement.prototype ? ' govuk-frontend-supported' : '');",
        ),
        # Cookie banner until the user hides it
        fh.Div(hx_get="/cookie-banner", hx_trigger="load"),
        Header("Fast GOV.UK", "/"),
        # Navigation
        navigation,
        # Phase banner
        fh.Div(hx_get="/phase", hx_trigger="load"),
        fh.Div(
            fh.Main(
                fh.Div(
                    fh.Div(
                        # Every page will check if there are any notifications
                        fh.Div(hx_get="/notifications", hx_trigger="load"),
                        *content,
                        cls="govuk-grid-column-two-thirds",
                    ),
                    fh.Div(*sidebar or [], cls="govuk-grid-column-one-thirds"),
                    cls="govuk-grid-row",
                ),
                cls="govuk-main-wrapper",
            ),
            cls="govuk-width-container",
        ),
        # Get central service footer
        fh.Div(hx_get="/footer", hx_trigger="load"),
        fh.Script(src="/govuk-frontend-5.11.1.min.js", type="module"),
        fh.Script(
            "import {initAll} from '/govuk-frontend-5.11.1.min.js'; initAll();",
            type="module",
        ),
    )


def Cookies(*content: fh.FT):
    """
    A standard `GOV.UK Cookie Page`_ component that includes definition of cookies and
    a table detailing the 2 essential cookies used by fast-gov-uk services.

    Examples:

        >>> ds.Cookies()
        # Render the Cookies page
        >>> ds.Cookies(ds.H2("Additional Cookies"), ...)
        # Renders the Cookies page with additional cookies

    This is just the component. You would probably want to render the Cookies
    page at the `/cookies` URL. You can do so by adding the following function
    to your `app.py`:

    .. code-block:: python

        @fast.page
        def cookies():
            return ds.Cookies()

    Args:
        *content (FT): List of content for the Page.

    Returns:
        FT: A FastHTML Cookies page component.

    .. _GOV.UK Cookie Page: https://design-system.service.gov.uk/patterns/cookies-page/
    """
    return Page(
        H1("Cookies"),
        P("Cookies are small files saved on your phone, tablet or computer when you visit a website."),
        P("We use cookies to make this site work and collect information about how you use our service."),
        H2("Essential Cookies"),
        P("Essential cookies keep your information secure while you use this service. We do not need to ask permission to use them."),
        Table(
            data=[
                {"name": "session_cookie", "purpose": "Used to store your settings and progress", "expires": "1 day"},
                {"name": "cookie_policy", "purpose": "Saves your cookie consent settings", "expires": "1 year"},
            ],
            caption="Essential cookies we use",
        ),
        *content,
    )
