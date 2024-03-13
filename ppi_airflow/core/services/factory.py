from ppi_airflow.core.services.service import Service


class ServiceFactory:
    """
    Classe responsável por gerenciar e criar conexões com base em builders
    registrados.

    A ServiceFactory permite o registro de builders para diferentes
    projetos. Cada builder é associado a um projeto específico e é
    utilizado para criar instâncias de conexões relacionadas a esse projeto.

    Attributes:
        _builders (dict):
            Um dicionario que registrará o nome do projeto como chave e seu serviçõe de conexão como valor

    Methods:
        register_builder(project_name, builder) -> None:
            Registra um builder associado a um projeto.

        create(project_name, **kwargs) -> object:
            Cria uma conexão utilizando o builder registrado para o projeto específico.
    """

    def __init__(self):
        self._builders = {}

    def register_builder(self, project_name, builder) -> None:
        """
        Registra um builder associado a um projeto.

        Parameters:
            project_name (str):
                Nome do projeto ao qual o builder está associado.

            builder (object):
                Um objeto que deve ser um construtor de conexão (um callable) para
                o projeto.
        """
        self._builders[project_name] = builder

    def create(self, project_name, **kwargs) -> Service:
        """
        Cria uma conexão utilizando o builder registrado para o projeto
        específico.

        Parameters:
            project_name (str):
                Nome do projeto para o qual a conexão deve ser criada.

            **kwargs (any):
                Parâmetros adicionais que serão passados para o construtor do
                builder.

        Returns:
            Service:
                Uma instância de conexão com serviço externo criada pelo builder associado ao projeto.

        Raises:
            ValueError:
                Se não houver um builder registrado para o projeto.
        """
        builder = self._builders.get(project_name)
        if not builder:
            raise ValueError(project_name)
        return builder(**kwargs)
