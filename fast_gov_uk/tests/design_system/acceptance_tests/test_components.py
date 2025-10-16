import fasthtml.common as fh

import fast_gov_uk.design_system as ds


def test_inset(html):
    """
    Link: https://design-system.service.gov.uk/components/inset-text/
    """
    inset = ds.Inset((
        "It can take up to 8 weeks to register a lasting power "
        "of attorney if there are no mistakes in the application."
    ))
    assert html(inset) == html(
        '<div class="govuk-inset-text">'
            "It can take up to 8 weeks to register a lasting power "
            "of attorney if there are no mistakes in the application."
        "</div>"
    )


def test_detail(html):
    """
    Link: https://design-system.service.gov.uk/components/details/
    """
    detail = ds.Detail(
        "Help with nationality",
        # The text has the character: "'" which is escaped automatically
        # by FastHTML to protect against XSS attacks. As a result, we
        # need to explicitly mark this as Safe. In real world, Safe means
        # that this text is not (a) being submitted in a form by a user
        # (b) saved into the DB and then (c) loaded and rendered here.
        ds.Safe(
            "We need to know your nationality so we can work out which "
            "elections you're entitled to vote in. If you cannot provide "
            "your nationality, you'll have to send copies of identity "
            "documents through the post."
        ),
    )
    assert html(detail) == html(
        '<details class="govuk-details">'
            '<summary class="govuk-details__summary">'
                '<span class="govuk-details__summary-text">'
                    "Help with nationality"
                "</span>"
            "</summary>"
            '<div class="govuk-details__text">'
                "We need to know your nationality so we can work out which "
                "elections you're entitled to vote in. If you cannot provide "
                "your nationality, you'll have to send copies of identity "
                "documents through the post."
            "</div>"
        "</details>"
    )


def test_panel(html):
    """
    Link: https://design-system.service.gov.uk/components/panel/
    """
    panel = ds.Panel(
        ds.Safe("Your reference number<br><strong>HDJ2123F</strong>"),
        title="Application complete",
    )
    assert html(panel) == html(
        '<div class="govuk-panel govuk-panel--confirmation">'
            '<h1 class="govuk-panel__title">'
                "Application complete"
            "</h1>"
            '<div class="govuk-panel__body">'
                "Your reference number<br><strong>HDJ2123F</strong>"
            "</div>"
        "</div>"
    )


def test_tag(html):
    """
    Link: https://design-system.service.gov.uk/components/tag/

    The following is a simplification of the table of tags titled
    "Using colour with tags" b/c I don't want to pollute this with
    all the <table> stuff.
    """
    tags = ds.Div(
        ds.Tag("Inactive", color="grey"),
        ds.Tag("New", color="green"),
        ds.Tag("Active", color="turquoise"),
        ds.Tag("Pending", color="blue"),
        ds.Tag("In progress", color="light-blue"),
        ds.Tag("Received", color="purple"),
        ds.Tag("Sent", color="pink"),
        ds.Tag("Rejected", color="red"),
        ds.Tag("Declined", color="orange"),
        ds.Tag("Delayed", color="yellow"),
    )
    assert html(tags) == html(
        "<div>"
            '<strong class="govuk-tag govuk-tag--grey">Inactive</strong>'
            '<strong class="govuk-tag govuk-tag--green">New</strong>'
            '<strong class="govuk-tag govuk-tag--turquoise">Active</strong>'
            '<strong class="govuk-tag govuk-tag--blue">Pending</strong>'
            '<strong class="govuk-tag govuk-tag--light-blue">In progress</strong>'
            '<strong class="govuk-tag govuk-tag--purple">Received</strong>'
            '<strong class="govuk-tag govuk-tag--pink">Sent</strong>'
            '<strong class="govuk-tag govuk-tag--red">Rejected</strong>'
            '<strong class="govuk-tag govuk-tag--orange">Declined</strong>'
            '<strong class="govuk-tag govuk-tag--yellow">Delayed</strong>'
        "</div>"
    )


def test_warning(html):
    """
    Link: https://design-system.service.gov.uk/components/warning-text/
    """
    warning = ds.Warning("You can be fined up to £5,000 if you do not register.")
    assert html(warning) == html(
        '<div class="govuk-warning-text">'
            '<span class="govuk-warning-text__icon" aria-hidden="true">!</span>'
            '<strong class="govuk-warning-text__text">'
                '<span class="govuk-visually-hidden">Warning</span>'
                "You can be fined up to £5,000 if you do not register."
            "</strong>"
        "</div>"
    )


