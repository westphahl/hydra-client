from __future__ import annotations

import typing

from .abc import AbstractEndpoint, AbstractResource
from .utils import filter_none, urljoin

if typing.TYPE_CHECKING:
    from .client import Hydra


class LoginRequest(AbstractEndpoint):

    endpoint = "/oauth2/auth/requests/login"

    def __init__(self, data: dict, parent: AbstractResource):
        super().__init__(parent)
        self.challenge = data["challenge"]
        self.client = data["client"]
        self.oidc_context = data["oidc_context"]
        self.request_url = data["request_url"]
        self.requested_access_token_audience = data["requested_access_token_audience"]
        self.requested_scope = data["requested_scope"]
        self.session_id = data["session_id"]
        self.skip = data["skip"]
        self.subject = data["subject"]

    @classmethod
    def params(cls, challenge: str) -> dict:
        return {"login_challenge": challenge}

    @classmethod
    def get(cls, challenge: str, hydra: Hydra) -> LoginRequest:
        url = urljoin(hydra.url, cls.endpoint)
        response = hydra._request("GET", url, cls.params(challenge))
        return cls(response.json(), hydra)

    def accept(
        self,
        subject: str,
        acr: str = None,
        context: dict = None,
        force_subject_identifier: str = None,
        remember: bool = False,
        remember_for: int = None,
    ) -> str:
        data = filter_none(
            {
                "acr": acr,
                "context": context,
                "force_subject_identifier": force_subject_identifier,
                "remember": remember,
                "remember_for": remember_for,
                "subject": subject,
            }
        )
        url = urljoin(self.url, "accept")
        response = self._request(
            "PUT", url, params=self.params(self.challenge), json=data
        )
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
        response = self._request(
            "PUT", url, params=self.params(self.challenge), json=data
        )
        payload = response.json()
        return payload["redirect_to"]


class LoginSession(AbstractResource):

    endpoint = "/oauth2/auth/sessions/login"

    @classmethod
    def params(cls, subject: str) -> dict:
        return {"subject": subject}

    @classmethod
    def invalidate(cls, subject: str, hydra: Hydra) -> None:
        url = urljoin(hydra.url, cls.endpoint)
        # This returns 204/201 without any content
        hydra._request("DELETE", url, params=cls.params(subject))
