import dash
from dash import html
import dash_bootstrap_components as dbc
import configuration as config_vars


sidebar = html.Div(
            [
                html.Div(
                    [
                        html.I(className="bi bi-book me-3",
                               style={"padding-left": '12px', "font-size": "1.5em"}),
                        html.Span("Restaurant Name", className='sidebar_title'),
                    ],
                    className="sidebar-header",
                ),
                html.Hr(),
                dbc.Nav(
                    [
                        dbc.NavLink(
                            [html.I(className="bi bi-calendar-week me-2"),
                             html.Span("Reservations")],
                            href='/table',
                            active="partial",
                        ),
                        dbc.NavLink(
                            [html.I(className="bi bi-calendar-plus me-2"),
                             html.Span("Edit reservations")],
                            href='/reservations',
                            active="partial",
                        ),
                        dbc.NavLink(
                            [html.I(className="bi bi-bar-chart-line-fill me-2"),
                             html.Span("statistics")],
                            href='/statistics',
                            active="partial",

                        ),
                    ],
                    vertical=True,
                    pills=True,
                ),
                html.Div(f'Software Version {config_vars.SW_VERSION}',
                         className='text_sidebar_footer1')
            ],
            className="sidebar",
        )

layout = html.Div(children=[

    dbc.Row(sidebar),
    dash.page_container,
])
