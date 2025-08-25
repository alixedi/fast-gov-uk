import fasthtml.common as fh


def Inset(text: str) -> fh.FT:
    """
    Inset text component.
    Args:
        text (str): The main text to display.
    Returns:
        FT: A FastHTML Inset text component.
    """
    return fh.Div(text, cls="govuk-inset-text")


def Detail(
    summary: str,
    *content: fh.FT,
    open: bool = False,
) -> fh.FT:
    """
    Detail component.
    Args:
        summary (str): The summary text for the detail.
        content (FT): The content to display when the detail is expanded.
        open (bool): If True, the detail is initially open. Defaults to False.
    Returns:
        FT: A FastHTML Detail component.
    """
    return fh.Details(
        fh.Summary(summary, cls="govuk-details__summary"),
        *content,
        cls="govuk-details",
        open=open,
    )


def Panel(
    *content: fh.FT,
    title: str = "",
) -> fh.FT:
    """
    Panel component.
    Args:
        content (FT): The content to display in the panel.
        title (str): The title of the panel. Defaults to "".
    Returns:
        FT: A FastHTML Panel component.
    """
    return fh.Div(
        fh.H1(title, cls="govuk-panel__title") if title else "",
        fh.Div(*content, cls="govuk-panel__body"),
        cls="govuk-panel govuk-panel--confirmation",
    )


def Tag(
    text: str,
    color: str = "",
) -> fh.FT:
    """
    Tag component.
    Args:
        text (str): The text to display in the tag.
        color (str): The color of the tag. Defaults to "blue".
    Returns:
        FT: A FastHTML Tag component.
    """
    colors = {
        "": "",
        "blue": " govuk-tag--blue",
        "green": " govuk-tag--green",
        "red": " govuk-tag--red",
        "yellow": " govuk-tag--yellow",
        "grey": " govuk-tag--grey",
    }
    return fh.Strong(text, cls=f"govuk-tag{colors.get(color)}")


def Warning(
    *content: fh.FT,
) -> fh.FT:
    """
    Warning component.
    Args:
        content (FT): The content to display in the warning.
    Returns:
        FT: A FastHTML Warning component.
    """
    return fh.Div(
        fh.Span(
            "!",
            cls="govuk-warning-text__icon",
            aria_hidden="true",
        ),
        fh.Strong(
            fh.Span("Warning", cls="govuk-visually-hidden"),
            *content,
            cls="govuk-warning-text__text",
        ),
        cls="govuk-warning-text",
    )


def Notification(
    content: fh.FT,
    title: str,
    success: bool = False,
) -> fh.FT:
    """
    Notification banner component.
    Args:
        content (FT): The content to display in the phase banner.
        title (str): The title of the notification.
        success (bool): If True, applies a success style. Defaults to False.
    Returns:
        FT: A FastHTML Notification component.
    """
    success_cls = " govuk-notification-banner--success" if success else ""
    return fh.Div(
        fh.Div(
            fh.H2(
                title,
                cls="govuk-notification-banner__title",
                id="govuk-notification-banner-title",
            ),
            cls="govuk-notification-banner__header",
        ),
        fh.Div(content, cls="govuk-notification-banner__content"),
        cls=f"govuk-notification-banner{success_cls}",
        role="region",
        aria_labelledby="govuk-notification-banner-title",
        data_module="govuk-notification-banner",
    )


def _accordian_section(n, heading, content, open=False):
    """
    Helper function to create an accordion section.
    Args:
        n (int): The section number.
        heading (str): The heading of the section.
        content (str): The content of the section.
        open (bool): If True, the section is initially open. Defaults to False.
    Returns:
        FT: A FastHTML accordion section component.
    """
    return fh.Div(
        fh.Div(
            fh.H2(
                fh.Span(
                    heading,
                    cls="govuk-accordion__section-button",
                    id=f"accordion-section-heading-{n}",
                ),
                cls="govuk-accordion__section-heading",
            ),
            cls="govuk-accordion__section-header",
        ),
        fh.Div(
            content,
            cls="govuk-accordion__section-content",
            id=f"accordion-section-content-{n}",
        ),
        cls="govuk-accordion__section",
        open=open,
    )


def Accordian(*sections: dict) -> fh.FT:
    """
    Accordion component.
    Args:
        *sections (dict): Sections to include in the accordion.
    Returns:
        FT: A FastHTML Accordion component.
    """
    return fh.Div(
        *[
            _accordian_section(
                n + 1,
                section["heading"],
                section["content"],
                open=section.get("open", False),
            )
            for n, section in enumerate(sections)
        ],
        cls="govuk-accordion",
        data_module="govuk-accordion",
    )


def _tab_panel(n, heading, content):
    """
    Helper function to create a tab panel.
    Args:
        n (int): The panel number.
        heading (str): The heading of the panel.
        content (str): The content of the panel.
    Returns:
        FT: A FastHTML tab section component.
    """
    active = n == 0  # The first tab is active by default
    active_cls = "" if active else " govuk-tabs__panel--hidden"
    return fh.Div(
        fh.H2(heading, cls="govuk-heading-l"),
        content,
        cls=f"govuk-tabs__panel{active_cls}",
        id=f"tab-panel-{n}",
    )


def _tab_li(n, heading):
    """
    Helper function to create a tab list item.
    Args:
        n (int): The list item number.
        heading (str): The heading of the tab.
    Returns:
        FT: A FastHTML tab list item component.
    """
    active = n == 0  # The first tab is active by default
    active_cls = " govuk-tabs__list-item--selected" if active else ""
    return fh.Li(
        fh.A(
            heading,
            href=f"#tab-panel-{n}",
            cls="govuk-tabs__tab",
        ),
        cls=f"govuk-tabs__list-item{active_cls}",
    )


