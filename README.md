# restaurant-booking-manager 
[![Issues][issues-shield]][issues-url]

[issues-shield]: https://img.shields.io/github/issues/mmtnz/restaurant-booking-manager.svg?style=flat
[issues-url]: https://github.com/mmtnz/restaurant-booking-manager/issues

[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Dash 4.0](https://img.shields.io/badge/dash-4.0-yellow.svg)](https://dash.plotly.com/)
[![mysql](https://img.shields.io/badge/-MySQL-orange?style=flate&logo=mysql&logoColor=white.svg)](https://mysql.com/)

## Table of Contents
<details>
  <summary>Click me</summary>
  
  ### Contents
  1. [Description](#description)
  2. [Built With](#built-with)
  3. [Challenges](#challenges)
  4. [Getting Started](#getting-started)
</details>

## Description

This demo/app represents a booking system that could be used in companies such as restaurants (current case), hotels, etc.

The motivation of this project is to learn new software tools and offer an easy managment solution for companies such as the mentioned above. 

The user can visualize reservations of the selected date, as well as **add, edit or remove any reservation** filtering by date. Furthemore, not only can occupation be controlled but also the number of employees needed. This isthanks to the statistics page which can be used to discover the more occupated seasons in past years. Thus extra people could be added to staff only as required.


### Built With

- [![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
- [![Dash 4.0](https://img.shields.io/badge/dash-4.0-yellow.svg)](https://dash.plotly.com/) : Dash library is an easy way to create a web app.
- ![mysql](https://img.shields.io/badge/MySQL-orange?style=flate&logo=mysql&logoColor=white.svg) : MySql database is used to gather all reservations. This allows the app add, edit or remove reservations easyly.

### Challenges

This first release is designed to be used locally (database is locally located). However, future development lines will be focused on creating cloud solutions.

- Use a `cloud-based database`.
- Create the customer side. This will consist in a `chatbot` that automatically manage the reservations in the cloud database.

<p align="right">(<a href="#restaurant-booking-manager">back to top</a>)</p>

## Getting Started

In this section it will be shown how to run the app locally.

The first step is to clone this repository in a local folder.

### Prerequisites

- #### Database:
In this release it is necessary to have the database locally located therefore a new database schema has to be created.

This schema must contain a table with the following structure:

```sh
CREATE TABLE movies(
  ReservationId VARCHAR(50) NOT NULL,
  ReservationName VARCHAR(30) NOT NULL,
  ReservationDate VARCHAR(60) NOT NULL,
  ReservationTables VARCHAR
  ReservationObservations VARCHAR(1000),
  PRIMARY KEY(ReservationId)
);
```

Make sure that the user to use has the privilegs needed.

- #### Requirements:
Create and activate a new virtual enviroment.
```sh
python3 -m venv project_local_folder/myvenv
cd project_local_folder/myvenv/scripts
activate
```

Install the requirements.
```sh
cd project_local_folder
pip install -r requirements.txt
```

- #### Configuration:
Change the configuration.ini file with the new database data and indicate the number of tables and number of people per table.

- #### Run app:
```sh
python app.py
```

Open browser at [http://127.0.0.1:8050](http://127.0.0.1:8050)

If something is not working as spected, check for errors in the `log file` located in the folder path.

<p align="right">(<a href="#restaurant-booking-manager">back to top</a>)</p>


