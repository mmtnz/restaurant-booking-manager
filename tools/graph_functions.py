import plotly.graph_objects as go
import configuration as conf_vars
import pandas as pd
import datetime as dt
from dash import dcc


def get_histogram_layout(x_val, y_val):
    """
    To obtain layout of histogram graphic object
    :param x_val: list with the label of each bar (axis x)
    :param y_val: list with the value of each bar (axis y)
    :return: graphic object layout
    """

    histogram_layout = go.Layout(
        margin=go.layout.Margin(l=10, r=0, t=0, b=50),
        showlegend=False,
        plot_bgcolor=conf_vars.COLOR_DARK_THING,
        paper_bgcolor=conf_vars.COLOR_DARK_THING,
        dragmode="select",
        font=dict(color="white"),
        xaxis=dict(
            showgrid=False,
            autorange=True,
        ),
        yaxis=dict(
            range=[0, max(y_val) + max(y_val) / 4],
            showticklabels=False,
            showgrid=False,
            fixedrange=True,
            rangemode="nonnegative",
            zeroline=True,
        ),
        annotations=[
            dict(
                x=xi,
                y=yi,
                text=str(yi),
                xanchor="center",
                yanchor="bottom",
                showarrow=False,
                font=dict(color="white"),
            )
            for xi, yi in zip(x_val, y_val)
        ]
    )
    return histogram_layout


def get_histogram(x_val: list, y_val: list, color_val: list, title: str):
    """
    To create custom histogram graphic object
    :param x_val: axis x values -> label for each bar
    :param y_val: axis y values -> value for each bar
    :param color_val: color for each bar
    :param title: histogram title
    :return: histogram graphic object
    """
    histogram = go.Figure(
        data=[
            go.Bar(x=x_val, y=y_val, marker=dict(color=color_val), hoverinfo="x", width=0.8),
            go.Scatter(
                opacity=0,
                x=x_val,
                y=y_val / 2,
                hoverinfo="none",
                mode="markers",
                marker=dict(color="rgb(66, 134, 244, 0)", symbol="square", size=40),
                visible=True,
            ),
        ],
        layout=get_histogram_layout(x_val, y_val),
    )
    histogram.update_layout(title=dict(
        text=title,
        x=0.5,
        y=0.95,
        font=dict(color="white"),))

    return histogram


# @@@ PIE-CHART-GRAPH @@@
def get_statistics_percentage_pie(values, labels):
    """
    To obtain statics percentage pie
    :param values: list with values
    :param labels: list with each value respective name/label
    :return: pie-chart graphic object
    """

    colors = [conf_vars.COLOR_GREEN, conf_vars.COLOR_DARK_GREEN, conf_vars.COLOR_DARK_THING,
              conf_vars.COLOR_LIGHT_GREEN_1, conf_vars.COLOR_LIGHT_GREEN_2, 'white',
              conf_vars.COLOR_SEMI_DARK_GREEN_1, conf_vars.COLOR_SEMI_DARK_GREEN_2, conf_vars.COLOR_SEMI_DARK_GREEN_3,
              conf_vars.COLOR_SEMI_DARK_GREEN_4, conf_vars.COLOR_SEMI_DARK_GREEN_5, conf_vars.COLOR_SEMI_DARK_GREEN_6]

    # Mode: Item that repeats the most
    try:
        mode_font_size = 60
        mode_index = [index for index, item in enumerate(values) if item == max(values)]
        mode_annotation = labels[mode_index[0]]
    except Exception as e:
        print(e)
        a = 1

    # If there are months with same number of visits
    if len(mode_index) > 1:
        mode_font_size /= len(mode_index)
        for m in range(1, len(mode_index)):
            mode_annotation += f", {mode_index[m]}"

    pie_fig = go.Figure(data=[go.Pie(values=values, hole=0.9, labels=labels)])
    pie_fig.update_layout(showlegend=False,
                          annotations=[dict(text=mode_annotation, font_size=mode_font_size, font_color="white",
                                            x=0.5, y=0.55, showarrow=False),
                                       dict(text='More visited',
                                            x=0.5, y=0.3, font_size=20, font_color="white", showarrow=False),
                                       ],
                          paper_bgcolor='rgba(0,0,0,0)',
                          ),
    pie_fig.update_traces(marker=dict(colors=colors[:len(labels)]),
                          textfont_size=13, textfont_color="white", textinfo="percent+label")
    return pie_fig


