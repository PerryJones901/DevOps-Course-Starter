import os

class AuthConfig():
    def __init__(self):
        self._AUTH_CLIENT_ID = os.environ.get('AUTH_CLIENT_ID')
        self._AUTH_CLIENT_SECRET = os.environ.get('AUTH_CLIENT_SECRET')

    @property
    def AUTH_CLIENT_ID(self) -> str:
        return self._AUTH_CLIENT_ID

    @property
    def AUTH_CLIENT_SECRET(self) -> str:
        return self._AUTH_CLIENT_SECRET
