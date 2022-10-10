# restaurant-booking-manager 
[![Issues][issues-shield]][issues-url]

[issues-shield]: https://img.shields.io/github/issues/mmtnz/restaurant-booking-manager.svg?style=flat
[issues-url]: https://github.com/mmtnz/restaurant-booking-manager/issues

[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Dash 2.6](https://img.shields.io/badge/dash-2.6-yellow.svg)](https://dash.plotly.com/)
[![mysql](https://img.shields.io/badge/MySQL-database-orange?style=flate&logo=mysql&logoColor=white.svg)](https://mysql.com/)



### Table of Contents
<details>
  <summary>Click me</summary>
  
### Contents
- 1. [Description](#description)
  - 1. [Built With](#built-with)
  - 2. [Challenges](#challenges)
- 2. [Funtionalities](#funtionalities)
  - 1. [Show reservations](#show-reservations)
  - 2. [Edit reservations](#edit-reservations)
  - 3. [Statistics](#statistics)
- 2. [Getting Started](#getting-started)
- 3. [Contact](#contact)
</details>

## Description

This demo/app represents a booking system that could be used in companies such as restaurants (current case), hotels, etc.


![example](https://user-images.githubusercontent.com/100723086/194145144-741c19ff-0e05-455b-b3ef-d371d435970f.gif)

The motivation of this project is to learn new software tools and offer an easy managment solution for companies such as the mentioned above. 

The user can visualize reservations of the selected date, as well as **add, edit or remove any reservation** filtering by date. Furthemore, not only can occupation be controlled but also the number of employees needed. This isthanks to the statistics page which can be used to discover the more occupated seasons in past years. Thus extra people could be added to staff only as required.


### Built With

- [![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
- [![Dash 2.6](https://img.shields.io/badge/dash-2.6-yellow.svg)](https://dash.plotly.com/) : Dash library is an easy way to create a web app.
- [![mysql](https://img.shields.io/badge/MySQL-database-orange?style=flate&logo=mysql&logoColor=white.svg)](https://mysql.com/) : MySql database is used to gather all reservations. This allows the app add, edit or remove reservations easyly.

### Challenges

This first release is designed to be used locally (database is locally located). However, future development lines will be focused on creating cloud solutions.

- Use a `cloud-based database`.
- Create the customer side. This will consist in a `chatbot` that automatically manage the reservations in the cloud database.

<p align="right">(<a href="#restaurant-booking-manager">back to top</a>)</p>

## Funtionalities

- ### Show reservations

In this page reservations are visually shown, indicating name, time and observations.

![show_small](https://user-images.githubusercontent.com/100723086/194363209-ac9321ba-eff6-4202-9428-12e02d60784c.png)


- ### Edit reservations

In this page reservation could be added, edited or removed. 

There also is a graphic indicating occupation percentage.

![reservations](https://user-images.githubusercontent.com/100723086/194899543-74f7235a-0cd4-4627-9919-510e4bd9bdc8.png)


- ### Statistics

In this page it is possible to analyze week and month satatistics.

![statistics](https://user-images.githubusercontent.com/100723086/194364280-53e1d36d-1170-473e-bd05-80cc02860c20.png)

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

If something is not working as spected, check for errors the `log file` located in folder path.

<p align="right">(<a href="#restaurant-booking-manager">back to top</a>)</p>

## Contact

- e-mail: [mariomlafuente@gmail.com](mailto:mariomlafuente@gmail.com) 

<p align="right">(<a href="#restaurant-booking-manager">back to top</a>)</p>