def Tab(*panels: dict) -> fh.FT:
    """
    Tab component.
    Args:
        *panels (dict): Panels to include in the tab.
    Returns:
        FT: A FastHTML Tab component.
    """
    return fh.Div(
        fh.Ul(
            *[_tab_li(n, panel["heading"]) for n, panel in enumerate(panels)],
            cls="govuk-tabs__list",
        ),
        *[
            _tab_panel(n, panel["heading"], panel["content"])
            for n, panel in enumerate(panels)
        ],
        cls="govuk-tabs",
        data_module="govuk-tabs",
    )


def ErrorSummary(title: str, *links: fh.FT) -> fh.FT:
    """
    ErrorSummary component.
    Args:
        title (str): The title of the ErrorSummary component.
        links (A): Links to include in the ErrorSummary component.
    Returns:
        FT: A FastHTML ErrorSummary component.
    """
    return fh.Div(
        fh.Div(
            fh.H2(
                title,
                cls="govuk-error-summary__title",
            ),
            fh.Div(
                fh.Ul(*[fh.Li(link) for link in links]),
                cls="govuk-error-summary__body",
            ),
            role="alert",
        ),
        cls="govuk-error-summary",
        data_module="govuk-error-summary",
    )


def Table(caption: str, data: list[dict], row_headers: list = []):
    """
    Table component.
    Args:
        caption (str): The caption of the Table component.
        data (list[dict]): Data for the Table component.
        headers (list): List of columns that should be headers in each row
    Returns:
        FT: A FastHTML Table component.
    """
    headers = data[0].keys()
    return fh.Table(
        fh.Caption(caption, cls="govuk-table__caption govuk-table__caption--m"),
        fh.Thead(
            fh.Tr(
                *[
                    fh.Th(header, scope="col", cls="govuk-table__header")
                    for header in headers
                ],
                cls="govuk-table__row",
            ),
            cls="govuk-table__head",
        ),
        fh.Tbody(
            *[
                fh.Tr(
                    *[
                        fh.Th(row[key], cls="govuk-table__header")
                        if key in row_headers
                        else fh.Td(row[key], cls="govuk-table__cell")
                        for key in row
                    ],
                    cls="govuk-table__row",
                )
                for row in data
            ],
            cls="govuk-table__body",
        ),
        cls="govuk-table",
    )


def Task(
    label: str,
    href: str,
    completed: bool = False,
    hint: str = "",
) -> fh.FT:
    """
    Task component.
    Args:
        label (str): Label for the Task item.
        href (str): Link for the Task item.
        completed (bool): Is the taks completed?
        hint (str): Hint for the Task item.
    Returns:
        FT: A FastHTML Task component.
    """
    _id = label.lower().replace(" ", "-")
    return fh.Li(
        fh.Div(
            fh.A(
                label,
                href=href,
                cls="govuk-link govuk-task-list__link",
                aria_describedby=f"{_id}-status",
            ),
            fh.Div(
                hint,
                cls="govuk-task-list__hint",
                _id=f"{_id}-hint",
            )
            if hint
            else "",
            fh.Div(
                "Completed",
                cls="govuk-task-list__status",
                _id=f"{_id}-status",
            )
            if completed
            else fh.Div(
                fh.Strong(
                    "Incomplete",
                    cls="govuk-tag govuk-tag--blue",
                ),
                cls="govuk-task-list__status",
                _id=f"{_id}-status",
            ),
            cls="govuk-task-list__name-and-hint",
        ),
        cls="govuk-task-list__item govuk-task-list__item--with-link",
    )


def TaskList(
    *tasks: fh.FT,
) -> fh.FT:
    """
    TaskList component.
    Args:
        TaskList (list[Task]): Tasks for the TaskList.
    Returns:
        FT: A FastHTML TaskList component.
    """
    return fh.Ul(
        *[task for task in tasks],
        cls="govuk-task-list",
    )


def SummaryList(rows: list[tuple[str, str, list[fh.FT]]], border: bool = True) -> fh.FT:
    """
    SummaryList component.
    Args:
        rows (list): List of key (str), value (str), action (A) tuples.
        border (bool): Choose if a border should be drawn.
    Returns:
        FT: A FastHTML SummaryList component
    """
    return fh.Div(
        *[
            fh.Div(
                fh.Dt(key, cls="govuk-summary-list__key"),
                fh.Dd(value, cls="govuk-summary-list__value"),
                fh.Dd(
                    fh.Ul(
                        *[
                            fh.Li(action, cls="govuk-summary-list__actions-list-item")
                            for action in actions
                        ],
                        cls="govuk-summary-list__actions-list",
                    ),
                    cls="govuk-summary-list__actions",
                ),
                cls="govuk-summary-list__row",
            )
            for key, value, actions in rows
        ],
        cls=f"govuk-summary-list{'' if border else ' govuk-summary-list--no-border'}",
    )


def SummaryCard(
    title: str, summary_list: fh.FT, actions: list[fh.FT] | None = None
) -> fh.FT:
    """
    SummaryCard component.
    Args:
        title (str): Title of the card.
        summary_list (list): SummaryList component.
        actions (list): List of card actions. Defaults to None.
    Returns:
        FT: A FastHTML component.
    """
    actions = actions or []
    return fh.Div(
        fh.Div(
            fh.H2(title, cls="govuk-summary-card__title"),
            fh.Ul(
                *[fh.Li(action, cls="govuk-summary-card__actio") for action in actions],
                cls="govuk-summary-card__actions",
            ),
            cls="govuk-summary-card__title-wrapper",
        ),
        fh.Div(
            summary_list,
            cls="govuk-summary-card__content",
        ),
        cls="govuk-summary-card",
    )
