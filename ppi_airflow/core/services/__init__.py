import os
from postgre_connection_service import PostgresConnectionService

config = {
    'host': os.environ.get('DB_HOST'),
    'database': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASS'),
}

postgre = PostgresConnectionService(config)
postgre.create_connection()

with PostgresConnectionService(config) as conn:
    print(type(conn))



