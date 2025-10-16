import pytest

import fast_gov_uk.design_system as ds
from fast_gov_uk.design_system import OGL, Crown, Logo


@pytest.mark.parametrize(
    "args, expected",
    (
        (
            ["Test", "/test"],
            (
                '<header data-module="govuk-header" class="govuk-header">'
                    '<div class="govuk-header__container govuk-width-container">'
                        '<div class="govuk-header__logo">'
                            '<a href="/test" aria-label="Home" class="govuk-header__link govuk-header__link--homepage">'
                                f"{Logo()}"
                                '<span class="govuk-header__product-name">Test</span>'
                            "</a>"
                        "</div>"
                    "</div>"
                "</header>"
            ),
        ),
    ),
)
def test_header(args, expected):
    """Test Header with various parameters.
    Args:
        args (list): The FooterLinks to pass to Header.
        expected (str): The expected HTML output.
    """
    header = ds.Header(*args)
    assert str(header) == expected


@pytest.mark.parametrize(
    "args, expected",
    (
        (
            [],
            (
                '<footer class="govuk-footer">'
                    '<div class="govuk-width-container">'
                        f"{Crown()}"
                        '<div class="govuk-footer__meta">'
                            '<div class="govuk-footer__meta-item govuk-footer__meta-item--grow">'
                                f"{OGL()}"
                                '<span class="govuk-footer__licence-description">'
                                    "All content is available under the"
                                    '<a href="https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/" rel="license" class="govuk-footer__link">'
                                        "Open Government Licence v3.0"
                                    "</a>"
                                "</span>"
                            "</div>"
                            '<div class="govuk-footer__meta-item">'
                                '<a href="https://www.nationalarchives.gov.uk/information-management/re-using-public-sector-information/uk-government-licensing-framework/crown-copyright/" class="govuk-footer__link govuk-footer__copyright-logo">'
                                    "© Crown copyright"
                                "</a>"
                            "</div>"
                        "</div>"
                    "</div>"
                "</footer>"
            ),
        ),
        (
            [("Test Link", "/test")],
            (
                '<footer class="govuk-footer">'
                    '<div class="govuk-width-container">'
                        f"{Crown()}"
                        '<div class="govuk-footer__meta">'
                            '<div class="govuk-footer__meta-item govuk-footer__meta-item--grow">'
                                '<h2 class="govuk-visually-hidden">Support links</h2>'
                                '<ul class="govuk-footer__inline-list">'
                                    '<li class="govuk-footer__inline-list-item">'
                                        '<a href="/test" class="govuk-footer__link">Test Link</a>'
                                    "</li>"
                                "</ul>"
                                f"{OGL()}"
                                '<span class="govuk-footer__licence-description">'
                                    "All content is available under the"
                                    '<a href="https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/" rel="license" class="govuk-footer__link">'
                                        "Open Government Licence v3.0"
                                    "</a>"
                                "</span>"
                            "</div>"
                            '<div class="govuk-footer__meta-item">'
                                '<a href="https://www.nationalarchives.gov.uk/information-management/re-using-public-sector-information/uk-government-licensing-framework/crown-copyright/" class="govuk-footer__link govuk-footer__copyright-logo">'
                                    "© Crown copyright"
                                "</a>"
                            "</div>"
                        "</div>"
                    "</div>"
                "</footer>"
            ),
        ),
    ),
)
def test_footer(args, expected):
    """Test Footer with various parameters.
    Args:
        args (list): The FooterLinks to pass to Footer.
        expected (str): The expected HTML output.
    """
    footer = ds.Footer(*args)
    assert str(footer) == expected


@pytest.mark.parametrize(
    "kwargs, expected",
    (
        (
            {"content": [ds.P("Test Content")]},
            (
                '<div class="govuk-width-container">'
                    '<div class="govuk-phase-banner">'
                        '<p class="govuk-phase-banner__content">'
                            '<strong class="govuk-tag govuk-phase-banner__content__tag">Alpha</strong>'
                            '<span class="govuk-phase-banner__text">'
                                '<p class="govuk-body">Test Content</p>'
                            '</span>'
                        "</p>"
                    "</div>"
                "</div>"
            ),
        ),
        (
            {"phase": "Beta", "content": [ds.P("Test Content")]},
            (
                '<div class="govuk-width-container">'
                    '<div class="govuk-phase-banner">'
                        '<p class="govuk-phase-banner__content">'
                            '<strong class="govuk-tag govuk-phase-banner__content__tag">Beta</strong>'
                            '<span class="govuk-phase-banner__text">'
                                '<p class="govuk-body">Test Content</p>'
                            '</span>'
                        "</p>"
                    "</div>"
                "</div>"
            ),
        ),
        (
            {"content": [ds.A("Test Link")]},
            (
                '<div class="govuk-width-container">'
                    '<div class="govuk-phase-banner">'
                        '<p class="govuk-phase-banner__content">'
                            '<strong class="govuk-tag govuk-phase-banner__content__tag">Alpha</strong>'
                            '<span class="govuk-phase-banner__text">'
                                '<a href="#" class="govuk-link">Test Link</a>'
                            "</span>"
                        "</p>"
                    "</div>"
                "</div>"
            ),
        ),
        (
            {"content": [ds.A("Test Link"), ds.P("Test Content")]},
            (
                '<div class="govuk-width-container">'
                    '<div class="govuk-phase-banner">'
                        '<p class="govuk-phase-banner__content">'
                            '<strong class="govuk-tag govuk-phase-banner__content__tag">Alpha</strong>'
                            '<span class="govuk-phase-banner__text">'
                                '<a href="#" class="govuk-link">Test Link</a>'
                                '<p class="govuk-body">Test Content</p>'
                            "</span>"
                        "</p>"
                    "</div>"
                "</div>"
            ),
        ),
    ),
)
def test_phase_banner(kwargs, expected):
    """Test PhaseBanner with various parameters.
    Args:
        kwargs (dict): The arguments to pass to PhaseBanner.
        expected (str): The expected HTML output.
    """
    content = kwargs.pop("content")
    banner = ds.PhaseBanner(*content, **kwargs)
    assert str(banner) == expected


@pytest.mark.parametrize("component", (
    ds.Header("test", "/", hx_test="foo"),
    ds.Footer(hx_test="foo"),
    ds.PhaseBanner(hx_test="foo"),
))
def test_html_attribute(component, html):
    """
    Test that passes an html attribute to components - that is not
    explicitly handled but should be passed through to the
    underlying FT.
    """
    assert 'hx-test="foo"' in html(component)
