"""
GOV.UK Design System components such as Inset, Detail, Panel, Tag, Warning,
Notification, Accordion, Tab, ErrorSummary, Table, TaskList, SummaryList,
and SummaryCard.

Each component is implemented as a function that returns a FastHTML
component with the appropriate GOV.UK classes and structure.
"""

import fasthtml.common as fh

from .utils import mkid


def Inset(text: str, **kwargs) -> fh.FT:
    """
    `GOV.UK Inset text`_ component. Use the inset text component to differentiate
    a block of text from the content that surrounds it, for example: quotes, examples
    and additional information about the page.

    Examples:

        >>> inset = ds.Inset("This is an inset text")
        # Renders inset text -
        # | This is an inset text

    Args:
        text (str): The main text to display.
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML Inset text component.

    .. _GOV.UK Inset text: https://design-system.service.gov.uk/components/inset-text/
    """
    return fh.Div(text, cls="govuk-inset-text", **kwargs)


def Detail(
    summary: str,
    *content: fh.FT | str,
    open: bool = False,
    **kwargs,
) -> fh.FT:
    """
    `GOV.UK Detail`_ component to make a page easier to scan by letting users reveal
    more detailed information only if they need it.

    Examples:

        >>> detail = ds.Detail("More details", "This is the detailed content.")
        # Renders detail component with summary and content.
        # ▼ More details
        # | This is the detailed content.

    Args:
        summary (str): The summary text for the detail.
        *content (FT or str): The content to display when the detail is expanded.
        open (bool, optional): If True, the detail is initially open. Defaults to False.
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML Detail component.

    .. _GOV.UK Detail: https://design-system.service.gov.uk/components/details/
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
    `GOV.UK Panel`_ component - a visible container used on confirmation or
    results pages to highlight important content.

    Examples:

        >>> panel = ds.Panel("Panel content.", title="Test")
        # Renders panel component with title and content.
        # -----------------------
        # | Test
        # | Panel content.
        # -----------------------

    Args:
        *content (FT or str): The content to display in the panel.
        title (str, optional): The title of the panel. Defaults to "".
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML Panel component.

    .. _GOV.UK Panel: https://design-system.service.gov.uk/components/panel/
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
    `GOV.UK Tag`_ component used to show users the status of something.

    Examples:

        >>> tag = ds.Tag("In progress", color="blue")
        # Renders tag component with blue color.
        # [ In progress ]

    Args:
        text (str): The text to display in the tag.
        color (str, optional): The color of the tag. Defaults to "".
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML Tag component.

    .. _GOV.UK Tag: https://design-system.service.gov.uk/components/tag/
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
    `GOV.UK Warning`_ text component used when you need to warn users about
    something important, such as legal consequences of an action, or lack
    of action, that they might take.

    Examples:

        >>> warning = ds.Warning("This is a warning message.")
        # Renders warning component with content.
        # ! This is a warning message.

    Args:
        *content (FT or str): The content to display in the warning.
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML Warning component.

    .. _GOV.UK Warning: https://design-system.service.gov.uk/components/warning-text/
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
    NotificationLink component used in :py:meth:`Notification`.

    Examples:

        >>> link = ds.NotificatonLink("Click here", href="/more-info")
        >>> str(link)
        <a class="govuk-notification-banner__link" href="/more-info">Click here</a>

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
    Notification heading component usef in :py:meth:`Notification`.

    Examples:

        >>> heading = ds.NotificatonHeading("Important update")
        >>> str(heading)
        <p class="govuk-notification-banner__heading">Important update</p>

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
    `GOV.UK Notification banner`_ component used to tell the user about something
    they need to know about, but that's not directly related to the page content.

    A notification banner lets you tell the user about something that's not directly
    relevant to the thing they're trying to do on that page of the service.

    For example:

        - telling the user about a problem that's affecting the service as a whole
        - telling the user about something that affects them in particular
        - telling the user about the outcome of something they've just done on a previous page

    Examples:

        >>> notification = ds.Notification(
        ...     ds.NotificatonHeading("Service update"),
        ...     "Our service will be down for maintenance on Saturday.",
        ...     title="Important",
        ... )
        # Renders notification banner with heading and content.
        # ------------------------------
        # | Important
        # | Service update
        # | Our service will be down for maintenance on Saturday.
        # ------------------------------

    Args:
        *content (FT): The content to display in the notification banner.
        title (str, optional): The title of the notification. Defaults to "Important".
        success (bool, optional): If True, applies a success style. Defaults to False.
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML Notification component.

    .. _GOV.UK Notification banner: https://design-system.service.gov.uk/components/notification-banner/
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
    Helper function to create an accordion section for :py:meth:`Accordion`.

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
    `GOV.UK Accordion`_ component - lets users show and hide sections of
    related content on a page.

    Only use an accordion if there's evidence it's helpful for the user to:

        - see an overview of multiple, related sections of content
        - choose to show and hide sections that are relevant to them
        - look across information that might otherwise be on different pages

    Examples:

        >>> accordion = ds.Accordion(
        ...     {"heading": "Section 1", "content": "Content 1.", "open": True},
        ...     {"heading": "Section 2", "summary": "Summary 2.", "content": "Content 2."},
        ... )
        # Renders accordion with two sections, second section is open by default.
        # ------------------------------
        # | Section 1
        # | ▲ Hide
        # | Content for section 1.
        # ------------------------------
        # | Section 2
        # | Summary for section 2.
        # | ▼ Show
        # ------------------------------

    Args:
        *sections (dict): Sections to include in the accordion.
        accordion_id (str, optional): Id for accordion. Defaults to "accordion".
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML Accordion component.

    .. _GOV.UK Accordion: https://design-system.service.gov.uk/components/accordion/
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
    Helper function to create a tab panel for :py:meth:`Tab`.

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
    Helper function to create a tab list item for :py:meth:`Tab`.

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
    `GOV.UK Tab`_ componen - lets users navigate between related sections
    of content, displaying one section at a time.

    Tabs can be a helpful way of letting users quickly switch between related
    information if:

        - your content can be usefully separated into clearly labelled sections
        - the first section is more relevant than the others for most users
        - users will not need to view all the sections at once

    Examples:

        >>> tab = ds.Tab(
        ...     {"heading": "Tab 1", "content": "Content 1."},
        ...     {"heading": "Tab 2", "content": "Content 2."},
        ...     title="Example Tabs",
        ... )
        # Renders tab component with two panels.
        # ------------------------------
        # | Example Tabs
        # | [Tab 1] Tab 2
        # | Content 1.
        # ------------------------------

    Args:
        *panels (dict): Panels to include in the tab.
        title (str, optional): Title of the tab. Defaults to "".
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML Tab component.

    .. _GOV.UK Tab: https://design-system.service.gov.uk/components/tabs/
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
    `GOV.UK Error Summary`_ component used at the top of a page to summarise
    any errors a user has made.

    Examples:

        >>> error_summary = ds.ErrorSummary(
        ...     "There is a problem",
        ...     ds.A("Error 1", href="#error1"),
        ...     ds.A("Error 2", href="#error2"),
        ... )
        # Renders error summary component with title and links.
        # ------------------------------
        # | There is a problem
        # | - Error 1
        # | - Error 2
        # ------------------------------

    Args:
        title (str): The title of the ErrorSummary component.
        *links (A): Links to include in the ErrorSummary component.
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML ErrorSummary component.

    .. _GOV.UK Error Summary: https://design-system.service.gov.uk/components/error-summary/
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
    """
    Helper function to create a table head for :py:meth:`Table`.
    """
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
    """
    Helper function to create a table body for :py:meth:`Table`.
    """
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
    `GOV.UK Table`_ component - use this component to make information easier to compare
    and scan for users.

    Examples:

        >>> table = ds.Table(
        ...     data=[
        ...         {"Name": "Alice", "Age": 30, "City": "London"},
        ...         {"Name": "Bob", "Age": 25, "City": "Manchester"},
        ...     ],
        ...     caption="User Information",
        ...     header_cols=["Name"],
        ...     numeric_cols=["Age"],
        ...     col_width={"Name": "one-third", "Age": "one-sixth", "City": "half"},
        ...     small_text=True,
        ... )
        # Renders table component with caption, header columns, numeric columns, column widths, and small text.
        # ----------------------------------------------
        # | User Information
        # | Name       |  Age  |      City
        # | ----------------------------------------------
        # | Alice      |   30  |     London
        # | Bob        |   25  |  Manchester
        # ----------------------------------------------

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

    .. _GOV.UK Table: https://design-system.service.gov.uk/components/table/
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
    Task component used in :py:meth:`TaskList`.

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
    `GOV.UK TaskList`_ component.

    The task list component displays all the tasks a user needs to do, and allows users
    to easily identify which ones are done and which they still need to do.

    Use the task list if there's evidence that users:

        - do not want to, or cannot, complete all the tasks in one sitting
        - need to be able to choose the order they complete the tasks in

    Examples:

        >>> task_list = ds.TaskList(
        ...     ds.Task("Task 1", href="/task-1", completed=True),
        ...     ds.Task("Task 2", href="/task-2", completed=False, hint="This is a hint."),
        ... )
        # Renders task list component with two tasks.
        # ------------------------------
        # | Task 1            | Completed
        # | Task 2            | Incomplete
        # | This is a hint.
        # ------------------------------

    Args:
        *tasks (FT): Tasks for the TaskList.
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML TaskList component.

    .. _GOV.UK TaskList: https://design-system.service.gov.uk/components/task-list/
    """
    return fh.Ul(
        *[task for task in tasks],
        cls="govuk-task-list",
        **kwargs,
    )