def test_notification(html):
    """
    Link: https://design-system.service.gov.uk/components/notification-banner/
    """
    notificaton = ds.Notification(
        ds.NotificatonHeading(
            "You have 7 days left to send your application.",
            ds.NotificatonLink("View application", "#"),
            ".",
        ),
    )
    assert html(notificaton) == html(
        # '<div class="govuk-notification-banner" role="region" aria-labelledby="govuk-notification-banner-title" data-module="govuk-notification-banner">'
        # The spec is inconsistent b/c I think the role should be "alert" b/c
        # Its a notification and not just another banner -
        '<div class="govuk-notification-banner" role="alert" aria-labelledby="govuk-notification-banner-title" data-module="govuk-notification-banner">'
            '<div class="govuk-notification-banner__header">'
                '<h2 class="govuk-notification-banner__title" id="govuk-notification-banner-title">'
                    "Important"
                "</h2>"
            "</div>"
            '<div class="govuk-notification-banner__content">'
                '<p class="govuk-notification-banner__heading">'
                    "You have 7 days left to send your application."
                    '<a class="govuk-notification-banner__link" href="#">View application</a>.'
                "</p>"
            "</div>"
        "</div>"
    )


def test_notification_success(html):
    """
    Link: https://design-system.service.gov.uk/components/notification-banner/
    """
    notificaton = ds.Notification(
        ds.NotificatonHeading(
            "Training outcome recorded and trainee withdrawn",
        ),
        ds.P(
            "Contact ",
            ds.NotificatonLink("example@department.gov.uk", "#"),
            " if you think there's a problem."
        ),
        title="Success",
        success=True,
    )
    assert html(notificaton) == html(
        '<div class="govuk-notification-banner govuk-notification-banner--success" role="alert" aria-labelledby="govuk-notification-banner-title" data-module="govuk-notification-banner">'
            '<div class="govuk-notification-banner__header">'
                '<h2 class="govuk-notification-banner__title" id="govuk-notification-banner-title">'
                    "Success"
                "</h2>"
            "</div>"
            '<div class="govuk-notification-banner__content">'
                # '<h3 class="govuk-notification-banner__heading">'
                # In the spec, its h3 but I think its inconsistent
                # with the rest of the specs where its p -
                '<p class="govuk-notification-banner__heading">'
                    "Training outcome recorded and trainee withdrawn"
                "</p>"
                '<p class="govuk-body">'
                    'Contact '
                    '<a class="govuk-notification-banner__link" href="#">example@department.gov.uk</a> '
                    "if you think there's a problem."
                "</p>"
            "</div>"
        "</div>"
    )


