import uuid
from flask import Flask
import dash
from dash import Output, Input, State, ctx
from pages import sidebar
from tools import *
import datetime as dt
from dash import dcc

server = Flask(__name__)
app = dash.Dash(
    name=__name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP, dbc.icons.FONT_AWESOME
    ],
    meta_tags=[{'name': 'viewport',
                'content': 'width=device-width, initial-scale=1.0'}],
    server=server,
    use_pages=True)
app.config['suppress_callback_exceptions'] = True
app.layout = sidebar.layout

""" @@@@@@@ CALLBACKS @@@@@@@ """
COLUMNS = conf_vars.COLUMNS

""" @@@@ TABLES PAGE CALLBACKS @@@@ """
outputs_table_status = [Output(f"table-{i+1}", "className") for i in range(20)]
outputs_table_name = [Output(f"table-{i+1}", "children") for i in range(20)]
outputs_popover_trigger = [Output(f"row-for-popovers", "children")]
outputs_list = outputs_table_status + outputs_table_name + outputs_popover_trigger


@app.callback(
    outputs_list,
    Input("tables-screen-date-picker", "date"),
    prevent_initial_callback=True
)
def show_booked_tables(date):
    """
    To show reserved tables visually
    :param date: selected date
    :return:
    """
    # Database query
    next_date = get_next_day_str(date)
    select_query = get_db_reservations_date(date_1=date, date_2=next_date)

    df = pd.DataFrame(select_query, columns=COLUMNS)
    df['Day'] = pd.to_datetime(df['Day'])

    callbacks_list = get_tables_screen_callback_outputs(
        df_reservations=df,
        num_tables=conf_vars.NUM_TABLES
    )
    return callbacks_list


""" @@@@ RESERVATIONS PAGE CALLBACKS @@@@ """


@app.callback(
    [Output("add-reservation-modal", "is_open"), Output("day-add-reservation-modal", "children")],
    [Input("add-reservation-button", "n_clicks"), Input("modal-cancel-button", "n_clicks")],
    State("reservation-date-picker", "date"),
    prevent_initial_call=True
)
def open_close_add_modal(n_clicks_open, n_clicks_close, date):
    """
    To open and close the add new reservation modal
    :param n_clicks_open:
    :param n_clicks_close:
    :param date: selected date
    :return: state of add reservation modal (open/close) and its day title
    """
    date_str = dt.datetime.strptime(date, "%Y-%m-%d").strftime("%d %B, %Y")
    if ctx.triggered_id == 'add-reservation-button':
        return True, date_str
    if ctx.triggered_id == 'modal-cancel-button':
        return False, dash.no_update


MODAL_ITEMS = ['name', 'number', 'hour', 'minute', 'observations']
outputs_call = [Output(f"{item}-edit-reservation-modal", "value") for item in MODAL_ITEMS]
outputs_call += [Output("day-edit-reservation-modal", "children"),
                 Output("edit-reservation-modal", "is_open")]


@app.callback(
    outputs_call,
    [Input("edit-reservation-button", "n_clicks"),
     Input("edit-modal-cancel-button", "n_clicks")],
    [State("reservation-table", prop) for prop in ["active_cell, data"]],
    prevent_initial_call=True
)
def open_edit_modal(n_clicks_open, n_clicks_close, active_cell, table_data):
    """
    To open and close the edit reservation modal
    :param n_clicks_open:
    :param n_clicks_close:
    :param active_cell: index data of selected reservation on table
    :param table_data: all reservations table data (for selected day)
    :return: edit modal fields filled with reservation data from table
    """

    if ctx.triggered_id == 'edit-modal-close-button':
        return [dash.no_update] * 6 + [False]

    # When it is open, data of selected reservation is showed
    reservation_data = table_data[active_cell['row']]
    reservation_name = reservation_data['Name']
    reservation_number = reservation_data['Number of people']
    reservation_obs = reservation_data['Observations']
    date_datetime = dt.datetime.strptime(reservation_data['Day'], "%Y-%m-%d %H:%M")
    date_str = date_datetime.strftime("%d %B, %Y")
    reservation_hour = str(date_datetime.hour).zfill(2)
    reservation_minute = str(date_datetime.minute).zfill(2)

    return reservation_name, reservation_number, reservation_hour, reservation_minute,\
        reservation_obs, date_str, True


