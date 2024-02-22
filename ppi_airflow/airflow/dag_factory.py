import os
import sys
import traceback
from importlib import import_module
from logging import info

AIRFLOW_BASE = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

sys.path.append(AIRFLOW_BASE)


class DAGFactory:
    """
    Classe responsável por criar e gerenciar Directed Acyclic Graphs (DAGs).

    Encapsula funcionalidades relacionadas à obtenção de informações sobre projetos e seus DAGs,
    bem como a importação dinâmica de módulos e a criação de variáveis globais para esses DAGs.

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

    def __init__(self):
        self.__project_base = os.path.join(AIRFLOW_BASE, 'ppi_airflow')

    @property
    def projects(self) -> list[str]:
        """
        Itera recursivamente sobre o diretório base e o primeiro nível de
        seus subdiretórios.

        Examples:
            >>> factory = DAGFactory()
            >>> isinstance(factory.projects, list)
            True
            >>> len(factory.projects) > 0
            True

        Returns:
            Uma lista de nomes dos subdiretórios contidos no primeiro nível do diretório base da instância da classe, excluindo o diretório __pycache__.
        """
        return list(
            filter(
                lambda x: x not in ['__pycache__'],
                [dirs for _, dirs, _ in os.walk(self.__project_base)][1],
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

        Examples:
            >>> factory = DAGFactory()
            >>> factory.get_modules_from_all_projects()
        """

        for project_name in self.projects:
            try:
                module_name = f'ppi_airflow.dags.{project_name}.DAG'
                module = import_module(module_name)
                num_of_project_dags = 1

                for dag in module.DAGS:
                    var_name = f'{project_name}-{num_of_project_dags}'

                    globals()[var_name] = dag

                    info(f'DAG {var_name} armazenada no namespace global.')

                    num_of_project_dags += 1
            except Exception:
                print(traceback.format_exc())