def test_accordion(html):
    """
    Link: https://design-system.service.gov.uk/components/accordion/

    I am doing to test the most comprehensice spec - an accordion with
    with section summaries and links in the content.

    I have kept 2 sections and a couple of links each to be concise.
    """
    # The div is important b/c it seems if the top level component in
    # FastHTML has an "id" attribute, str(component) returns the id
    # instead of the rendered html of the component.
    accordion = ds.Div(
        ds.Accordion(
            {
                "heading": "Understanding agile project management",
                "summary": "Introductions, methods, core features.",
                "content": ds.Ul(
                    ds.Li(ds.A("Agile and government services: an introduction")),
                    ds.Li(ds.A("Agile methods: an introduction")),
                ),
            },
            {
                "heading": "Working with agile methods",
                "summary": "Workspaces, tools and techniques, user stories, planning.",
                "content": ds.Ul(
                    ds.Li(ds.A("Creating an agile working environment")),
                    ds.Li(ds.A("Agile tools and techniques")),
                ),
            },
            accordion_id="accordion-with-summary-sections",
        )
    )
    assert html(accordion) == html(
        '<div>'
            '<div class="govuk-accordion" data-module="govuk-accordion">'
                '<div class="govuk-accordion__section">'
                    '<div class="govuk-accordion__section-header">'
                        '<h2 class="govuk-accordion__section-heading">'
                            '<span class="govuk-accordion__section-button" id="accordion-with-summary-sections-heading-1">'
                                'Understanding agile project management'
                            '</span>'
                        '</h2>'
                        '<div class="govuk-accordion__section-summary govuk-body" id="accordion-with-summary-sections-summary-1">'
                                'Introductions, methods, core features.'
                        '</div>'
                    '</div>'
                    '<div id="accordion-with-summary-sections-content-1" class="govuk-accordion__section-content">'
                        '<ul class="govuk-list">'
                            '<li>'
                                '<a class="govuk-link" href="#">Agile and government services: an introduction</a>'
                            '</li>'
                            '<li>'
                                '<a class="govuk-link" href="#">Agile methods: an introduction</a>'
                            '</li>'
                        '</ul>'
                    '</div>'
                '</div>'
                '<div class="govuk-accordion__section">'
                    '<div class="govuk-accordion__section-header">'
                        '<h2 class="govuk-accordion__section-heading">'
                            '<span class="govuk-accordion__section-button" id="accordion-with-summary-sections-heading-2">'
                                'Working with agile methods'
                            '</span>'
                        '</h2>'
                        '<div class="govuk-accordion__section-summary govuk-body" id="accordion-with-summary-sections-summary-2">'
                            'Workspaces, tools and techniques, user stories, planning.'
                        '</div>'
                    '</div>'
                    '<div id="accordion-with-summary-sections-content-2" class="govuk-accordion__section-content">'
                        '<ul class="govuk-list">'
                            '<li>'
                                '<a class="govuk-link" href="#">Creating an agile working environment</a>'
                            '</li>'
                            '<li>'
                                '<a class="govuk-link" href="#">Agile tools and techniques</a>'
                            '</li>'
                        '</ul>'
                    '</div>'
                '</div>'
            '</div>'
        '</div>'
    )


def test_tab(html):
    """
    Link: https://design-system.service.gov.uk/components/tabs/

    To simplify, I have removed the tables from tab contents and
    replaced them with paras.
    """
    tab = ds.Tab(
        {"heading": "Past day", "content": ds.P("Content from past day")},
        {"heading": "Past week", "content": ds.P("Content from past week")},
        {"heading": "Past month", "content": ds.P("Content from past month")},
        {"heading": "Past year", "content": ds.P("Content from past year")},
        title="Contents",
    )
    assert html(tab) == html(
        '<div class="govuk-tabs" data-module="govuk-tabs">'
            '<h2 class="govuk-tabs__title">'
                'Contents'
            '</h2>'
            '<ul class="govuk-tabs__list">'
                '<li class="govuk-tabs__list-item govuk-tabs__list-item--selected">'
                '<a class="govuk-tabs__tab" href="#past-day">'
                    'Past day'
                '</a>'
                '</li>'
                '<li class="govuk-tabs__list-item">'
                '<a class="govuk-tabs__tab" href="#past-week">'
                    'Past week'
                '</a>'
                '</li>'
                '<li class="govuk-tabs__list-item">'
                '<a class="govuk-tabs__tab" href="#past-month">'
                    'Past month'
                '</a>'
                '</li>'
                '<li class="govuk-tabs__list-item">'
                '<a class="govuk-tabs__tab" href="#past-year">'
                    'Past year'
                '</a>'
                '</li>'
            '</ul>'
            '<div class="govuk-tabs__panel" id="past-day">'
                '<h2 class="govuk-heading-l">Past day</h2>'
                '<p class="govuk-body" class="govuk-body">Content from past day</p>'
            '</div>'
            '<div class="govuk-tabs__panel govuk-tabs__panel--hidden" id="past-week">'
                '<h2 class="govuk-heading-l">Past week</h2>'
                '<p class="govuk-body">Content from past week</p>'
            '</div>'
            '<div class="govuk-tabs__panel govuk-tabs__panel--hidden" id="past-month">'
                '<h2 class="govuk-heading-l">Past month</h2>'
                '<p class="govuk-body">Content from past month</p>'
            '</div>'
            '<div class="govuk-tabs__panel govuk-tabs__panel--hidden" id="past-year">'
                '<h2 class="govuk-heading-l">Past year</h2>'
                '<p class="govuk-body">Content from past year</p>'
            '</div>'
        '</div>'
    )


