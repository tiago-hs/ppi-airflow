import os

from dotenv import load_dotenv

from ppi_airflow.core.services.provider import ServiceProvider
from ppi_airflow.projects.connectors.postgres_funds_uat import PostgresFundsUATBuilder
from ppi_airflow.projects.connectors.sqlserver_funds_uat import SqlServerUATBuilder

load_dotenv()

# TODO: criar módulo de configuração externo
postgres_uat_config = {
    'DB_NAME': os.environ.get('POSTGRES_FUNDS_UAT_DATABASE_NAME'),
    'DB_USER': os.environ.get('POSTGRES_FUNDS_UAT_DATABASE_USER'),
    'DB_PASS': os.environ.get('POSTGRES_FUNDS_UAT_DATABASE_PASS'),
    'DB_HOST': os.environ.get('POSTGRES_FUNDS_UAT_DATABASE_HOST'),
    'DB_PORT': os.environ.get('POSTGRES_FUNDS_UAT_DATABASE_PORT'),
}

sqlserver_uat_config = {
    'SERVER': os.environ.get('SQL_SERVER_PMS_SERVER'),
    'DATABASE': os.environ.get('SQL_SERVER_PMS_DATABASE'),
    'USERNAME': os.environ.get('SQL_SERVER_PMS_USER'),
    'PASSWORD': os.environ.get('SQL_SERVER_PMS_PASSWORD'),
}

postgres_funds_uat = 'PostgreSQL'
sqlserver_funds_uat = 'SQLServer'

service = ServiceProvider()

service.register_builder(postgres_funds_uat, PostgresFundsUATBuilder())
service.register_builder(sqlserver_funds_uat, SqlServerUATBuilder())


POSTGRESQL_FUNDS_UAT_SERVICE = service.get(
    postgres_funds_uat, config=postgres_uat_config
)
SQLSERVER_FUNDS_UAT_SERVICE = service.get(
    sqlserver_funds_uat, config=sqlserver_uat_config
)
