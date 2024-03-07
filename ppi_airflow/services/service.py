from abc import abstractmethod


class Service:
    """
    Implementa uma instancia de conexão com um banco de dados seguindo
    o protocolo de gerenciamento de contexto.

    Attributes:
        config (dict):
            Um dicionário contendo os parâmetros de configuração necessários para
            estabelecer uma conexão com um banco de dados.

        **_ignored (any):
            Parâmetros adicionais que podem ser ignorados. Presentes apenas para
            compatibilidade com chamadas de outros métodos.
    """

    def __init__(self, config, **_ignored):
        self._config = config

    @abstractmethod
    def create_connection(self):
        """
        Método responsável por chamar a dependência externa que retornará
        o objeto de conexão com um banco de dados.
        """
        raise NotImplementedError(
            f'{self.__class__.__name__}.__call__ needs to be implemented.'
        )

    @abstractmethod
    def close_connection(self):
        """
        Método responsável por fechar uma conexão externa caso necessário
        """
        raise NotImplementedError(
            f'{self.__class__.__name__}.__call__ needs to be implemented.'
        )

    @abstractmethod
    def execute_operation(self):
        """
        Executa uma operação específica para o tipo de conexão, como uma query de bancode dados por exemplo.
        """

    def __enter__(self):
        """
        Este método é chamado quando o objeto é usado como gerenciador de
        contexto (utilizando 'with'). Deve retornar um recurso de conexão,
        seja um banco de dados ou outro serviço.
        """
        self.create_connection()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Este método é chamado quando o bloco 'with' é concluído e
        é responsável por realizar ações de limpeza, como fechar
        a conexão com o banco de dados.

        Parameters:
            exc_type (object):
                Tipo da exceção, se houver.

            exc_value (any):
                Valor da exceção, se houver.

            traceback (Trace):
                Objeto traceback, se houver.
        """
        self.close_connection()

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(config={self._config})'
