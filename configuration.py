import configparser
from database import DataBase
from custom_logger import logger

""" Read config file as configparser """
try:
    config_file = 'configuration.ini'
    configuration_reader = configparser.ConfigParser()
    configuration_reader.read(config_file)
except Exception as e:
    logger.error(f'[!] Error reading config file -> {type(e)}: {e}')
    configuration_reader = None

""" Map config file vars with global vars """
try:
    SW_VERSION = 1.0

    DB_HOST = configuration_reader['database']['db_host']
    DB_PASSWORD = configuration_reader['database']['db_password']
    DB_SCHEMA_NAME = configuration_reader['database']['db_schema_name']
    DB_USER = configuration_reader['database']['db_user']
    DB_TABLE_NAME = configuration_reader['database']['db_table_name']

    logger.info(f'[+] Configuration.ini has been successfully read')
except Exception as e:
    logger.error(f'[!] Error reading config file -> {type(e)}: {e}')
    SW_VERSION = '0.0'
    DB_HOST = DB_PASSWORD = DB_SCHEMA_NAME = DB_USER = DB_TABLE_NAME = ''

""" Create DataBase object """
try:
    database = DataBase(
        host=DB_HOST,
        schema_name=DB_SCHEMA_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    if database.error_creating:
        logger.error(f"[!] Error creating database object -> {type(e)}: {e}")
    else:
        logger.info(f'[+] Database object successfully created')
except Exception as e:
    database = None
    logger.error(f"[!] Error creating database object -> {type(e)}: {e}")

""" GLOBALS VARS """
# Colors
COLOR_DARK = '#1f2630'
COLOR_DARK_THING = "#252e3f"
COLOR_GREEN = "#2cfec1"
COLOR_BLUE = "#7fafdf"

COLOR_DARK_GREEN = "#134a3c"
COLOR_SEMI_DARK_GREEN_1 = "#289878"
COLOR_SEMI_DARK_GREEN_2 = "#5ac1a4"
COLOR_SEMI_DARK_GREEN_3 = "#5dc8aa"
COLOR_SEMI_DARK_GREEN_4 = "#1e7b61"
COLOR_SEMI_DARK_GREEN_5 = "#3dae8e"
COLOR_SEMI_DARK_GREEN_6 = "#2bb489"
COLOR_LIGHT_GREEN_1 = "#9cd4c6"
COLOR_LIGHT_GREEN_2 = "#98ffe0"
COLOR_WHITE_GREEN = "#b7bbbb"

# Restaurant
NUM_TABLES = 20
NUM_PEOPLE_PER_TABLE = 6
COLUMNS = ["Id", "Name", "Day", "Number of people", "Table(s)", "Observations"]
