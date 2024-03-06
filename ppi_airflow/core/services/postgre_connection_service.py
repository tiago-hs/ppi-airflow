import psycopg2
from dotenv import load_dotenv

load_dotenv()
from service import Service


class PostgresConnectionService(Service):
    def __init__(self, config):
        self._config = config
        self.connection = None

    def create_connection(self):
        return psycopg2.connect(
            host=self._config['host'],
            database=self._config['database'],
            user=self._config['user'],
            password=self._config['password'],
        )

    def close_connection(self):
        if self.connection:
            self.connection.close()
