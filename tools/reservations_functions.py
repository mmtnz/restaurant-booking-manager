from configuration import database
import datetime as dt
import configuration as conf_vars
from custom_logger import logger
import pandas as pd
import dash_bootstrap_components as dbc
from dash import html


def get_db_reservations_date(date_1, date_2):
    """
    To execute reservation database select query between two dates
    :param date_1: first date
    :param date_2: second date
    :return: tuples list with each row obtained from query
    """

    try:
        select_query = database.select_query(
            table_name=conf_vars.DB_TABLE_NAME,
            where_condition=f"ReservationDay BETWEEN '{date_1}' AND '{date_2}'")
    except Exception as e:
        select_query = []
        logger.error(f"[!] Error executing SELECT query -> {type(e)}: {e}")

    return select_query


def add_new_reservation(reservation_id, reservation_datetime, reservation_number_people,
                        reservation_name, reservation_tables, reservation_obs) -> bool:
    """
    To insert new reservation in the database
    :param reservation_id: reservation identifier
    :param reservation_datetime:
    :param reservation_number_people:
    :param reservation_name:
    :param reservation_tables:
    :param reservation_obs:
    :return: is_error, bool that indicates if there has been any error
    """
    is_error = False
    try:
        database.insert_query(
            table_name=conf_vars.DB_TABLE_NAME,
            values=(reservation_id, reservation_name, reservation_datetime,
                    reservation_number_people, reservation_tables, reservation_obs)
        )
        logger.info(f'[+] Reservation {reservation_id} successfully saved')
    except Exception as e:
        logger.error(f'[!] Error inserting reservation {reservation_id} -> {type(e)}:{e}')
        is_error = True
    return is_error


def edit_reservation(reservation_id, reservation_datetime, reservation_number_people,
                     reservation_name, reservation_tables, reservation_obs):
    """
    To edit reservation data from its Id
    :param reservation_id:
    :param reservation_datetime:
    :param reservation_number_people:
    :param reservation_name:
    :param reservation_tables:
    :param reservation_obs:
    :return: is_error, bool that indicates if there has been any error
    """
    is_error = False
    columns = ['ReservationName', 'ReservationDate', 'ReservationNumber',
               'ReservationTables', 'ReservationObservations']
    values = [reservation_name, reservation_datetime, reservation_number_people,
              reservation_tables, reservation_obs]

    values_str = [f"{columns[i]}='{values[i]}'" for i in range(len(columns))]

    try:
        database.update(
            table_name=conf_vars.DB_TABLE_NAME,
            values_str=values_str,
            condition=f"ReservationId = '{reservation_id}'"
        )
    except Exception as e:
        logger.error(f'[!] Error editing reservation {reservation_id} -> {type(e)}:{e}')
        is_error = True
    return is_error


def delete_reservation(reservation_id):

    """
    To delete a reservation from its Id
    :param reservation_id:
    :return: is_error, bool that indicates if there has been any error
    """
    is_error = False
    try:
        database.delete_query(
            table_name=conf_vars.DB_TABLE_NAME,
            condition=f"ReservationId = '{reservation_id}'"
        )
    except Exception as e:
        logger.error(f'[!] Error deleting reservation {reservation_id} -> {type(e)}:{e}')
        is_error = True
    return is_error


def check_availability(reservation_datetime, num_people):
    """
    To check availability for selected day and number of people
    :param reservation_datetime:
    :param num_people:
    :return:    -bool indicating if it is available
                -string with tables to be used
                -number of free tables (before current reservation), -1 if error
    """

    reservation_day = reservation_datetime
    reservation_day_next = get_next_day_str(reservation_day)
    num_total_tables = conf_vars.NUM_TABLES

    # Get reservations in selected day
    try:
        reservations = database.select_query(
            table_name=conf_vars.DB_TABLE_NAME,
            where_condition=f"ReservationDay BETWEEN '{reservation_day}' and {reservation_day_next}"
        )
    except Exception as e:
        logger.error(f"[!] Error reading database -> {type(e)}: {e}")
        return False, "", -1

    df_reservations = pd.DataFrame(data=reservations, columns=conf_vars.COLUMNS)
    booked_tables_list, num_booked_tables = get_booked_tables(
        tables_list=df_reservations['Table(s)'].tolist(),
        num_total_tables=num_total_tables
    )
    tables_left = num_total_tables - num_booked_tables
    if tables_left <= 0:
        return False, "", tables_left

    tables_str = get_reservation_tables_str(num_booked_tables, num_people)
    return True, tables_str, tables_left


def get_tables_availability(tables_list):
    """
    To check the number of tables already reserved
    Global variables are used to ease number of tables and people per table modification
    :param tables_list: list with each reservation tables id. If it uses more than one table, its ids separated with '-'
    :return: values to pie chart and number of seats left
    """
    num_reserved_tables = 0
    for tables_id in tables_list:
        num_reserved_tables += len(tables_id.split('-'))

    num_available_tables = conf_vars.NUM_TABLES - num_reserved_tables

    # pie_chart_values = [num_reserved_tables, num_available_tables]
    pie_chart_values = [num_available_tables, num_reserved_tables]
    num_seats_left = num_available_tables * conf_vars.NUM_PEOPLE_PER_TABLE

    return pie_chart_values, num_seats_left