def test_error_summary(html):
    """
    Link: https://design-system.service.gov.uk/components/error-summary/
    """
    err = ds.ErrorSummary(
        "There is a problem",
        # Using FastHTML links here b/c these links in the spec
        # don't have the govuk-link class
        fh.A("Enter your full name"),
        fh.A("The date your passport was issued must be in the past"),
    )
    assert html(err) == html(
        '<div class="govuk-error-summary" data-module="govuk-error-summary">'
            '<div role="alert">'
                '<h2 class="govuk-error-summary__title">There is a problem</h2>'
                '<div class="govuk-error-summary__body">'
                    '<ul class="govuk-list govuk-error-summary__list">'
                        '<li><a href="#">Enter your full name</a></li>'
                        '<li><a href="#">The date your passport was issued must be in the past</a></li>'
                    '</ul>'
                '</div>'
            '</div>'
        '</div>'
    )


def test_table(html):
    """
    Link: https://design-system.service.gov.uk/components/table/

    This takes the first example on the link above. It also covers
    table captions and table headers.
    """
    table = ds.Table(
        data=[
            {"Date": "First 6 weeks", "Amount": "£109.80 per week"},
            {"Date": "Next 33 weeks", "Amount": "£109.80 per week"},
            {"Date": "Total estimated pay", "Amount": "£4,282.20"},
        ],
        caption="Dates and amounts",
        header_cols=["Date"],
    )
    assert html(table) == html(
        '<table class="govuk-table">'
            '<caption class="govuk-table__caption govuk-table__caption--m">Dates and amounts</caption>'
            '<thead class="govuk-table__head">'
                '<tr class="govuk-table__row">'
                    '<th scope="col" class="govuk-table__header">Date</th>'
                    '<th scope="col" class="govuk-table__header">Amount</th>'
                '</tr>'
            '</thead>'
            '<tbody class="govuk-table__body">'
                '<tr class="govuk-table__row">'
                    '<th scope="row" class="govuk-table__header">First 6 weeks</th>'
                    '<td class="govuk-table__cell">£109.80 per week</td>'
                '</tr>'
                '<tr class="govuk-table__row">'
                    '<th scope="row" class="govuk-table__header">Next 33 weeks</th>'
                    '<td class="govuk-table__cell">£109.80 per week</td>'
                '</tr>'
                '<tr class="govuk-table__row">'
                    '<th scope="row" class="govuk-table__header">Total estimated pay</th>'
                    '<td class="govuk-table__cell">£4,282.20</td>'
                '</tr>'
            '</tbody>'
        '</table>'
    )


def test_table_numeric(html):
    """
    Link: https://design-system.service.gov.uk/components/table/

    This if for Numbers in a table example.
    """
    table = ds.Table(
        data=[
            {"Month you apply": "January", "Rate for bicycles": "£85", "Rate for vehicles": "£95"},
            {"Month you apply": "February", "Rate for bicycles": "£75", "Rate for vehicles": "£55"},
            {"Month you apply": "March", "Rate for bicycles": "£165", "Rate for vehicles": "£125"},
        ],
        caption="Months and rates",
        header_cols=["Month you apply"],
        numeric_cols=["Rate for bicycles", "Rate for vehicles"],
    )
    assert html(table) == html(
        '<table class="govuk-table">'
            '<caption class="govuk-table__caption govuk-table__caption--m">Months and rates</caption>'
            '<thead class="govuk-table__head">'
                '<tr class="govuk-table__row">'
                    '<th scope="col" class="govuk-table__header">Month you apply</th>'
                    '<th scope="col" class="govuk-table__header govuk-table__header--numeric">Rate for bicycles</th>'
                    '<th scope="col" class="govuk-table__header govuk-table__header--numeric">Rate for vehicles</th>'
                '</tr>'
            '</thead>'
            '<tbody class="govuk-table__body">'
                '<tr class="govuk-table__row">'
                    '<th scope="row" class="govuk-table__header">January</th>'
                    '<td class="govuk-table__cell govuk-table__cell--numeric">£85</td>'
                    '<td class="govuk-table__cell govuk-table__cell--numeric">£95</td>'
                '</tr>'
                '<tr class="govuk-table__row">'
                    '<th scope="row" class="govuk-table__header">February</th>'
                    '<td class="govuk-table__cell govuk-table__cell--numeric">£75</td>'
                    '<td class="govuk-table__cell govuk-table__cell--numeric">£55</td>'
                '</tr>'
                '<tr class="govuk-table__row">'
                    '<th scope="row" class="govuk-table__header">March</th>'
                    '<td class="govuk-table__cell govuk-table__cell--numeric">£165</td>'
                    '<td class="govuk-table__cell govuk-table__cell--numeric">£125</td>'
                '</tr>'
            '</tbody>'
        '</table>'
    )


