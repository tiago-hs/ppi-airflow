class ServiceBuilder:
    """
    Define a estrutura para construtores de conexão e mantém a instancia
    disponível para reuso.

    Esta classe fornece um método abstrato `__call__` que deve ser implementado
    por todas as subclasses. O método `__call__` é responsável por instanciar
    e retornar um objeto concreto de ConnectionService com base na configuração
    fornecida.

    Attributes:
        __service (Service):
            A instância de Service criada pelo método '__call__'.

    Methods:
        __call__(config, **_ignored) -> Service:
            Método abstrato que deve ser implementado por subclasses. Recebe uma
            configuração e retorna uma instância de Service.

    """

    def __init__(self):
        self._service = None

    def __call__(self, config, **_ignored):
        """
        Fornece uma interface geral responsável pela criação de um
        serviço concreto.

        Parameters:
            config (dict):
                Um dicionário ou um dataclass contendo a configuração necessária
                para criar a conexão com o banco de dados.

            **_ignored (any):
                Parâmetros adicionais que podem ser ignorados. Presentes apenas
                para compatibilidade com chamadas de outros métodos.

        Returns:
            Uma instância de Service com base na configuração.

        Examples:

            class MyProjectServiceBuilder(ServiceBuilder):
                def __init__(self):
                    self._service = None

                def __call__(self, config, **_ignored):
                    if not self._service:
                        self._service = MyProjectService(config)
                    return self._service
        """
        raise NotImplementedError(
            f'{self.__class__.__name__}.__call__ needs to be implemented.'
        )