def get_reservation_tables_str(num_booked_tables, reservation_num_people):
    """
    To get the table(s) identifier string, they are filled in order
    :param num_booked_tables: number of already reserved tables
    :param reservation_num_people: number of people in current reservation
    :return: string with table(s) identifier
    """

    first_table = num_booked_tables + 1
    num_people_per_table = conf_vars.NUM_PEOPLE_PER_TABLE

    # Check number of tables needed
    num_tables = reservation_num_people/num_people_per_table
    num_tables = int(num_tables) + 1 * (not num_tables.is_integer())

    # Create string
    tables_list = [str(first_table + table_num) for table_num in range(num_tables)]
    tables_str = '-'.join(tables_list)
    return tables_str


def get_next_day_str(date, datetime_format="%Y-%m-%d", is_datetime=False):
    """
    To get the following day in string format
    :param date: current day
    :param datetime_format:
    :param is_datetime: bool to indicate if date is datetime or string
    :return: string with the following day with datetime_format
    """

    if not is_datetime:
        date = dt.datetime.strptime(date, datetime_format)

    next_date = date + dt.timedelta(days=1)
    next_date = next_date.strftime(datetime_format)
    return next_date


def create_datetime_str(reservation_date, reservation_hour, reservation_minute):
    """
     To join date and time in one string
    :param reservation_date:
    :param reservation_hour:
    :param reservation_minute:
    :return: string with date and time
    """
    return f"{reservation_date} {reservation_hour}:{reservation_minute}"


# @@@@ TABLES SCREEN @@@@
def get_booked_tables(tables_list, num_total_tables):
    """
    To find what table is reserved
    :param tables_list: database table(s) column with each reservation's tables
    :param num_total_tables: total number of tables
    :return: boolean list with True if the table is reserved, number of rserved tables
    """

    is_table_reserved_list = [False] * num_total_tables
    num_reserved_tables = 0
    for reservation_tables in tables_list:
        tables = reservation_tables.split('-')
        for table in tables:
            is_table_reserved_list[int(table)-1] = True
            num_reserved_tables += 1
    return is_table_reserved_list, num_reserved_tables


def get_tables_class_name_list(df_reservations, num_tables):
    """
    To get each table class name according to his availability (for style)
    :param df_reservations: dataframe with reservations on selected date
    :param num_tables: max number of tables available
    :return: list with class names
    """
    tables_class_name_list = ['table-free'] * num_tables

    # Boolean list indicating if table is reserved
    is_table_reserved_list = get_booked_tables(
        tables_list=df_reservations['Table(s)'].tolist(),
        num_total_tables=num_tables
    )

    # Change class in reserved tables
    for index in range(num_tables):
        if is_table_reserved_list[index]:
            tables_class_name_list[index] = 'table-reserved'

    return tables_class_name_list


def get_popover(name, time, observations, index):
    """
    To get popover shown while hovering or clicking a table
    It contains reservation info
    :param name:
    :param time:
    :param observations:
    :param index:
    :return: popover dbc object
    """

    popover = dbc.Popover(
        [
            dbc.PopoverHeader(f"Name: {name}"),
            dbc.PopoverBody(
                [
                    html.Label(f"- Time: {time}", className='m-2'),
                    html.Br(),
                    html.Label(f"- Observations: {observations}", className='m-2')
                ]
            ),

        ],
        target=f"table-{index}", trigger='click hover', placement='right',
        className="table-info-pop", id=f"table-{index}-popover"
    )
    return popover


def get_table_name_list_and_popovers(df_reservations, num_tables: int):
    """
    To obtain each table name and its respective popover with reservation info
    :param df_reservations: dataframe with reservation on selected day
    :param num_tables: total number of tables
    :return: list with div names and list with popovers
    """
    # Initialize -> Default table name
    table_name_list = [html.H5(f'Table {i + 1}', className='reservation-table-text') for i in range(num_tables)]
    popovers_list = []

    # If table reserved update name and create popover with reservation info
    for i in range(num_tables):
        search_result = df_reservations[df_reservations['Table(s)'].str.contains(f'{i+1}')]
        if len(search_result) > 0:
            name = search_result['Name'].values[0]
            time = search_result['Day'].values[0]
            time = pd.Timestamp(time).time().strftime("%H:%M")
            observations = search_result['Observations'].values[0]

            table_name_list[i] = html.Div(
                [
                    html.H5(f"Table {i + 1}"),
                    html.H5(f"{name}"),
                ], className='table-text-div'
            )

            popover = get_popover(name, time, observations, index=i+1)
            popovers_list.append(popover)

    if len(popovers_list) == 0:
        popovers_list = [None]

    return table_name_list, popovers_list


def get_tables_screen_callback_outputs(df_reservations, num_tables: int):
    """
    To obtain the callback outputs of tables screen. These are:
        - each table class name: table-reserved or table-free (for styling)
        - each table name: Name to be shown over the table
        - popovers: popovers that will appear when cursor is hovering a reserved table
    :param df_reservations:
    :param num_tables:
    :return: callbacks list
    """

    # List with table class name (for styling)
    tables_class_name_list = get_tables_class_name_list(df_reservations, num_tables)

    # Find reserved table reservation data to show and for pop over
    table_name_list, popovers_list = get_table_name_list_and_popovers(
        df_reservations=df_reservations,
        num_tables=num_tables
    )

    # Group all callbacks in an unique list
    callback_list = tables_class_name_list + table_name_list
    callback_list.append(popovers_list)
    return callback_list
