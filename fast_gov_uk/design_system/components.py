import fasthtml.common as fh

from .utils import mkid


def Inset(text: str, **kwargs) -> fh.FT:
    """
    Inset text component.

    Args:
        text (str): The main text to display.
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML Inset text component.
    """
    return fh.Div(text, cls="govuk-inset-text", **kwargs)


def Detail(
    summary: str,
    *content: fh.FT | str,
    open: bool = False,
    **kwargs,
) -> fh.FT:
    """
    Detail component.

    Args:
        summary (str): The summary text for the detail.
        *content (FT or str): The content to display when the detail is expanded.
        open (bool, optional): If True, the detail is initially open. Defaults to False.
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML Detail component.
    """
    return fh.Details(
        fh.Summary(
            fh.Span(summary, cls="govuk-details__summary-text"),
            cls="govuk-details__summary",
        ),
        fh.Div(
            *content,
            cls="govuk-details__text",
        ),
        cls="govuk-details",
        open=open,
        **kwargs,
    )


def Panel(
    *content: fh.FT | str,
    title: str = "",
    **kwargs,
) -> fh.FT:
    """
    Panel component.

    Args:
        *content (FT or str): The content to display in the panel.
        title (str, optional): The title of the panel. Defaults to "".
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML Panel component.
    """
    return fh.Div(
        fh.H1(title, cls="govuk-panel__title") if title else "",
        fh.Div(*content, cls="govuk-panel__body"),
        cls="govuk-panel govuk-panel--confirmation",
        **kwargs,
    )


def Tag(
    text: str,
    color: str = "",
    **kwargs,
) -> fh.FT:
    """
    Tag component.

    Args:
        text (str): The text to display in the tag.
        color (str, optional): The color of the tag. Defaults to "".
        **kwargs: Additional keyword arguments.

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
        "turquoise": " govuk-tag--turquoise",
        "light-blue": " govuk-tag--light-blue",
        "purple": " govuk-tag--purple",
        "pink": " govuk-tag--pink",
        "orange": " govuk-tag--orange",
    }
    return fh.Strong(text, cls=f"govuk-tag{colors.get(color)}", **kwargs)


def Warning(
    *content: fh.FT | str,
    **kwargs,
) -> fh.FT:
    """
    Warning component.

    Args:
        *content (FT or str): The content to display in the warning.
        **kwargs: Additional keyword arguments.

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
        **kwargs,
    )


def NotificatonLink(
    text: str,
    href: str = "#",
    **kwargs,
) -> fh.FT:
    """
    NotificationLink component.

    Args:
        text (str): The text to display in the link.
        href (str, optional): The URL the link points to. Defaults to "#".
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML NotificationLink component.
    """
    cls = "govuk-notification-banner__link"
    return fh.A(text, href=href, cls=cls, **kwargs)


def NotificatonHeading(*content: fh.FT | str, **kwargs) -> fh.FT:
    """
    Notification heading component.

    Args:
        *content (FT or str): The content to display in the heading.
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML H2 component.
    """
    return fh.P(
        *content,
        cls="govuk-notification-banner__heading",
        **kwargs,
    )