@app.callback(
    [Output("reservation-table", "style_data_conditional"),
     Output("edit-reservation-button", "disabled"),
     Output("remove-reservation-button", "disabled")],
    Input("reservation-table", "active_cell"),
    prevent_initial_call=True
)
def highlight_row_and_active_button(active_cell_dict):
    """
    To highlight the whole row when clicking a cell and to activate edit and remove buttons
    :param active_cell_dict: selected cell
    :return: conditional style for that row
    """

    selected_row = active_cell_dict['row']
    conditional = [
        {
            'if': {
                'row_index': selected_row
            },
            'backgroundColor': conf_vars.COLOR_BLUE,
            'color': conf_vars.COLOR_DARK_THING,
            'border': f'1px solid {conf_vars.COLOR_DARK_THING}'
        },
        {
            'if': {
                'state': 'selected'
            },
            'backgroundColor': conf_vars.COLOR_BLUE,
            'color': conf_vars.COLOR_DARK_THING,
            'border': f'1px solid {conf_vars.COLOR_DARK_THING}'
        }
    ]
    return conditional, False, False


@app.callback(
    [Output("reservation-table", "data"), Output("percentage-graph-div", "children"),
     Output("add-reservation-button", "disabled")],
    Input("reservation-date-picker", "date"),
)
def update_reservations_table(date):
    """
    To update reservations table and pie chart indicating occupation
    :param date: selected date
    :return: updated reservations table and percentage pie-chart
    """
    if date is None:  # Default chart
        graph = dcc.Graph(
            figure=get_reservations_percentage_pie(
                values=[conf_vars.NUM_TABLES, 0],
                seats_left='-'
            )
        )
        return dash.no_update, graph, dash.no_update

    # Database query
    next_date = get_next_day_str(date)
    select_query = get_db_reservations_date(date_1=date, date_2=next_date)

    df = pd.DataFrame(select_query, columns=COLUMNS)
    df['Day'] = pd.to_datetime(df['Day'])
    df['Day'] = df['Day'].dt.strftime('%Y-%m-%d %H:%M')
    data = df.to_dict('records')
    pie_chart_values, num_seats_left = get_tables_availability(list(df['Table(s)']))
    graph = dcc.Graph(
        figure=get_reservations_percentage_pie(
            values=pie_chart_values,
            seats_left=num_seats_left
        )
    )

    return data, graph, False


# Callback states
state_items = [State(f"{item}-add-reservation-modal", "value") for item in MODAL_ITEMS]
state_items += [State("reservation-date-picker", "date")]


@app.callback(
    [Output("successful-add-alert", f"{prop}")
     for prop in ["children", "is_open", "color"]],
    Input("modal-add-button", "n_clicks"),
    state_items,
    prevent_initial_call=True
)
def add_reservation_callback(nc, reservation_name, reservation_number_people,
                             reservation_hour, reservation_minute, reservation_obs,
                             reservation_date):
    """
    To add (if there is availability) the new reservation to the database
    :param nc:
    :param reservation_name:
    :param reservation_number_people:
    :param reservation_hour:
    :param reservation_minute:
    :param reservation_obs:
    :param reservation_date:
    :return: alert message indicating if the action has been successfully completed or not
    """

    is_available, tables_str, tables_left = check_availability(
        num_people=reservation_number_people,
        reservation_datetime=reservation_date
    )

    if is_available:
        reservation_datetime = create_datetime_str(reservation_date, reservation_hour,
                                                   reservation_minute)
        reservation_id = str(uuid.uuid4())
        is_error = add_new_reservation(
            reservation_id=reservation_id,
            reservation_name=reservation_name,
            reservation_datetime=reservation_datetime,
            reservation_number_people=reservation_number_people,
            reservation_tables=tables_str,
            reservation_obs=reservation_obs
        )

        if not is_error:
            banner_msg = f"Reservation {reservation_id} successfully added"
            banner_color = "success"
        else:
            banner_msg = f"Error adding reservation"
            banner_color = "danger"

    else:
        if tables_left == -1:  # error
            banner_msg = f"Error connecting with database"
        else:
            banner_msg = f"Error adding reservation," \
                         f"{tables_left} tables left ({tables_left} per table)"
        banner_color = "danger"

    return banner_msg, True, banner_color


# State items updated
state_items += [State("reservation-table", prop) for prop in ["active_cell, data"]]


