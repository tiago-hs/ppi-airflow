import os
import sys

from ppi_airflow.airflow.dag_factory import DAGFactory
from ppi_airflow.airflow.no_project_error import NoProjectsError

BASE_PATH = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

AIRFLOW_BASE_PATH = os.path.join(BASE_PATH, 'ppi_airflow/dags')

sys.path.append(AIRFLOW_BASE_PATH)

dag_factory = DAGFactory(AIRFLOW_BASE_PATH)
try:
    print(dag_factory.projects)
    dag_factory.get_modules_from_all_projects()
except NoProjectsError as e:
    print(e)