def Notification(
    *content: fh.FT,
    title: str = "Important",
    success: bool = False,
    **kwargs,
) -> fh.FT:
    """
    Notification banner component.

    Args:
        *content (FT): The content to display in the notification banner.
        title (str, optional): The title of the notification. Defaults to "Important".
        success (bool, optional): If True, applies a success style. Defaults to False.
        **kwargs: Additional keyword arguments.

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
        role="alert",
        aria_labelledby="govuk-notification-banner-title",
        data_module="govuk-notification-banner",
        **kwargs,
    )


def _accordion_section(accordion_id, n, heading, summary, content, open=False):
    """
    Helper function to create an accordion section.

    Args:
        accordion_id (str): Id for accordion.
        n (int): The section number.
        heading (str): The heading of the section.
        summary (str): The summary of the section.
        content (str): The content of the section.
        open (bool, optional): If True, the section is initially open. Defaults to False.

    Returns:
        FT: A FastHTML accordion section component.
    """
    return fh.Div(
        fh.Div(
            fh.H2(
                fh.Span(
                    heading,
                    cls="govuk-accordion__section-button",
                    id=f"{accordion_id}-heading-{n}",
                ),
                cls="govuk-accordion__section-heading",
            ),
            fh.Div(
                summary,
                cls="govuk-accordion__section-summary govuk-body",
                id=f"{accordion_id}-summary-{n}",
            )
            if summary
            else "",
            cls="govuk-accordion__section-header",
        ),
        fh.Div(
            content,
            cls="govuk-accordion__section-content",
            id=f"{accordion_id}-content-{n}",
        ),
        cls="govuk-accordion__section",
        open=open,
    )


def Accordion(*sections: dict, accordion_id="accordion", **kwargs) -> fh.FT:
    """
    Accordion component.

    Args:
        *sections (dict): Sections to include in the accordion.
        accordion_id (str, optional): Id for accordion. Defaults to "accordion".
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML Accordion component.
    """
    return fh.Div(
        *[
            _accordion_section(
                accordion_id,
                n + 1,
                section["heading"],
                section.get("summary", ""),
                section["content"],
                open=section.get("open", False),
            )
            for n, section in enumerate(sections)
        ],
        cls="govuk-accordion",
        data_module="govuk-accordion",
        **kwargs,
    )


def _tab_panel(heading, content, active=False):
    """
    Helper function to create a tab panel.

    Args:
        heading (str): The heading of the panel.
        content (str): The content of the panel.
        active (bool, optional): Tab is active. Defaults to False.

    Returns:
        FT: A FastHTML tab section component.
    """
    tab_id = mkid(heading)
    active_cls = "" if active else " govuk-tabs__panel--hidden"
    return fh.Div(
        fh.H2(heading, cls="govuk-heading-l"),
        content,
        cls=f"govuk-tabs__panel{active_cls}",
        id=f"{tab_id}",
    )


def _tab_li(heading, active=False):
    """
    Helper function to create a tab list item.

    Args:
        heading (str): The heading of the tab.
        active (bool, optional): Tab is active. Defaults to False.

    Returns:
        FT: A FastHTML tab list item component.
    """
    tab_id = mkid(heading)
    active_cls = " govuk-tabs__list-item--selected" if active else ""
    return fh.Li(
        fh.A(
            heading,
            href=f"#{tab_id}",
            cls="govuk-tabs__tab",
        ),
        cls=f"govuk-tabs__list-item{active_cls}",
    )


def Tab(*panels: dict, title="", **kwargs) -> fh.FT:
    """
    Tab component.

    Args:
        *panels (dict): Panels to include in the tab.
        title (str, optional): Title of the tab. Defaults to "".
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML Tab component.
    """
    return fh.Div(
        fh.H2(title, cls="govuk-tabs__title"),
        fh.Ul(
            *[
                _tab_li(panel["heading"], active=(n == 0))
                for n, panel in enumerate(panels)
            ],
            cls="govuk-tabs__list",
        ),
        *[
            _tab_panel(panel["heading"], panel["content"], active=(n == 0))
            for n, panel in enumerate(panels)
        ],
        cls="govuk-tabs",
        data_module="govuk-tabs",
        **kwargs,
    )


def ErrorSummary(title: str, *links: fh.FT, **kwargs) -> fh.FT:
    """
    ErrorSummary component.

    Args:
        title (str): The title of the ErrorSummary component.
        *links (A): Links to include in the ErrorSummary component.
        **kwargs: Additional keyword arguments.

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
                fh.Ul(
                    *[fh.Li(link) for link in links],
                    cls="govuk-list govuk-error-summary__list",
                ),
                cls="govuk-error-summary__body",
            ),
            role="alert",
        ),
        cls="govuk-error-summary",
        data_module="govuk-error-summary",
        **kwargs,
    )


def _table_head(headers, numeric_cols, col_width):
    ths = []
    for header in headers:
        cls = "govuk-table__header"
        if header in col_width:
            width_cls = col_width.get(header, "")
            cls += f" govuk-!-width-{width_cls}"
        if header in numeric_cols:
            cls += " govuk-table__header--numeric"
        th = fh.Th(header, scope="col", cls=cls)
        ths.append(th)
    return fh.Thead(
        fh.Tr(*ths, cls="govuk-table__row"),
        cls="govuk-table__head",
    )


def _table_body(data, header_cols, numeric_cols):
    trs = []
    for row in data:
        tds = []
        for col, val in row.items():
            if col in header_cols:
                cls = "govuk-table__header"
                if col in numeric_cols:
                    cls += " govuk-table__header--numeric"
                td = fh.Th(val, cls=cls, scope="row")
            else:
                cls = "govuk-table__cell"
                if col in numeric_cols:
                    cls += " govuk-table__cell--numeric"
                td = fh.Td(val, cls=cls)
            tds.append(td)
        trs.append(fh.Tr(*tds, cls="govuk-table__row"))
    return fh.Tbody(*trs, cls="govuk-table__body")


def Table(
    data: list[dict],
    caption: str = "",
    header_cols: list | None = None,
    numeric_cols: list | None = None,
    col_width: dict | None = None,
    small_text: bool = False,
    **kwargs,
) -> fh.FT:
    """
    Table component.

    Args:
        data (list[dict]): Data for the Table component.
        caption (str, optional): The caption of the Table component. Defaults to "".
        header_cols (list, optional): List of columns that should be headers in each row. Defaults to None.
        numeric_cols (list, optional): List of columns that are numeric. Defaults to None.
        col_width (dict, optional): Override column widths. Defaults to None.
        small_text (bool, optional): Render a more compact table. Defaults to False.
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML Table component.
    """
    header_cols = header_cols or []
    numeric_cols = numeric_cols or []
    col_width = col_width or {}
    small_text_cls = " govuk-table--small-text-until-tablet" if small_text else ""
    _caption = fh.Caption(caption, cls="govuk-table__caption govuk-table__caption--m")
    return fh.Table(
        _caption if caption else "",
        _table_head(data[0].keys(), numeric_cols, col_width),
        _table_body(data, header_cols, numeric_cols),
        cls=f"govuk-table{small_text_cls}",
        **kwargs,
    )


