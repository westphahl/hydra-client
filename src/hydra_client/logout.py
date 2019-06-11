from __future__ import annotations

import typing

from .abc import AbstractEndpoint, AbstractResource
from .utils import filter_none, urljoin

if typing.TYPE_CHECKING:
    from .client import Hydra


class LogoutRequest(AbstractEndpoint):

    endpoint = "/oauth2/auth/requests/logout"

    def __init__(self, data: dict, parent: AbstractResource):
        super().__init__(parent)
        self.challenge = data["_challenge"]
        self.request_url = data["request_url"]
        self.rp_initiated = data["rp_initiated"]
        self.sid = data["sid"]
        self.subject = data["subject"]

    @classmethod
    def params(cls, challenge: str) -> dict:
        return {"logout_challenge": challenge}

    @classmethod
    def get(cls, challenge: str, hydra: Hydra) -> LogoutRequest:
        url = urljoin(hydra.url, cls.endpoint)
        response = hydra._request("GET", url, cls.params(challenge))
        # NOTE: we have to inject the challenge here since the endpoint doesn't
        # return it as it's the case for login/consent.
        data = response.json()
        data["_challenge"] = challenge
        return cls(data, hydra)

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
    ) -> None:
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
        # This returns 204/201 without any content
        self._request("PUT", url, params=self.params(self.challenge), json=data)
