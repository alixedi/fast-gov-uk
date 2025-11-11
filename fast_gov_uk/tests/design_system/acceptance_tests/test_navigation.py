import fast_gov_uk.design_system as ds


def test_backlink(html):
    """
    Link: https://design-system.service.gov.uk/components/back-link/
    """
    backlink = ds.BackLink("#")
    assert html(backlink) == html(
        '<a href="#" class="govuk-back-link">' \
            'Back'
        '</a>'
    )


def test_backlink_dark(html):
    """
    Link: https://design-system.service.gov.uk/components/back-link/
    """
    backlink = ds.BackLink("#", inverse=True)
    assert html(backlink) == html(
        '<a href="#" class="govuk-back-link govuk-back-link--inverse">'
            'Back'
        '</a>'
    )


def test_skiplink(html):
    """
    Link: https://design-system.service.gov.uk/components/skip-link/
    """
    skiplink = ds.SkipLink("#")
    assert html(skiplink) == html(
        '<a href="#" class="govuk-skip-link" data-module="govuk-skip-link">'
            'Skip to main content'
        '</a>'
    )


def test_breadcrumbs(html):
    """
    Link: https://design-system.service.gov.uk/components/breadcrumbs/
    """
    breadcrumbs = ds.Breadcrumbs(
        ("Home", "#"),
        ("Passports, travel and living abroad", "#"),
        ("Travel abroad", "#"),
    )
    assert html(breadcrumbs) == html(
        '<nav class="govuk-breadcrumbs" aria-label="Breadcrumb">'
        '<ol class="govuk-breadcrumbs__list">'
            '<li class="govuk-breadcrumbs__list-item">'
                '<a class="govuk-breadcrumbs__link" href="#">Home</a>'
            '</li>'
            '<li class="govuk-breadcrumbs__list-item">'
                '<a class="govuk-breadcrumbs__link" href="#">Passports, travel and living abroad</a>'
            '</li>'
            '<li class="govuk-breadcrumbs__list-item">'
                '<a class="govuk-breadcrumbs__link" href="#">Travel abroad</a>'
            '</li>'
        '</ol>'
        '</nav>'
    )


def test_breadcrumbs_collpse(html):
    """
    Link: https://design-system.service.gov.uk/components/breadcrumbs/
    """
    breadcrumbs = ds.Breadcrumbs(
        ("Home", "#"),
        ("Environment", "#"),
        ("Rural and countryside", "#"),
        ("Rural development and land management", "#"),
        ("Economic growth in rural areas", "#"),
        collapse_on_mobile=True,
    )
    assert html(breadcrumbs) == html(
        '<nav class="govuk-breadcrumbs govuk-breadcrumbs--collapse-on-mobile" aria-label="Breadcrumb">'
        '<ol class="govuk-breadcrumbs__list">'
            '<li class="govuk-breadcrumbs__list-item">'
                '<a class="govuk-breadcrumbs__link" href="#">Home</a>'
            '</li>'
            '<li class="govuk-breadcrumbs__list-item">'
                '<a class="govuk-breadcrumbs__link" href="#">Environment</a>'
            '</li>'
            '<li class="govuk-breadcrumbs__list-item">'
                '<a class="govuk-breadcrumbs__link" href="#">Rural and countryside</a>'
            '</li>'
            '<li class="govuk-breadcrumbs__list-item">'
                '<a class="govuk-breadcrumbs__link" href="#">Rural development and land management</a>'
            '</li>'
            '<li class="govuk-breadcrumbs__list-item">'
                '<a class="govuk-breadcrumbs__link" href="#">Economic growth in rural areas</a>'
            '</li>'
        '</ol>'
        '</nav>'
    )


def test_exit_page(html):
    """
    Link: https://design-system.service.gov.uk/components/exit-this-page/
    """
    exit_page = ds.ExitPage()
    assert html(exit_page) == html(
        '<div class="govuk-exit-this-page" data-module="govuk-exit-this-page">'
        '<a href="https://www.bbc.co.uk/weather" role="button" draggable="false" class="govuk-button govuk-button--warning govuk-exit-this-page__button govuk-js-exit-this-page-button" data-module="govuk-button" rel="nofollow noreferrer">'
            '<span class="govuk-visually-hidden">Emergency</span> Exit this page'
        '</a>'
        '</div>'
    )


def test_navigation(html):
    """
    Link: https://design-system.service.gov.uk/components/service-navigation/
    """
    navigation = ds.Navigation(
        ds.NavigationLink("Navigation item 1", "#"),
        ds.NavigationLink("Navigation item 2", "#", active=True),
        ds.NavigationLink("Navigation item 3", "#"),
        service_name="Service name",
    )
    assert html(navigation) == html(
        '<section aria-label="Service information" class="govuk-service-navigation"'
        'data-module="govuk-service-navigation">'
        '<div class="govuk-width-container">'
            '<div class="govuk-service-navigation__container">'
            '<span class="govuk-service-navigation__service-name">'
                # '<a href="#" class="govuk-service-navigation__link">Service name</a>'
                # The spec had href for service link that was "#" instead of the root
                '<a href="/" class="govuk-service-navigation__link">Service name</a>'
            '</span>'
            '<nav aria-label="Menu" class="govuk-service-navigation__wrapper">'
                '<button type="button" class="govuk-service-navigation__toggle govuk-js-service-navigation-toggle" aria-controls="navigation" hidden>'
                'Menu'
                '</button>'
                '<ul class="govuk-service-navigation__list" id="navigation">'
                '<li class="govuk-service-navigation__item">'
                    '<a class="govuk-service-navigation__link" href="#">Navigation item 1</a>'
                '</li>'
                '<li class="govuk-service-navigation__item govuk-service-navigation__item--active">'
                    '<a class="govuk-service-navigation__link" href="#" aria-current="true">'
                        '<strong class="govuk-service-navigation__active-fallback">Navigation item 2</strong>'
                    '</a>'
                '</li>'
                '<li class="govuk-service-navigation__item">'
                    '<a class="govuk-service-navigation__link" href="#">Navigation item 3</a>'
                '</li>'
                '</ul>'
            '</nav>'
            '</div>'
        '</div>'
        '</section>'
    )