@app.callback(
    [Output("successful-edit-alert", f"{prop}")
     for prop in ["children", "is_open", "color"]],
    Input("edit-modal-add-button", "n_clicks"),
    state_items,
    prevent_initial_call=True
)
def edit_reservation_callback(nc, reservation_name, reservation_number_people,
                              reservation_hour, reservation_minute, reservation_obs,
                              reservation_date, active_cell, table_data):
    """
    To edit an already saved reservation
    :param nc:
    :param reservation_name:
    :param reservation_number_people:
    :param reservation_hour:
    :param reservation_minute:
    :param reservation_obs:
    :param reservation_date:
    :param active_cell: coordinates of cell selected
    :param table_data: reservations of selected date
    :return: alert message indicating if the action has been successfully completed or not
    """
    reservation_data = table_data[active_cell['row']]
    reservation_id = reservation_data['Id']
    reservation_tables = reservation_data['Table(s)']
    reservation_datetime = create_datetime_str(reservation_date, reservation_hour,
                                               reservation_minute)
    is_error = edit_reservation(
        reservation_id=reservation_id,
        reservation_datetime=reservation_datetime,
        reservation_number_people=reservation_number_people,
        reservation_name=reservation_name,
        reservation_tables=reservation_tables,
        reservation_obs=reservation_obs
    )

    if not is_error:
        banner_msg = f"Reservation {reservation_id} successfully edited"
        banner_color = "success"
    else:
        banner_msg = f"Error adding reservation"
        banner_color = "danger"

    return banner_msg, True, banner_color


@app.callback(
    Output("modal-add-button", "disabled"),
    [Input(f"{field}-add-reservation-modal", "value") for field in ["name", "number"]],
    prevent_initial_call=True
)
def activate_add_button(reservation_name, reservation_number_people):
    """
    To enable add button only when reservation data is filled
    :param reservation_name:
    :param reservation_number_people:
    :return: state of add button (enabled/disabled)
    """

    if (reservation_name is not None and len(reservation_name) > 0) and (
            reservation_number_people is not None and reservation_number_people > 0):
        return False
    else:
        return True


""" @@@@ statistics PAGE CALLBACKS @@@@ """


# @app.callback(
#     [Output("histogram-month", "figure"), Output("pie-graph-month-div", "children")],
#     [Input("statistics-date-picker", prop) for prop in ["start_date", "end_date"]],
# )
# def update_month_graphs(start_date, end_date):
#     """
#     To update graphs in static month tab
#     :param start_date:
#     :param end_date:
#     :return: month histogram and pie chart
#     """
#
#     histogram_title = "People per month"
#
#     if start_date is None or end_date is None:
#         histogram, pie_chart = get_empty_graphs(histogram_title)
#         return histogram, pie_chart
#
#     df_query = get_db_reservations_date(start_date, end_date)
#     histogram = update_histogram_month(start_date, end_date, df_query, histogram_title)
#     pie_chart = update_pie_month(start_date, end_date, df_query)
#     return histogram, pie_chart
#
#
# @app.callback(
#     [Output("histogram-week", "figure"), Output("pie-graph-week-div", "children")],
#     [Input("statistics-date-picker", prop) for prop in ["start_date", "end_date"]]
# )
# def update_week_graphs(start_date, end_date):
#     """
#     To update graphs in static week tab
#     :param start_date:
#     :param end_date:
#     :return: week histogram and pie chart
#     """
#     histogram_title = "People per day of the week"
#     if start_date is None or end_date is None:
#         histogram, pie_chart = get_empty_graphs(histogram_title)
#         return histogram, pie_chart  # Default graphs appearance
#
#     df_query = get_db_reservations_date(start_date, end_date)
#     histogram = update_histogram_week(start_date, end_date, df_query, histogram_title)
#     pie_chart = update_pie_week(start_date, end_date, df_query)
#     return histogram, pie_chart


