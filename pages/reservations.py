import dash
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import os
from PIL import Image
import pandas as pd
import configuration as conf_vars
import datetime as dt


add_reservation_modal = dbc.Modal(
    [
        dbc.ModalHeader(html.H4("Add new reservation")),
        dbc.ModalBody(
            [
                dbc.Alert("mensaje", id="successful-add-alert", is_open=False,
                          duration=10000, dismissable=True, className='mx-3'),
                dbc.Row(
                    [
                        html.H5("Day:", className='col-3 px-3'),
                        html.H5(className='col-8', id="day-add-reservation-modal")
                    ], className='mb-3'
                ),
                dbc.Row(
                    [
                        html.H5("Name:", className='col-3 px-3'),
                        dcc.Input(id="name-add-reservation-modal", className='modal-input col-8',
                                  type='text', placeholder="Write name"),
                    ], className='mb-3'
                ),
                dbc.Row(
                    [
                        html.H5("Time:", className='col-3 px-3'),
                        html.Div(
                            [
                                dcc.Dropdown([str(h).zfill(2) for h in range(0, 24)], '00', className='time-dropdown', id='hour-add-reservation-modal'),
                                html.Div(":", style={"width": "fit-content", "padding": "1px"}),
                                dcc.Dropdown([str(m).zfill(2) for m in range(0, 60)], '00', className='time-dropdown', id='minute-add-reservation-modal'),
                            ], className='col-8', id="div-for-time"
                        ),
                    ], className='mb-3'
                ),
                dbc.Row(
                    [
                        html.H5("Number:", className='col-3 px-3'),
                        dcc.Input(id="number-add-reservation-modal", className='modal-input col-8',
                                  type='number', placeholder="Select number of people",
                                  min=0, max=conf_vars.NUM_TABLES * conf_vars.NUM_PEOPLE_PER_TABLE)
                    ], className='mb-3'
                ),
                dbc.Row(
                    [
                        html.H5("Observations:", className='col-3 px-3'),
                        dcc.Input(id="observations-add-reservation-modal", className='modal-input col-8',
                                  type='text', placeholder="(Allergies, children, birthdays ...)")

                    ], className='mb-3'
                ),
            ]
        ),
        dbc.ModalFooter(
            [
                html.Button("Add", id="modal-add-button", className="button-green button-modal", disabled=True),
                html.Button("Cancel", id="modal-cancel-button", className="button-dark button-modal"),
            ]
        )
    ],
    id="add-reservation-modal", is_open=False, centered=True, size='lg'
)

edit_reservation_modal = dbc.Modal(
    [
        dbc.ModalHeader(html.H4("Edit reservation")),
        dbc.ModalBody(
            [
                dbc.Alert("mensaje", id="successful-edit-alert", is_open=False,
                          duration=10000, dismissable=True, className='mx-3'),
                dbc.Row(
                    [
                        html.H5("Day:", className='col-3 px-3'),
                        html.H5(className='col-8', id="day-edit-reservation-modal")
                    ], className='mb-3'
                ),
                dbc.Row(
                    [
                        html.H5("Name:", className='col-3 px-3'),
                        dcc.Input(id="name-edit-reservation-modal", className='modal-input col-8',
                                  type='text', placeholder="Write name"),
                    ], className='mb-3'
                ),
                dbc.Row(
                    [
                        html.H5("Time:", className='col-3 px-3'),
                        html.Div(
                            [
                                dcc.Dropdown([str(h).zfill(2) for h in range(0, 24)], '00',
                                             className='time-dropdown', id='hour-edit-reservation-modal'),
                                html.Div(":", style={"width": "fit-content", "padding": "1px"}),
                                dcc.Dropdown([str(m).zfill(2) for m in range(0, 60)], '00',
                                             className='time-dropdown', id='minute-edit-reservation-modal'),
                            ], className='col-8 div-for-time'
                        ),
                    ], className='mb-3'
                ),
                dbc.Row(
                    [
                        html.H5("Number:", className='col-3 px-3'),
                        dcc.Input(id="number-edit-reservation-modal", className='modal-input col-8',
                                  type='number', placeholder="Select number of people",
                                  min=0, max=conf_vars.NUM_TABLES * conf_vars.NUM_PEOPLE_PER_TABLE)
                    ], className='mb-3'
                ),
                dbc.Row(
                    [
                        html.H5("Observations:", className='col-3 px-3'),
                        dcc.Input(id="observations-edit-reservation-modal", className='modal-input col-8',
                                  type='text', placeholder="(Allergies, children, birthdays ...)")

                    ], className='mb-3'
                ),
            ]
        ),
        dbc.ModalFooter(
            [
                html.Button("Update", id="edit-modal-add-button", className="button-green button-modal", disabled=False),
                html.Button("Cancel", id="edit-modal-cancel-button", className="button-dark button-modal"),
            ]
        )
    ],
    id="edit-reservation-modal", is_open=False, centered=True, size='lg'
)

COLUMNS = ["Id", "Name", "Day", "Number of people", "Table(s)", "Observations"]
BUTTONS = ["add", "edit", "remove"]

layout = html.Div(
    [
        add_reservation_modal,
        edit_reservation_modal,

        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                html.H5("Day:"),
                                dcc.DatePickerSingle(
                                    id='reservation-date-picker',
                                    placeholder='Select a day',
                                    className="custom-day-picker",
                                    date=dt.date.today(),
                                )
                            ]
                        ),
                        dbc.Row(
                            [
                                html.Button(button_name, id=f"{button_name}-reservation-button",
                                            style={"width": "fit-content"},
                                            className="reservation-button button-dark",
                                            disabled=True)
                                for button_name in BUTTONS

                            ],
                            className="div-for-buttons"
                        ),
                        dbc.Row(
                            dash_table.DataTable(
                                id='reservation-table',
                                columns=[{"name": c, "id": c} for c in COLUMNS],
                                # fixed_rows={'headers': True},
                                sort_action='native',
                                style_header={
                                            'backgroundColor': conf_vars.COLOR_GREEN,
                                            'color': conf_vars.COLOR_DARK,
                                            'border': f'1px solid {conf_vars.COLOR_DARK_THING}'
                                        },
                                style_cell={
                                            'textAlign': 'left',
                                            'maxWidth': 'auto',
                                },
                                style_data={
                                            'backgroundColor': conf_vars.COLOR_DARK_THING,
                                            'color': "white"
                                },
                                style_cell_conditional=[{
                                    'if': {'column_id': 'Id'},
                                    'display': 'None'
                                }]
                            ),
                        )
                    ],
                    id="reservation_table_div",
                    width={"offset": 2},
                    lg=5, md=5,
                ),
                dbc.Col(id="percentage-graph-div", lg=5, md=5,),
            ]
        )
    ]
)

dash.register_page(os.path.basename(__file__), name='Reservations', path="/reservations", layout=layout)
