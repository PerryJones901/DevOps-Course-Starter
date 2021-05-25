import os

class AppConfig:
    def __init__(self):
        self._MONGO_USERNAME = os.environ.get('MONGO_USERNAME')
        self._MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')
        self._MONGO_CLUSTER_NAME = os.environ.get('MONGO_CLUSTER_NAME')
        self._MONGO_DEFAULT_DB_NAME = os.environ.get('MONGO_DB_NAME')
        self._SECRET_KEY = os.environ.get('SECRET_KEY')
        self._LOGIN_DISABLED = os.environ.get('LOGIN_DISABLED', None)

    @property
    def MONGO_USERNAME(self) -> str:
        return self._MONGO_USERNAME

    @property
    def MONGO_PASSWORD(self) -> str:
        return self._MONGO_PASSWORD

    @property
    def MONGO_CLUSTER_NAME(self) -> str:
        return self._MONGO_CLUSTER_NAME

    @property
    def MONGO_DB_NAME(self) -> str:
        return self._MONGO_DEFAULT_DB_NAME

    @property
    def SECRET_KEY(self) -> str:
        return self._SECRET_KEY

    @property
    def LOGIN_DISABLED(self) -> str:
        return self._LOGIN_DISABLED
