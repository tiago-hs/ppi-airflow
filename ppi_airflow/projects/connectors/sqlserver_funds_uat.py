import pyodbc

from ppi_airflow.core.services.builder import ServiceBuilder
from ppi_airflow.core.services.service import Service


class SqlServerUATBuilder(ServiceBuilder):
    def __call__(self, config, **_ignored):
        if not self._service:
            self._service = SqlServerFundsUATService(config)
            return self._service


class SqlServerFundsUATService(Service):
    def __init__(self, config):
        if not isinstance(config, dict):
            raise TypeError(
                f'The parameter {config} needs to be a dictionary and its type is {type(config)}.'
            )
        else:
            self._config = config
        self._connection = None

    def create_connection(self):
        SERVER = self._config['SQL_SERVER_PMS_SERVER']
        DATABASE = self._config['SQL_SERVER_PMS_DATABASE']
        USERNAME = self._config['SQL_SERVER_PMS_USER']
        PASSWORD = self._config['SQL_SERVER_PMS_PASSWORD']

        connection_string = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'

        try:
            return pyodbc.connect(connection_string)
        except pyodbc.Error as e:
            raise ConnectionError(f'Failed to connect to PostgreSQL: {e}')

    def close_connection(self):
        if self._connection:
            self._connection.close()