def get_reservations_percentage_pie(values, seats_left):
    """
    To obtain reservations percentage pie with occupation
    :param values: list with values
    :param seats_left: number of seats left
    :return: pie-chart graphic object
    """
    pie_fig = go.Figure(data=[go.Pie(values=values, hole=0.9, labels=['Available tables', 'Reserved tables'])])
    pie_fig.update_layout(showlegend=False,
                          annotations=[dict(text=seats_left,
                                            x=0.5, y=0.55, font_size=60, font_color="white", showarrow=False),
                                       dict(text='seats left',
                                            x=0.5, y=0.3, font_size=20, font_color="white", showarrow=False),
                                       ],
                          paper_bgcolor='rgba(0,0,0,0)',
                          ),
    pie_fig.update_traces(marker=dict(colors=[conf_vars.COLOR_DARK_THING, conf_vars.COLOR_GREEN]),
                          textfont_size=15, textfont_color="white", textinfo="value+label")
    return pie_fig


# @@@ HISTOGRAM-VALUES @@@
def get_number_per_month_histogram(df, start_date, end_date):
    """
    To count the number of people on each month (separated by years)
    :param df: dataframe with reservations
    :param start_date:
    :param end_date:
    :return: year dict with a list with number of people each month (order: January to December)
    """

    if len(df) > 0:
        # Convert df into a list of dictionaries to search by key
        list_items = df.to_dict('records')
    else:
        list_items = []

    number_per_month = []
    start_year = start_date.year
    end_year = end_date.year
    start_month_index = start_date.month - 1
    end_month_index = end_date.month - 1

    # Initialize dict with a 0 * 12 month list for each year key
    number_per_month_dict = {year: [0] * 12 for year in range(start_year, end_year + 1)}

    # Fill dictionary with df number of people values
    for item in list_items:
        month = item['Day'].month - 1  # Index start at 0
        year = item['Day'].year
        number_per_month_dict[year][month] += item['Number of people']

    # Remove unnecessary months in start_year and end_year (it could be the same year)
    for year, month_list in number_per_month_dict.items():
        if year == start_year and year == end_year:  # Only one year selected
            number_per_month += month_list[start_month_index:end_month_index+1]
        elif year == start_year and year != end_year:  # Add month list of first year
            number_per_month += month_list[start_month_index:]
        elif year == end_year and year != start_year:  # Add month list of last year
            number_per_month += month_list[:end_month_index+1]

    return number_per_month


def get_number_per_day_of_week_histogram(df, start_date, end_date):
    """
    To count the number of people on each day of week (grouped by months)
    :param df: dataframe with reservations
    :param start_date:
    :param end_date:
    :return: month list with number of people each day of week (order: Monday to Sunday)
    """

    if len(df) > 0:
        # Convert df into a list of dictionaries to search by key
        list_items = df.to_dict('records')
    else:
        list_items = []

    number_per_day_of_week = []
    start_year = start_date.year
    end_year = end_date.year
    start_month_index = start_date.month
    end_month_index = end_date.month

    # Initialize dict with a 0 * 7 week list for each month key -> dict(year: dict(month: days_list))
    number_per_day_of_week_dict = {}
    for year in range(start_year, end_year + 1):
        if start_year == end_year:
            start_month_index = start_date.month
            end_month_index = end_date.month
        elif year == start_year:
            start_month_index = start_date.month
            end_month_index = 12
        elif year == end_year:
            start_month_index = 1
            end_month_index = end_date.month
        number_per_day_of_week_dict[year] = {month: [0] * 7 for month in range(start_month_index, end_month_index + 1)}

    # Fill dictionary with df number of people values

    for item in list_items:
        month = item['Day'].month  # Index start at 0
        year = item['Day'].year
        day = item['Day'].day_of_week
        number_per_day_of_week_dict[year][month][day] += item['Number of people']

    for month_dict in number_per_day_of_week_dict.values():
        for week_results in month_dict.values():
            number_per_day_of_week += week_results

    return number_per_day_of_week