def test_table_width(html):
    """
    Link: https://design-system.service.gov.uk/components/table/

    This if for custom column widths example.
    """
    table = ds.Table(
        data=[
            {"Date": "First 6 weeks", "Rate for vehicles": "£109.80 per week", "Rate for bicycles": "£59.10 per week"},
            {"Date": "Next 33 weeks", "Rate for vehicles": "£159.80 per week", "Rate for bicycles": "£89.10 per week"},
            {"Date": "Total estimated pay", "Rate for vehicles": "£4,282.20", "Rate for bicycles": "£2,182.20"},
        ],
        caption="Month you apply",
        header_cols=["Date"],
        col_width={"Date": "one-half", "Rate for vehicles": "one-quarter", "Rate for bicycles": "one-quarter"},
    )
    assert html(table) == html(
        '<table class="govuk-table">'
            '<caption class="govuk-table__caption govuk-table__caption--m">Month you apply</caption>'
            '<thead class="govuk-table__head">'
                '<tr class="govuk-table__row">'
                    '<th scope="col" class="govuk-table__header govuk-!-width-one-half">Date</th>'
                    '<th scope="col" class="govuk-table__header govuk-!-width-one-quarter">Rate for vehicles</th>'
                    '<th scope="col" class="govuk-table__header govuk-!-width-one-quarter">Rate for bicycles</th>'
                '</tr>'
            '</thead>'
            '<tbody class="govuk-table__body">'
                '<tr class="govuk-table__row">'
                    '<th scope="row" class="govuk-table__header">First 6 weeks</th>'
                    '<td class="govuk-table__cell">£109.80 per week</td>'
                    '<td class="govuk-table__cell">£59.10 per week</td>'
                '</tr>'
                '<tr class="govuk-table__row">'
                    '<th scope="row" class="govuk-table__header">Next 33 weeks</th>'
                    '<td class="govuk-table__cell">£159.80 per week</td>'
                    '<td class="govuk-table__cell">£89.10 per week</td>'
                '</tr>'
                '<tr class="govuk-table__row">'
                    '<th scope="row" class="govuk-table__header">Total estimated pay</th>'
                    '<td class="govuk-table__cell">£4,282.20</td>'
                    '<td class="govuk-table__cell">£2,182.20</td>'
                '</tr>'
            '</tbody>'
        '</table>'
    )


def test_tasklist(html):
    """
    Link: https://design-system.service.gov.uk/components/task-list/

    I have removed similar tasks for conciseness and so we are left with
    "Company Directors" and "Financial hostory".
    """
    task_list = ds.TaskList(
        ds.Task("Company Directors", "#", completed=True),
        ds.Task("Financial history", "#", hint="Include 5 years of the company's relevant financial information"),
    )
    assert html(task_list) == html(
        '<ul class="govuk-task-list">'
            '<li class="govuk-task-list__item govuk-task-list__item--with-link">'
                '<div class="govuk-task-list__name-and-hint">'
                    '<a class="govuk-link govuk-task-list__link" href="#" aria-describedby="company-directors-status">Company Directors</a>'
                '</div>'
                '<div class="govuk-task-list__status" id="company-directors-status">'
                    'Completed'
                '</div>'
            '</li>'
            '<li class="govuk-task-list__item govuk-task-list__item--with-link">'
                '<div class="govuk-task-list__name-and-hint">'
                    '<a class="govuk-link govuk-task-list__link" href="#" aria-describedby="financial-history-hint financial-history-status">Financial history</a>'
                    '<div id="financial-history-hint" class="govuk-task-list__hint">'
                        "Include 5 years of the company's relevant financial information"
                    '</div>'
                '</div>'
                '<div class="govuk-task-list__status" id="financial-history-status">'
                    '<strong class="govuk-tag govuk-tag--blue">Incomplete</strong>'
                '</div>'
            '</li>'
        '</ul>'
    )


