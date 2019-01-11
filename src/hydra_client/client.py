from .abc import AbstractResource
from .consent import ConsentRequest
from .login import LoginRequest
from .version import Version


class Hydra(AbstractResource):
    def __init__(self, url: str):
        super().__init__()
        self.url = url


class HydraAdmin(Hydra):
    def login_request(self, challenge: str) -> LoginRequest:
        return LoginRequest.get(challenge, self)

    def consent_request(self, challenge: str) -> ConsentRequest:
        return ConsentRequest.get(challenge, self)

    def version(self) -> str:
        return Version.get(self)