def Task(
    label: str,
    href: str,
    completed: bool = False,
    hint: str = "",
    **kwargs,
) -> fh.FT:
    """
    Task component.

    Args:
        label (str): Label for the Task item.
        href (str): Link for the Task item.
        completed (bool, optional): Is the task completed? Defaults to False.
        hint (str, optional): Hint for the Task item. Defaults to "".
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML Task component.
    """
    _id = mkid(label)
    status_id = f"{_id}-status"
    hint_id = f"{_id}-hint"
    aria_hint_id = f"{hint_id} " if hint else ""
    return fh.Li(
        fh.Div(
            fh.A(
                label,
                href=href,
                cls="govuk-link govuk-task-list__link",
                aria_describedby=f"{aria_hint_id}{status_id}",
            ),
            fh.Div(
                hint,
                cls="govuk-task-list__hint",
                _id=hint_id,
            )
            if hint
            else "",
            cls="govuk-task-list__name-and-hint",
        ),
        fh.Div(
            "Completed",
            cls="govuk-task-list__status",
            _id=status_id,
        )
        if completed
        else fh.Div(
            fh.Strong(
                "Incomplete",
                cls="govuk-tag govuk-tag--blue",
            ),
            cls="govuk-task-list__status",
            _id=status_id,
        ),
        cls="govuk-task-list__item govuk-task-list__item--with-link",
        **kwargs,
    )


def TaskList(
    *tasks: fh.FT,
    **kwargs,
) -> fh.FT:
    """
    TaskList component.

    Args:
        *tasks (FT): Tasks for the TaskList.
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML TaskList component.
    """
    return fh.Ul(
        *[task for task in tasks],
        cls="govuk-task-list",
        **kwargs,
    )


def SummaryItem(key: str, value: str | fh.FT, *actions: fh.FT, **kwargs):
    """
    SummaryRow component - a list of these goes in to form a SummaryList.

    Args:
        key (str): Key for the SummaryRow.
        value (str | fh.FT): Content of the SummaryRow.
        *actions (fh.FT): Action(s) assigned to the SummaryRow.
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML SummaryRow component.
    """
    for action in actions:
        action.children = (
            *action.children,
            fh.Span(key.lower(), cls="govuk-visually-hidden"),
        )

    if not actions:
        actions_component = ""
    else:
        if len(actions) == 1:
            actions_component = fh.Dd(*actions, cls="govuk-summary-list__actions")
        else:
            actions_component = fh.Dd(
                fh.Ul(
                    *[
                        fh.Li(action, cls="govuk-summary-list__actions-list-item")
                        for action in actions
                    ],
                    cls="govuk-summary-list__actions-list",
                ),
                cls="govuk-summary-list__actions",
            )
    no_actions_cls = "" if actions else " govuk-summary-list__row--no-actions"

    return fh.Div(
        fh.Dt(key, cls="govuk-summary-list__key"),
        fh.Dd(value, cls="govuk-summary-list__value"),
        actions_component,
        cls=f"govuk-summary-list__row{no_actions_cls}",
        **kwargs,
    )


def SummaryList(*items: fh.FT, border: bool = True, **kwargs) -> fh.FT:
    """
    SummaryList component.

    Args:
        *items (FT): List of SummaryItems.
        border (bool, optional): Choose if a border should be drawn. Defaults to True.
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML SummaryList component.
    """
    no_border_cls = "" if border else " govuk-summary-list--no-border"
    return fh.Dl(
        *items,
        cls=f"govuk-summary-list{no_border_cls}",
        **kwargs,
    )


def SummaryCard(
    title: str, summary_list: fh.FT, actions: list[fh.FT] | None = None, **kwargs
) -> fh.FT:
    """
    SummaryCard component.

    Args:
        title (str): Title of the card.
        summary_list (fh.FT): SummaryList component.
        actions (list[fh.FT], optional): List of card actions. Defaults to None.
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML component.
    """
    actions = actions or []

    for action in actions:
        action.children = (
            *action.children,
            fh.Span(f"({title})", cls="govuk-visually-hidden"),
        )

    actions_component = (
        fh.Ul(
            *[fh.Li(action, cls="govuk-summary-card__action") for action in actions],
            cls="govuk-summary-card__actions",
        )
        if actions
        else ""
    )

    return fh.Div(
        fh.Div(
            fh.H2(title, cls="govuk-summary-card__title"),
            actions_component,
            cls="govuk-summary-card__title-wrapper",
        ),
        fh.Div(
            summary_list,
            cls="govuk-summary-card__content",
        ),
        cls="govuk-summary-card",
        **kwargs,
    )