def test_summary_list_simple(html):
    """
    Link: https://design-system.service.gov.uk/components/summary-list/

    This tests the simple sumary list without any actions.
    """
    summary_list = ds.SummaryList(
        ds.SummaryItem("Name", "Sarah Philips"),
        ds.SummaryItem("Date of birth", "5 January 1978"),
        ds.SummaryItem("Address", ds.Safe("72 Guild Street<br>London<br>SE23 6FH")),
        ds.SummaryItem("Contact details", ds.Div(ds.P("07700 900457"), ds.P("sarah.phillips@example.com"))),
    )
    assert html(summary_list) == html(
        '<dl class="govuk-summary-list">'
        # The spec doesn't include govuk-summary-list__row--no-actions class
        # '<div class="govuk-summary-list__row">'
        '<div class="govuk-summary-list__row govuk-summary-list__row--no-actions">'
            '<dt class="govuk-summary-list__key">Name</dt>'
            '<dd class="govuk-summary-list__value">Sarah Philips</dd>'
        '</div>'
        # The spec doesn't include govuk-summary-list__row--no-actions class
        # '<div class="govuk-summary-list__row">'
        '<div class="govuk-summary-list__row govuk-summary-list__row--no-actions">'
            '<dt class="govuk-summary-list__key">Date of birth</dt>'
            '<dd class="govuk-summary-list__value">5 January 1978</dd>'
        '</div>'
        # The spec doesn't include govuk-summary-list__row--no-actions class
        # '<div class="govuk-summary-list__row">'
        '<div class="govuk-summary-list__row govuk-summary-list__row--no-actions">'
            '<dt class="govuk-summary-list__key">Address</dt>'
            '<dd class="govuk-summary-list__value">72 Guild Street<br>London<br>SE23 6FH</dd>'
        '</div>'
        # The spec doesn't include govuk-summary-list__row--no-actions class
        # '<div class="govuk-summary-list__row">'
        '<div class="govuk-summary-list__row govuk-summary-list__row--no-actions">'
            '<dt class="govuk-summary-list__key">Contact details</dt>'
            '<dd class="govuk-summary-list__value">'
                # Specs don't have a div here but I think its useful
                '<div>'
                    '<p class="govuk-body">07700 900457</p>'
                    '<p class="govuk-body">sarah.phillips@example.com</p>'
                '</div>'
            '</dd>'
        '</div>'
        '</dl>'
    )


def test_summary_list_no_border(html):
    """
    Link: https://design-system.service.gov.uk/components/summary-list/

    This tests the simple sumary list without any actions or border.
    """
    summary_list = ds.SummaryList(
        ds.SummaryItem("Name", "Sarah Philips"),
        ds.SummaryItem("Date of birth", "5 January 1978"),
        ds.SummaryItem("Address", ds.Safe("72 Guild Street<br>London<br>SE23 6FH")),
        ds.SummaryItem("Contact details", ds.Div(ds.P("07700 900457"), ds.P("sarah.phillips@example.com"))),
        border=False,
    )
    assert html(summary_list) == html(
        '<dl class="govuk-summary-list govuk-summary-list--no-border">'
        # The spec doesn't include govuk-summary-list__row--no-actions class
        # '<div class="govuk-summary-list__row">'
        '<div class="govuk-summary-list__row govuk-summary-list__row--no-actions">'
            '<dt class="govuk-summary-list__key">Name</dt>'
            '<dd class="govuk-summary-list__value">Sarah Philips</dd>'
        '</div>'
        # The spec doesn't include govuk-summary-list__row--no-actions class
        # '<div class="govuk-summary-list__row">'
        '<div class="govuk-summary-list__row govuk-summary-list__row--no-actions">'
            '<dt class="govuk-summary-list__key">Date of birth</dt>'
            '<dd class="govuk-summary-list__value">5 January 1978</dd>'
        '</div>'
        # The spec doesn't include govuk-summary-list__row--no-actions class
        # '<div class="govuk-summary-list__row">'
        '<div class="govuk-summary-list__row govuk-summary-list__row--no-actions">'
            '<dt class="govuk-summary-list__key">Address</dt>'
            '<dd class="govuk-summary-list__value">72 Guild Street<br>London<br>SE23 6FH</dd>'
        '</div>'
        # The spec doesn't include govuk-summary-list__row--no-actions class
        # '<div class="govuk-summary-list__row">'
        '<div class="govuk-summary-list__row govuk-summary-list__row--no-actions">'
            '<dt class="govuk-summary-list__key">Contact details</dt>'
            '<dd class="govuk-summary-list__value">'
                # Specs don't have a div here but I think its useful
                '<div>'
                    '<p class="govuk-body">07700 900457</p>'
                    '<p class="govuk-body">sarah.phillips@example.com</p>'
                '</div>'
            '</dd>'
        '</div>'
        '</dl>'
    )



