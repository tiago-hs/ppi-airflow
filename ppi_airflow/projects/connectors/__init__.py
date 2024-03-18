import os

from dotenv import load_dotenv

from ppi_airflow.core.services.provider import ServiceProvider
from ppi_airflow.projects.connectors.postgres_funds_uat import PostgresFundsUATBuilder

load_dotenv()

# TODO: criar módulo de configuração externo
config = {
    'DB_NAME': os.environ.get('DB_NAME'),
    'DB_USER': os.environ.get('DB_USER'),
    'DB_PASS': os.environ.get('DB_PASS'),
    'DB_HOST': os.environ.get('DB_HOST'),
    'DB_PORT': os.environ.get('DB_PORT'),
}

project_name = 'upcoming_fixed_income_maturity_dates'
service = ServiceProvider()

service.register_builder(project_name, PostgresFundsUATBuilder())


POSTGRESQL_SERVICE = service.get(project_name, config=config)
