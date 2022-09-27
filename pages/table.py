import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import os
from PIL import Image
import datetime as dt


layout = html.Div(children=[
    dbc.Row(
        dbc.Col(
            html.Div(
                dcc.DatePickerSingle(
                    id='tables-screen-date-picker',
                    placeholder='Select a day',
                    date=dt.date.today()
                ),
                className='my-4'
            ),
            width={"offset": 2}
        ),
    ),
    dbc.Row(
        [
            dbc.Col(
                [

                    html.Div(f"Table-{i+1+(j*5)}", id=f"table-{i+1+(j*5)}",
                             className="table-reserved")
                    for i in range(5)
                ],
                className="table-row-div col-8 mb-3",
                width=dict(offset=2)
            )
            for j in range(4)
        ], className='my-5'
    ),
    dbc.Row(
        [
            dbc.Popover(
                [
                    dbc.PopoverHeader("Name"),
                    dbc.PopoverBody("Reservation time",),
                    dbc.PopoverBody("Reservation obs"),
                ],
                target=f"table-{i+1}", trigger=None,
                className="table-info-pop", id=f"table-{i+1}-popover"
            )
            for i in range(20)
        ], id="row-for-popovers"
    )
])

dash.register_page(os.path.basename(__file__), name='Table', path="/table", layout=layout)
