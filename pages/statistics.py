import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import os


tab_month = dbc.Row(
    [
        dbc.Col(dcc.Graph(id="histogram-month"), lg=5, md=5),
        dbc.Col(id="pie-graph-month-div", width={"offset": 1}, lg=5, md=5)
    ]
)
tab_week = dbc.Row(
    [
        dbc.Col(dcc.Graph(id="histogram-week"), lg=5, md=5),
        dbc.Col(id="pie-graph-week-div", width={"offset": 1}, lg=5, md=5)
    ]
)

layout = html.Div(children=[
    dbc.Row(
        dbc.Col(
            [
                html.H5("Date:"),
                dcc.DatePickerRange(
                    id='statistics-date-picker',
                    className="custom-day-picker",
                    start_date_placeholder_text='First day',
                    end_date_placeholder_text='Last day',
                    clearable=True,
                    first_day_of_week=1
                )
            ],
            width=dict(offset=2),
            lg=6, md=6, className='my-4'
        )
    ),
    dbc.Row(
        dbc.Col(
            dbc.Tabs(
                [
                    dbc.Tab(tab_week, label="Week statistics"),
                    dbc.Tab(tab_month, label="Month statistics"),
                ],
                className="statistics-tab"
            ),
            width={"offset": 2}
        )
    ),
])

dash.register_page(os.path.basename(__file__), name='statistics', path="/statistics", layout=layout)