def test_summary_list_full(html):
    """
    Link: https://design-system.service.gov.uk/components/summary-list/

    This tests a sumary list with actions.
    """
    summary_list = ds.SummaryList(
        ds.SummaryItem("Name", "Sarah Philips"),
        ds.SummaryItem("Date of birth", "5 January 1978", ds.A("Change")),
        ds.SummaryItem("Address", ds.Safe("72 Guild Street<br>London<br>SE23 6FH"), ds.A("Change")),
        ds.SummaryItem("Contact details", ds.Div(ds.P("07700 900457"), ds.P("sarah.phillips@example.com")), ds.A("Add"), ds.A("Change")),
    )
    assert html(summary_list) == html(
        '<dl class="govuk-summary-list">'
            '<div class="govuk-summary-list__row govuk-summary-list__row--no-actions">'
                '<dt class="govuk-summary-list__key">Name</dt>'
                '<dd class="govuk-summary-list__value">Sarah Philips</dd>'
            '</div>'
            '<div class="govuk-summary-list__row">'
                '<dt class="govuk-summary-list__key">Date of birth</dt>'
                '<dd class="govuk-summary-list__value">5 January 1978</dd>'
                '<dd class="govuk-summary-list__actions">'
                    '<a class="govuk-link" href="#">Change<span class="govuk-visually-hidden"> date of birth</span></a>'
                '</dd>'
            '</div>'
            '<div class="govuk-summary-list__row">'
                '<dt class="govuk-summary-list__key">Address</dt>'
                '<dd class="govuk-summary-list__value">72 Guild Street<br>London<br>SE23 6FH</dd>'
                '<dd class="govuk-summary-list__actions">'
                    '<a class="govuk-link" href="#">Change<span class="govuk-visually-hidden"> address</span></a>'
                '</dd>'
            '</div>'
            '<div class="govuk-summary-list__row">'
                '<dt class="govuk-summary-list__key">Contact details</dt>'
                '<dd class="govuk-summary-list__value">'
                    # Specs don't have a div here but I think its useful
                    '<div>'
                        '<p class="govuk-body">07700 900457</p>'
                        '<p class="govuk-body">sarah.phillips@example.com</p>'
                    '</div>'
                '</dd>'
                '<dd class="govuk-summary-list__actions">'
                    '<ul class="govuk-summary-list__actions-list">'
                        '<li class="govuk-summary-list__actions-list-item">'
                            '<a class="govuk-link" href="#">Add<span class="govuk-visually-hidden"> contact details</span></a>'
                        '</li>'
                        '<li class="govuk-summary-list__actions-list-item">'
                            '<a class="govuk-link" href="#">Change<span class="govuk-visually-hidden"> contact details</span></a>'
                        '</li>'
                    '</ul>'
                '</dd>'
            '</div>'
        '</dl>'
    )


