import mysql.connector as mysqlcon


class DataBase:

    def __init__(self, host, schema_name, user, password):
        self._host = host
        self._schema_name = schema_name
        self._user = user
        self._password = password

        self._connection = None
        self._cursor = None

        self._num_attempts = 4  # Connection attempts
        self.error_creating = False
        self._connect()

    def _connect(self):
        num_attempts = 0
        while num_attempts < self._num_attempts:

            self._connection = mysqlcon.connect(host=self._host, database=self._schema_name,
                                                user=self._user, password=self._password)

            if self._connection is not None and self._connection.is_connected():
                return None

            num_attempts += 1

        self.error_creating = TimeoutError

    def _disconnect(self):
        try:
            self._cursor.close()
            self._connection.close()
        except Exception as e:
            print(f'[!] Error disconnecting -> {type(e)}: {e}')

    def select_query(self, table_name, columns=None, where_condition=None, order_by_column=None, order_asc=True):

        if self._connection is None or not self._connection.is_connected():
            self._connect()
        self._cursor = self._connection.cursor()

        columns = columns if columns else '*'
        sql_select_query = f"SELECT {columns} FROM {table_name}"  # Status = 0 means entry is not read

        if where_condition:
            where_query = f" WHERE {where_condition}"
            sql_select_query += where_query

        if order_by_column is not None:
            ord_type = "ASC" if order_asc else "DESC"
            order_by_query = f" ORDER BY {order_by_column} {ord_type}"
            sql_select_query += order_by_query

        self._cursor.execute(sql_select_query)
        return self._cursor.fetchall()

    def insert_query(self, table_name, values, columns=None):
        if not self._connection.is_connected():
            self._connect()
        self._cursor = self._connection.cursor()
        sql_insert_query = f"INSERT INTO {table_name}"
        if columns:
            sql_insert_query += f" {columns}"

        sql_insert_query += f" VALUES {values}"
        self._cursor.execute(sql_insert_query)
        self._connection.commit()

    def delete_query(self, table_name, condition):
        if not self._connection.is_connected():
            self._connect()
        self._cursor = self._connection.cursor()

        sql_delete_query = f"DELETE FROM {table_name} WHERE {condition}"
        self._cursor.execute(sql_delete_query)
        self._connection.commit()

    def update_query(self, table_name, values_str, condition):

        if not self._connection.is_connected():
            self._connect()
        self._cursor = self._connection.cursor()

        sql_update_query = f"UPDATE {table_name} SET {values_str} WHERE {condition}"
        self._cursor.execute(sql_update_query)
        self._connection.commit()