def SummaryItem(key: str, value: str | fh.FT, *actions: fh.FT, **kwargs):
    """
    SummaryRow component - a list of these goes in to form a :py:meth:`SummaryList`.

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
    `GOV.UK Summary List`_ component.

    Use a summary list to summarise information, for example, a user's responses at
    the end of a form.

    :py:meth:`SummaryItem` represents a single row in the summary list, and
    :py:meth:`SummaryCard` is a higher-level component that uses :py:meth:`SummaryList`.

    Examples:

        >>> summary_list = ds.SummaryList(
        ...     ds.SummaryItem("Name", "Alice", ds.A("Change", href="/change-name")),
        ...     ds.SummaryItem("Age", "30", ds.A("Change", href="/change-age")),
        ... )
        # Renders summary list component with two items.
        # ------------------------------
        # | Name       | Alice        | Change
        # | Age        | 30           | Change
        # ------------------------------

    Args:
        *items (FT): List of SummaryItems.
        border (bool, optional): Choose if a border should be drawn. Defaults to True.
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML SummaryList component.

    .. _GOV.UK Summary List: https://design-system.service.gov.uk/components/summary-list/
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
    `GOV.UK Summary Card`_ component.

    If you're showing multiple summary lists on a page, you can show each list within a
    summary card. This lets you visually separate each summary list and give each a title
    and some actions.

    Examples:

        >>> summary_card = ds.SummaryCard(
        ...     title="Your details",
        ...     summary_list=ds.SummaryList(
        ...         ds.SummaryItem("Name", "Alice", ds.A("Change", href="/change-name")),
        ...         ds.SummaryItem("Age", "30", ds.A("Change", href="/change-age")),
        ...     ),
        ...     actions=[ds.A("Delete", href="/delete")],
        ... )
        # Renders summary card component with title, summary list, and actions.
        # ------------------------------
        # | Your details         | Delete
        # | Name       | Alice        | Change
        # | Age        | 30           | Change
        # ------------------------------

    Args:
        title (str): Title of the card.
        summary_list (fh.FT): SummaryList component.
        actions (list[fh.FT], optional): List of card actions. Defaults to None.
        **kwargs: Additional keyword arguments.

    Returns:
        FT: A FastHTML component.

    .. _GOV.UK Summary Card: https://design-system.service.gov.uk/components/summary-list/
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
