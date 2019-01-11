from __future__ import annotations

import typing

from .abc import AbstractEndpoint, AbstractResource
from .utils import filter_none, urljoin

if typing.TYPE_CHECKING:
    from .client import Hydra


class ConsentRequest(AbstractEndpoint):

    endpoint = "/oauth2/auth/requests/consent"

    def __init__(self, data: dict, parent: AbstractResource):
        super().__init__(parent)
        self.acr = data["acr"]
        self.challenge = data["challenge"]
        self.client = data["client"]
        self.login_challenge = data["login_challenge"]
        self.login_session_id = data["login_session_id"]
        self.oidc_context = data["oidc_context"]
        self.request_url = data["request_url"]
        self.requested_access_token_audience = data["requested_access_token_audience"]
        self.requested_scope = data["requested_scope"]
        self.skip = data["skip"]
        self.subject = data["subject"]
        self.url = urljoin(self.url, self.challenge)

    @classmethod
    def get(cls, challenge: str, hydra: Hydra) -> ConsentRequest:
        url = urljoin(hydra.url, cls.endpoint, challenge)
        response = hydra._request("GET", url)
        return cls(response.json(), hydra)

    def accept(
        self,
        grant_access_token_audience: typing.Iterable[str] = None,
        grant_scope: typing.Iterable[str] = None,
        remember: bool = False,
        remember_for: int = None,
        session: dict = None,
    ) -> str:
        data = filter_none(
            {
                "grant_access_token_audience": grant_access_token_audience,
                "grant_scope": grant_scope,
                "remember": remember,
                "remember_for": remember_for,
                "session": session,
            }
        )
        url = urljoin(self.url, "accept")
        response = self._request("PUT", url, json=data)
        # TODO: Catch exceptions and raise custom error
        payload = response.json()
        return payload["redirect_to"]

    def reject(
        self,
        error: str = None,
        error_debug: str = None,
        error_description: str = None,
        error_hint: str = None,
        status_code: int = None,
    ) -> str:
        url = urljoin(self.url, "reject")
        data = filter_none(
            {
                "error": error,
                "error_debug": error_debug,
                "error_description": error_description,
                "error_hint": error_hint,
                "status_code": status_code,
            }
        )
        response = self._request("PUT", url, json=data)
        # TODO: Catch exceptions and raise custom error
        payload = response.json()
        return payload["redirect_to"]