def test_pagination(html):
    """
    Link: https://design-system.service.gov.uk/components/pagination/
    """
    pagination = ds.Pagination(
        ds.PaginationLink("1", "#"),
        ds.PaginationLink("2", "#", active=True),
        ds.PaginationLink("3", "#"),
        prev_link="#",
        next_link="#",
    )
    assert html(pagination) == html(
        '<nav class="govuk-pagination" aria-label="Pagination">'
            '<div class="govuk-pagination__prev">'
                '<a class="govuk-link govuk-pagination__link" href="#" rel="prev">'
                    '<svg class="govuk-pagination__icon govuk-pagination__icon--prev" xmlns="http://www.w3.org/2000/svg" height="13" width="15" aria-hidden="true" focusable="false" viewBox="0 0 15 13">'
                        '<path d="m6.5938-0.0078125-6.7266 6.7266 6.7441 6.4062 1.377-1.449-4.1856-3.9768h12.896v-2h-12.984l4.2931-4.293-1.414-1.414z"></path>'
                    '</svg>'
                    '<span class="govuk-pagination__link-title">'
                        'Previous<span class="govuk-visually-hidden"> page</span>'
                    '</span>'
                '</a>'
            '</div>'
            '<ul class="govuk-pagination__list">'
                '<li class="govuk-pagination__item">'
                    '<a class="govuk-link govuk-pagination__link" href="#" aria-label="Page 1">1</a>'
                '</li>'
                '<li class="govuk-pagination__item govuk-pagination__item--current">'
                    '<a class="govuk-link govuk-pagination__link" href="#" aria-label="Page 2" aria-current="page">2</a>'
                '</li>'
                '<li class="govuk-pagination__item">'
                    '<a class="govuk-link govuk-pagination__link" href="#" aria-label="Page 3">3</a>'
                '</li>'
            '</ul>'
            '<div class="govuk-pagination__next">'
                '<a class="govuk-link govuk-pagination__link" href="#" rel="next">'
                    '<span class="govuk-pagination__link-title">'
                        'Next<span class="govuk-visually-hidden"> page</span>'
                    '</span>'
                    '<svg class="govuk-pagination__icon govuk-pagination__icon--next" xmlns="http://www.w3.org/2000/svg" height="13" width="15" aria-hidden="true" focusable="false" viewBox="0 0 15 13">'
                        '<path d="m8.107-0.0078125-1.4136 1.414 4.2926 4.293h-12.986v2h12.896l-4.1855 3.9766 1.377 1.4492 6.7441-6.4062-6.7246-6.7266z"></path>'
                    '</svg>'
                '</a>'
            '</div>'
        '</nav>'
    )


def test_pagination_block(html):
    """
    Link: https://design-system.service.gov.uk/components/pagination/
    """
    pagination = ds.PaginationBlock(
        ("Applying for a provisional lorry or bus licence", "#"),
        ("Driver CPC part 1 test: theory", "#"),
    )
    assert html(pagination) == html(
        '<nav class="govuk-pagination govuk-pagination--block" aria-label="Pagination">'
            '<div class="govuk-pagination__prev">'
                '<a class="govuk-link govuk-pagination__link" href="#" rel="prev">'
                    '<svg class="govuk-pagination__icon govuk-pagination__icon--prev" xmlns="http://www.w3.org/2000/svg" height="13" width="15" aria-hidden="true" focusable="false" viewBox="0 0 15 13">'
                        '<path d="m6.5938-0.0078125-6.7266 6.7266 6.7441 6.4062 1.377-1.449-4.1856-3.9768h12.896v-2h-12.984l4.2931-4.293-1.414-1.414z"></path>'
                    '</svg>'
                    '<span class="govuk-pagination__link-title">'
                        'Previous<span class="govuk-visually-hidden"> page</span>'
                    '</span>'
                    '<span class="govuk-visually-hidden">:</span>'
                    '<span class="govuk-pagination__link-label">Applying for a provisional lorry or bus licence</span>'
                '</a>'
            '</div>'
            '<div class="govuk-pagination__next">'
                '<a class="govuk-link govuk-pagination__link" href="#" rel="next">'
                    '<svg class="govuk-pagination__icon govuk-pagination__icon--next" xmlns="http://www.w3.org/2000/svg" height="13" width="15" aria-hidden="true" focusable="false" viewBox="0 0 15 13">'
                        '<path d="m8.107-0.0078125-1.4136 1.414 4.2926 4.293h-12.986v2h12.896l-4.1855 3.9766 1.377 1.4492 6.7441-6.4062-6.7246-6.7266z"></path>'
                    '</svg>'
                    '<span class="govuk-pagination__link-title">'
                        'Next<span class="govuk-visually-hidden"> page</span>'
                    '</span>'
                    '<span class="govuk-visually-hidden">:</span>'
                    '<span class="govuk-pagination__link-label">Driver CPC part 1 test: theory</span>'
                '</a>'
            '</div>'
        '</nav>'
    )
