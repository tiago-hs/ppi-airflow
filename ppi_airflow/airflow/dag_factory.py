import os
import traceback
from importlib import import_module

from ppi_airflow.core.errors.no_project_error import NoProjectsError


class DAGFactory:
    """
    Classe responsável por criar e gerenciar Directed Acyclic Graphs (DAGs).

    Encapsula funcionalidades relacionadas à obtenção de informações sobre projetos e
    seus DAGs,
    bem como a importação dinâmica de módulos e a criação de variáveis globais para
    esses DAGs.

    Attributes:
        __project_base (str): O caminho base onde os projetos estão localizados.

    Methods:
        projects(self) -> list[str]:
            Itera recursivamente sobre o diretório base e o primeiro nível de
            seus subdiretórios, retornando uma lista de nomes dos subdiretórios contidos
            no primeiro nível do diretório base, excluindo o diretório '__pycache__'.

        get_modules_from_all_projects(self) -> None:
            Obtém módulos de todos os projetos e cria variáveis globais para os DAGs
            encontrados nesses módulos. Essas variáveis globais são nomeadas de acordo com
            o padrão 'projeto-numero_dag'.
    """

    def __init__(self, AIRFLOW_BASE_PATH):
        self.__project_base = AIRFLOW_BASE_PATH

    @property
    def projects(self) -> list[str]:
        """
        Itera recursivamente sobre o diretório base e o primeiro nível de
        seus subdiretórios.

        Returns:
            Uma lista de nomes dos subdiretórios contidos no primeiro nível do diretório base da instância da classe, excluindo o diretório __pycache__. Retornará uma lista vazia caso não existam projetos no diretório `dags`.

        Examples:
            >>> from ppi_airflow.airflow.dag_factory import DAGFactory
            >>> from ppi_airflow.airflow import AIRFLOW_BASE_PATH
            >>> factory = DAGFactory(AIRFLOW_BASE_PATH)
            >>> isinstance(factory.projects, list)
            True
        """

        return list(
            filter(
                lambda x: x not in ['__pycache__'],
                [dirs for _, dirs, _ in os.walk(self.__project_base)][0],
            )
        )

    def get_modules_from_all_projects(self) -> None:
        """
        Obtém módulos de todos os projetos.

        Percorre todos os projetos disponíveis na base de projetos e tenta
        importar o módulo correspondente à DAG de cada projeto. Para cada DAG
        encontrada em cada módulo, cria uma variável global com um nome exclusivo
        no formato `projeto-numero_dag`. Uma exceção é levantada se o processo de
        importação ou criação das variáveis globais não for possível. O traceback
        da exceção será impresso, mas a execução continuará para os próximos projetos.
        """

        if len(self.projects) == 0:
            raise NoProjectsError

        for project_name in self.projects:
            try:
                if not project_name:
                    raise ModuleNotFoundError(
                        f'Module {project_name} not found.'
                    )

                module_name = f'ppi_airflow.dags.{project_name}.DAG'
                module = import_module(module_name)
                num_of_project_dags = 1

                for dag in module.DAGS:

                    if not getattr(module, 'DAGS'):
                        raise AttributeError(
                            f'The module {module} no has attribute DAGS.'
                        )

                    var_name = f'{project_name}-{num_of_project_dags}'

                    globals()[var_name] = dag

                    print(f'INFO [DAGFactory] Projects: {self.projects}.')
                    print(
                        f'INFO [DAGFactory] DAG {var_name} in global namespace.'
                    )

                    num_of_project_dags += 1

            except Exception:
                print(traceback.format_exc())
