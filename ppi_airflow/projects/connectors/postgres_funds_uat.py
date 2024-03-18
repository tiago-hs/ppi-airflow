import psycopg2

from ppi_airflow.core.services.builder import ServiceBuilder
from ppi_airflow.core.services.service import Service


class PostgresFundsUATBuilder(ServiceBuilder):
    def __call__(self, config, **_ignored):
        if not self._service:
            self._service = PostgresFundsUATConnectionService(config)
            return self._service


class PostgresFundsUATConnectionService(Service):
    def __init__(self, config):
        if not isinstance(config, dict):
            raise TypeError(
                f'The parameter {config} needs to be a dictionary and its type is {type(config)}.'
            )
        else:
            self._config = config
        self._connection = None

    def create_connection(self):
        try:
            return psycopg2.connect(
                host=self._config['DB_HOST'],
                database=self._config['DB_NAME'],
                user=self._config['DB_USER'],
                password=self._config['DB_PASS'],
                port=self._config['DB_PORT'],
            )
        except psycopg2.OperationalError as e:
            raise ConnectionError(f'Failed to connect to PostgreSQL: {e}')

    def close_connection(self):
        if self._connection:
            self._connection.close()