@app.callback(
    [Output("histogram-week", "figure"), Output("pie-graph-week-div", "children"),
     Output("histogram-month", "figure"), Output("pie-graph-month-div", "children")],
    [Input("statistics-date-picker", prop) for prop in ["start_date", "end_date"]]
)
def update_statistics_graphs(start_date, end_date):
    """
    To update graphs in statistics page
    :param start_date:
    :param end_date:
    :return:
    """
    histogram_title_month = "People per month"
    histogram_title_week = "People per week"

    if start_date is None or end_date is None:
        histogram_month, pie_chart_month = get_empty_graphs(histogram_title_month)
        histogram_week, pie_chart_week = get_empty_graphs(histogram_title_week)
        return histogram_month, pie_chart_month, histogram_week, pie_chart_week

    df_query = get_db_reservations_date(start_date, end_date)
    histogram_month = update_histogram_month(start_date, end_date, df_query,
                                             histogram_title_month)
    pie_chart_month = update_pie_month(start_date, end_date, df_query)
    histogram_week = update_histogram_week(start_date, end_date, df_query,
                                           histogram_title_week)
    pie_chart_week = update_pie_week(start_date, end_date, df_query)
    return histogram_month, pie_chart_month, histogram_week, pie_chart_week


# @@@@@ statistics @@@@@
histogram_query_dict = [
        ("mario", dt.datetime(2022, 10, 21, 11, 30), 3, "1", ""),
        ("mario", dt.datetime(2022, 10, 21, 12, 30), 7, "2-3", ""),
        ("mario", dt.datetime(2022, 10, 21, 11, 45), 5, "4", ""),
        ("mario", dt.datetime(2022, 10, 22, 14, 30), 2, "5", ""),
        ("mario", dt.datetime(2022, 10, 21, 15, 30), 10, "6-7", ""),
        ("mario", dt.datetime(2022, 10, 21, 16, 30), 5, "8", ""),
        ("mario", dt.datetime(2022, 10, 21, 16, 30), 5, "9", ""),
        ("mario", dt.datetime(2022, 10, 25, 16, 30), 5, "10", ""),
        ("mario", dt.datetime(2022, 10, 15, 16, 30), 11, "11-12", ""),
        ("mario", dt.datetime(2022, 10, 21, 16, 30), 10, "13-14", ""),
        ("mario", dt.datetime(2022, 10, 28, 16, 30), 10, "13-14", ""),
        ("mario", dt.datetime(2022, 10, 21, 16, 30), 10, "13-14", ""),
        ("mario_2", dt.datetime(2022, 10, 21, 11, 30), 3, "1", ""),
        ("mario_2", dt.datetime(2022, 10, 21, 12, 30), 7, "2-3", ""),
        ("mario_2", dt.datetime(2022, 10, 30, 11, 45), 5, "4", "all"),
        ("mario_2", dt.datetime(2022, 10, 21, 14, 30), 2, "5", ""),
        ("mario_2", dt.datetime(2022, 10, 21, 15, 30), 10, "6-7", ""),
]

select_query_dict = {
    "2022-09-21": [
        ("mario", dt.datetime(2022, 10, 21, 11, 30), 3, "1", ""),
        ("mario", dt.datetime(2022, 10, 21, 12, 30), 7, "2-3", ""),
        ("mario", dt.datetime(2022, 10, 21, 11, 45), 5, "4", ""),
        ("mario", dt.datetime(2022, 10, 21, 14, 30), 2, "5", ""),
        ("mario", dt.datetime(2022, 10, 21, 15, 30), 10, "6-7", ""),
        ("mario", dt.datetime(2022, 10, 21, 16, 30), 5, "8", ""),
        ("mario", dt.datetime(2022, 10, 21, 16, 30), 5, "9", ""),
        ("mario", dt.datetime(2022, 10, 21, 16, 30), 5, "10", ""),
        ("mario", dt.datetime(2022, 10, 21, 16, 30), 11, "11-12", ""),
        ("mario", dt.datetime(2022, 10, 21, 16, 30), 10, "13-14", ""),
        ("mario", dt.datetime(2022, 10, 21, 16, 30), 10, "13-14", ""),
        ("mario", dt.datetime(2022, 10, 21, 16, 30), 10, "13-14", ""),
    ],
    "2022-09-22": [
        ("mario_2", dt.datetime(2022, 10, 21, 11, 30), 3, "1", ""),
        ("mario_2", dt.datetime(2022, 10, 21, 12, 30), 7, "2-3", ""),
        ("mario_2", dt.datetime(2022, 10, 21, 11, 45), 5, "4", "all"),
        ("mario_2", dt.datetime(2022, 10, 21, 14, 30), 2, "5", ""),
        ("mario_2", dt.datetime(2022, 10, 21, 15, 30), 10, "6-7", ""),
    ]
}

if __name__ == '__main__':
    app.run_server(port=8051, debug=True)