def get_week_name_axis_histogram(start_date, end_date):
    """
    To obtain week histogram labels
    :param start_date:
    :param end_date:
    :return: list with labels
    """
    # Index-month mapping ({} will be filled with year)
    month_name_dict = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
                       7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}

    week_dict = {0: 'Mon {} {}', 1: "Tue {} {}", 2: "Wed {} {}", 3: "Thu {} {}", 4: "Fri {} {}",
                 5: "Sat {} {}", 6: "Sun {} {}"}

    first_month = start_date.month
    last_month = end_date.month
    first_year = start_date.year
    last_year = end_date.year
    week_name_list = []

    for year in range(first_year, last_year + 1):
        month_ini = 1 if year != first_year else first_month
        month_end = 12 if year != last_year else last_month
        for month in range(month_ini, month_end + 1):
            for day in week_dict.values():
                week_name_list.append(day.format(month_name_dict[month], year))
    return week_name_list


def get_month_name_axis_histogram(start_date, end_date):
    """
    To obtain month histogram labels
    :param start_date:
    :param end_date:
    :return: list with labels
    """
    # Index-month mapping ({} will be filled with year)
    month_name_dict = {1: "Jan {}", 2: "Feb {}", 3: "Mar {}", 4: "Apr {}", 5: "May {}", 6: "Jun {}",
                       7: "Jul {}", 8: "Aug {}", 9: "Sep {}", 10: "Oct {}", 11: "Nov {}", 12: "Dec {}"}

    first_month = start_date.month
    last_month = end_date.month
    first_year = start_date.year
    last_year = end_date.year
    month_name_list = []

    for year in range(first_year, last_year + 1):

        month_ini = 1 if year != first_year else first_month
        month_end = 12 if year != last_year else last_month
        for month in range(month_ini, month_end + 1):
            month_name_list.append(month_name_dict[month].format(year))
    return month_name_list


# @@@ PIE-CHART-VALUES @@@
def get_number_per_month_pie(df, start_date, end_date):
    """
    To count the number of people on each month (It is not separated by years)
    :param df: dataframe with reservations
    :param start_date:
    :param end_date:
    :return: list with number of people each month (order: January to December)
    """

    if len(df) > 0:
        # Convert df into a list of dictionaries to search by key
        list_items = df.to_dict('records')
    else:
        list_items = []

    number_per_month = [0] * 12
    start_year = start_date.year
    end_year = end_date.year
    start_month_index = start_date.month - 1
    end_month_index = end_date.month - 1

    # Fill dictionary with df number of people values
    for item in list_items:
        month = item['Day'].month - 1  # Index start at 0
        number_per_month[month] += item['Number of people']

    # Remove unnecessary months when there are less than 12 months
    if start_year == end_year:
        number_per_month = number_per_month[start_month_index: end_month_index + 1]

    return number_per_month


def get_number_per_day_of_week_pie(df):
    """
    To count the number of people on each day of week
    :param df: dataframe with reservations
    :return: list with number of people each day of week (order: Monday to Sunday)
    """

    if len(df) > 0:
        # Convert df into a list of dictionaries
        list_items = df.to_dict('records')
    else:
        list_items = []
    number_per_day_of_week = [0] * 7  # List initialized

    for item in list_items:
        day = item['Day'].day_of_week
        number_per_day_of_week[day] += item['Number of people']

    return number_per_day_of_week


def get_month_labels_pie(start_date, end_date):
    """
    To obtain month pie-chart labels
    :param start_date:
    :param end_date:
    :return: list with labels
    """
    month_name_dict = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May ", 6: "Jun",
                       7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}

    first_year = start_date.year
    last_year = end_date.year

    if first_year != last_year:
        return [month for month in month_name_dict.values()]

    # If it is the same year, it is possible that not all months are selected
    first_month_index = start_date.month
    last_month_index = end_date.month

    return [month_name for month_index, month_name in month_name_dict.items() if
            first_month_index <= month_index <= last_month_index]


