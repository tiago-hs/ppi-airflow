from unittest.mock import MagicMock, call

from pytest import fixture, mark, raises

from ppi_airflow.airflow import AIRFLOW_BASE_PATH
from ppi_airflow.airflow.dag_factory import DAGFactory
from ppi_airflow.airflow.no_project_error import NoProjectsError


@fixture
def dag_factory():
    yield DAGFactory(AIRFLOW_BASE_PATH)


# Simula a hierarquia de diretórios em que há subdiretórios das rotinas.
@fixture
def mock_projets():
    return ['project_a', 'project_b']


# Simula a declaração de importação de um módulo
@fixture
def mock_import_module(project):
    return f'ppi_airflow.dags{project}.DAG'

@fixture
def mock_dags_module():
    dag_1 = MagicMock()
    dag_2 = MagicMock()
    dag_1.DAGS = [MagicMock(), MagicMock()]
    dag_2.DAGS = []
    return (dag_1, dag_2)

# @mark.skip
def test_deve_exibir_uma_messagem_de_erro_caso_nao_existam_projetos_a_serem_processados(
    dag_factory, mocker
):
    """
    Deve exibir uma mensagem de erro informando que não existem projetos para serem processados.
    """
    # Simula o path do projeto
    mock_walk_return_empty_projets = [(AIRFLOW_BASE_PATH, ['__pycache__'], [])]

    mocker.patch('os.walk', return_value=mock_walk_return_empty_projets)

    error_msg = 'ERROR [DAGFactory] There are no projects to process: Check obj.projects'

    with raises(NoProjectsError) as error:
        dag_factory.get_modules_from_all_projects()

    assert error.value.args[0] == error_msg
    assert len(dag_factory.projects) == 0


def test_deve_importar_os_modulos_corretamente(dag_factory, mocker):
    """
    Testa se a importação dinâmica ocorre adequadamente
    """

    mock_walk_return_existing_projets = [(AIRFLOW_BASE_PATH, mock_projets, [])]
    projects = mocker.patch(
        'os.walk', return_value=mock_walk_return_existing_projets
    )

    for project in projects:
        module_name = mock_import_module(project)
        mocker.patch(
            'ppi_airflow.airflow.dag_factory.import_module',
            return_value=MagicMock(return_value=module_name),
        )

        dag_factory.get_modules_from_all_projects()

        expected_calls = call(module_name)

        mocker.import_module.assert_has_calls([expected_calls])


def test_deve_garantir_se_o_modulo_DAG_possui_atributo_DAGS_com_uma_lista_de_objetos(dag_factory):
    """
    Testa se o modulo DAG.py fornece um atributo DAGS.
    """
    pass


def test_deve_garantir_que_o_atributo_dags_e_uma_lista_de_objetos_da_classe_dag(
    dag_factory,
):
    """
    Testa se o atributo DAGS fornece uma lista de objetos DAG do Airflow corretamente.
    """
    pass


def test_deve_exibir_uma_mensagem_de_erro_informando_que_o_atributo_DAGS_esta_vazio(
    dag_factory,
):
    """
    Testa se uma mensagem de erro é exibida caso o atributo DAGS seja uma lista vazia.
    """
    pass


def test_deve_importar_corretamente_as_varivaveis_globais(dag_factory):
    """
    Testa se as variaveis são armazenadas no escopo globla corretamente.
    """
    pass
