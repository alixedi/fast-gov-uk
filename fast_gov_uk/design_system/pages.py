import fasthtml.common as fh

from .components import Table
from .inputs import Field
from .typography import H1, H2, P
from .utils import OGL, Crown, Logo


def Header(title: str, homepage: str) -> fh.FT:
    """
    Header component.
    Args:
        title (str): The title of the header.
        homepage (str): The URL of the homepage.
    Returns:
        FT: A FastHTML Header component.
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
    )


def FooterLink(
    text: str,
    href: str,
) -> fh.FT:
    """
    Footer link component.
    Args:
        text (str): The text to display in the link.
        href (str): The URL the link points to. Defaults to "#".
    Returns:
        FT: A FastHTML FooterLink component.
    """
    return fh.A(
        text,
        href=href,
        cls="govuk-footer__link",
    )


def Footer(*links: tuple[str, str]) -> fh.FT:
    """
    Footer component.
    Args:
        links (tuples with text and href): Footer links.
    Returns:
        FT: A FastHTML Footer component.
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
    )


def PhaseBanner(
    *content: fh.FT,
    phase: str = "Alpha",
) -> fh.FT:
    """
    Phase banner component.
    Args:
        content (FT): The content to display in the phase banner.
        phase (str): The phase of the project. Defaults to "alpha".
    Returns:
        FT: A FastHTML PhaseBanner component.
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
    )


def Page(*content: fh.FT | Field) -> fh.FT:
    """
    Page component.
    Args:
        content (list): List of content for the Page.
    Returns:
        FT: A FastHTML Page component.
    """
    return fh.Body(
        fh.Script(
            "document.body.className += ' js-enabled' + ('noModule' in HTMLScriptElement.prototype ? ' govuk-frontend-supported' : '');",
        ),
        # Every page will have a cookie banner until the user hides it
        fh.Div(hx_get="/cookie-banner", hx_trigger="load"),
        Header("Fast GOV.UK", "/"),
        fh.Div(hx_get="/phase", hx_trigger="load"),
        fh.Div(
            fh.Main(
                fh.Div(
                    fh.Div(
                        *content,
                        cls="govuk-grid-column-two-thirds",
                    ),
                    cls="govuk-grid-row",
                ),
                cls="govuk-main-wrapper",
            ),
            cls="govuk-width-container",
        ),
        Footer(),
        fh.Script(src="/govuk-frontend-5.11.1.min.js", type="module"),
        fh.Script(
            "import {initAll} from '/govuk-frontend-5.11.1.min.js'; initAll();",
            type="module",
        ),
    )


def Cookies(*content: fh.FT):
    """
    Cookie page component.
    Args:
        content (list): List of content for the Page.
    Returns:
        FT: A FastHTML Cookies page component.

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