def get_week_labels_pie(start_date, end_date):
    """
    To obtain week pie-chart labels
    :param start_date:
    :param end_date:
    :return: list with labels
    """
    week_name_dict = {0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu", 4: "Fri ", 5: "Sat",  6: "Sun"}

    if (end_date - start_date).days >= 6:
        return [day for day in week_name_dict.values()]

    # If it is the same week, it is possible that not all days are selected
    first_day_index = pd.to_datetime(start_date).day_of_week
    last_day_index = pd.to_datetime(end_date).day_of_week

    return [day_name for day_index, day_name in week_name_dict.items() if
            first_day_index <= day_index <= last_day_index]


# @@@ CALLBACKS @@@
def update_histogram_month(start_date, end_date, df_reservation, histogram_title):
    """
    To update month histogram with new date range reservations
    :param start_date: first range day
    :param end_date: last range day
    :param df_reservation: dataframe with reservations between two selected days
    :param histogram_title:
    :return: updated histogram graphic object
    """

    start_date = dt.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = dt.datetime.strptime(end_date, "%Y-%m-%d")

    # Get histogram values
    month_axis = get_month_name_axis_histogram(start_date, end_date)
    number_per_month = get_number_per_month_histogram(df_reservation, start_date, end_date)

    default_histogram_values = {'Month': month_axis, 'Number': number_per_month}
    df_histogram_values = pd.DataFrame(default_histogram_values)
    x_val = df_histogram_values["Month"]
    y_val = df_histogram_values["Number"]
    color_val = [conf_vars.COLOR_GREEN] * len(x_val)

    return get_histogram(x_val, y_val, color_val, histogram_title)


def update_pie_month(start_date, end_date, df_reservation):
    """
    To update month pie-chart
    :param start_date: first range day
    :param end_date: last range day
    :param df_reservation: dataframe with reservations between two selected days
    :return: updated pie-chart graphic object
    """
    if len(df_reservation) == 0:
        return dcc.Graph(figure=get_statistics_percentage_pie(values=[0, 10],
                                                           labels=['-', '-']))

    start_date = dt.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = dt.datetime.strptime(end_date, "%Y-%m-%d")

    number_per_month = get_number_per_month_pie(df_reservation, start_date, end_date)
    month_labels = get_month_labels_pie(start_date, end_date)
    graph = dcc.Graph(
        figure=get_statistics_percentage_pie(
            values=number_per_month,
            labels=month_labels)
    )
    return graph


def update_histogram_week(start_date, end_date, df_reservation, histogram_title):
    """
    To update week histogram with new date range reservations
    :param start_date: first range day
    :param end_date: last range day
    :param df_reservation: dataframe with reservations between two selected days
    :param histogram_title:
    :return: updated histogram graphic object
    """

    start_date = dt.datetime.strptime(start_date,"%Y-%m-%d")
    end_date = dt.datetime.strptime(end_date, "%Y-%m-%d")

    day_axis_name = get_week_name_axis_histogram(start_date, end_date)
    number_per_day_of_week = get_number_per_day_of_week_histogram(
        df=df_reservation,
        start_date=start_date,
        end_date=end_date
    )

    histogram_week = {'Day': day_axis_name,
                      'Number': number_per_day_of_week}

    df_week = pd.DataFrame(histogram_week)
    x_val = df_week["Day"]
    y_val = df_week["Number"]
    color_val = [conf_vars.COLOR_GREEN] * len(x_val)

    return get_histogram(x_val, y_val, color_val, histogram_title)


def update_pie_week(start_date, end_date, df_reservation):
    """
    To update week pie-chart
    :param start_date: first range day
    :param end_date: last range day
    :param df_reservation: dataframe with reservations between two selected days
    :return: updated pie-chart graphic object
    """
    if len(df_reservation) == 0:
        return dcc.Graph(figure=get_statistics_percentage_pie(values=[0, 10],
                                                           labels=['-', '-']))

    start_date = dt.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = dt.datetime.strptime(end_date, "%Y-%m-%d")

    number_per_day = get_number_per_day_of_week_pie(df_reservation)
    day_labels = get_week_labels_pie(start_date, end_date)
    graph = dcc.Graph(
        figure=get_statistics_percentage_pie(
            values=number_per_day,
            labels=day_labels)
    )
    return graph


def get_empty_graphs(histogram_title: str):
    """
    To generates default/empty histogram and pie-chart graphs
    It is used by default and when there are no reservations on selected date range
    :param histogram_title:
    :return: histogram and pie-chart graphic objects
    """
    x_val = pd.Series(['- Select dates -'])
    y_val = pd.Series([0])
    histogram = get_histogram(x_val, y_val, [conf_vars.COLOR_GREEN],
                              histogram_title)  # Default histogram appearance
    pie_chart = dcc.Graph(figure=get_statistics_percentage_pie(
        values=[0, 10], labels=['-', '-']))
    return histogram, pie_chart