def test_summary_card_simple(html):
    summary_card = ds.SummaryCard(
        "Lead tenant",
        ds.SummaryList(
            ds.SummaryItem("Age", "38", ds.A("Change")),
            ds.SummaryItem("Nationality", "UK national resident in UK", ds.A("Change")),
            ds.SummaryItem("Working situation", "Part time - less than 30 hours a week", ds.A("Change")),
        ),
    )
    assert html(summary_card) == html(
        '<div class="govuk-summary-card">'
            '<div class="govuk-summary-card__title-wrapper">'
                '<h2 class="govuk-summary-card__title">Lead tenant</h2>'
            '</div>'
            '<div class="govuk-summary-card__content">'
                '<dl class="govuk-summary-list">'
                    '<div class="govuk-summary-list__row">'
                        '<dt class="govuk-summary-list__key">Age</dt>'
                        '<dd class="govuk-summary-list__value">38</dd>'
                        '<dd class="govuk-summary-list__actions">'
                            # '<a class="govuk-link" href="#">Change<span class="govuk-visually-hidden"> age (Lead tenant)</span></a>'
                            # TODO: The spec here includes the title of the card and I can't atm
                            '<a class="govuk-link" href="#">Change<span class="govuk-visually-hidden"> age</span></a>'
                        '</dd>'
                    '</div>'
                    '<div class="govuk-summary-list__row">'
                        '<dt class="govuk-summary-list__key">Nationality</dt>'
                        '<dd class="govuk-summary-list__value">UK national resident in UK</dd>'
                        '<dd class="govuk-summary-list__actions">'
                            # '<a class="govuk-link" href="#">Change<span class="govuk-visually-hidden"> nationality (Lead tenant)</span></a>'
                            # TODO: The spec here includes the title of the card and I can't atm
                            '<a class="govuk-link" href="#">Change<span class="govuk-visually-hidden"> nationality</span></a>'
                        '</dd>'
                    '</div>'
                    '<div class="govuk-summary-list__row">'
                        '<dt class="govuk-summary-list__key">Working situation</dt>'
                        '<dd class="govuk-summary-list__value">Part time - less than 30 hours a week</dd>'
                        '<dd class="govuk-summary-list__actions">'
                            # '<a class="govuk-link" href="#">Change<span class="govuk-visually-hidden"> working situation (Lead tenant)</span></a>'
                            # TODO: The spec here includes the title of the card and I can't atm
                            '<a class="govuk-link" href="#">Change<span class="govuk-visually-hidden"> working situation</span></a>'
                        '</dd>'
                    '</div>'
                '</dl>'
            '</div>'
        '</div>'
    )


def test_summary_card_actions(html):
    summary_card = ds.SummaryCard(
        "University of Gloucestershire",
        ds.SummaryList(
            ds.SummaryItem("Course", ds.Safe("English (3DMD)<br>PGCE with QTS full time")),
            ds.SummaryItem("Location", ds.Safe("School name<br>Road, City, SW1 1AA")),
        ),
        actions=[ds.A("Delete choice"), ds.A("Withdraw")]
    )
    assert html(summary_card) == html(
        '<div class="govuk-summary-card">'
            '<div class="govuk-summary-card__title-wrapper">'
                '<h2 class="govuk-summary-card__title">University of Gloucestershire</h2>'
                '<ul class="govuk-summary-card__actions">'
                '<li class="govuk-summary-card__action">'
                    '<a class="govuk-link" href="#">Delete choice'
                        # '<span class="govuk-visually-hidden"> of University of Gloucestershire (University of Gloucestershire)</span>'
                        # Minor changes to spec for consistency
                        '<span class="govuk-visually-hidden"> (University of Gloucestershire)</span>'
                    '</a>'
                '</li>'
                '<li class="govuk-summary-card__action">'
                    '<a class="govuk-link" href="#">Withdraw'
                        # '<span class="govuk-visually-hidden">from University of Gloucestershire (University of Gloucestershire)</span>'
                        # Minor changes to spec for consistency
                        '<span class="govuk-visually-hidden"> (University of Gloucestershire)</span>'
                    '</a>'
                '</li>'
                '</ul>'
            '</div>'
            '<div class="govuk-summary-card__content">'
                '<dl class="govuk-summary-list">'
                # '<div class="govuk-summary-list__row">'
                # Spec is missing a class
                '<div class="govuk-summary-list__row govuk-summary-list__row--no-actions">'
                    '<dt class="govuk-summary-list__key">Course</dt>'
                    '<dd class="govuk-summary-list__value">English (3DMD)<br>PGCE with QTS full time</dd>'
                '</div>'
                # '<div class="govuk-summary-list__row">'
                # Spec is missing a class
                '<div class="govuk-summary-list__row govuk-summary-list__row--no-actions">'
                    '<dt class="govuk-summary-list__key">Location</dt>'
                    '<dd class="govuk-summary-list__value">School name<br>Road, City, SW1 1AA</dd>'
                '</div>'
                '</dl>'
            '</div>'
        '</div>'
    )
