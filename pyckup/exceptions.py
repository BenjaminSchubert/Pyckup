class PyckupException(Exception):
    pass


class InvalidConfigException(PyckupException):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg

    def __str__(self):
        return "Invalid configuration: {}".format(self.msg)


class SyncException(PyckupException):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg

    def __str__(self):
        return "Error while syncing: {}".format(self.msg)