import os

class AppConfig:
    def __init__(self):
        self._MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME')
        self._MONGO_CONNECTION_STRING = os.environ.get('MONGO_CONNECTION_STRING')
        self._SECRET_KEY = os.environ.get('SECRET_KEY')
        self._LOGIN_DISABLED = os.environ.get('LOGIN_DISABLED', None)
        self._LOG_LEVEL = os.environ.get('LOG_LEVEL', 'ERROR')
        self._LOGGLY_TOKEN = os.environ.get('LOGGLY_TOKEN', None)

    @property
    def MONGO_DB_NAME(self) -> str:
        return self._MONGO_DB_NAME

    @property
    def MONGO_CONNECTION_STRING(self) -> str:
        return self._MONGO_CONNECTION_STRING

    @property
    def SECRET_KEY(self) -> str:
        return self._SECRET_KEY

    @property
    def LOGIN_DISABLED(self) -> str:
        return self._LOGIN_DISABLED

    @property
    def LOG_LEVEL(self) -> str:
        return self._LOG_LEVEL

    @property
    def LOGGLY_TOKEN(self) -> str:
        return self._LOGGLY_TOKEN
