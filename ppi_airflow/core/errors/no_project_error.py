class NoProjectsError(Exception):
    def __init__(
        self,
        massage='ERROR [DAGFactory] There are no projects to process: Check obj.projects',
    ):
        self.massage = massage
        super().__init__(self.massage)
