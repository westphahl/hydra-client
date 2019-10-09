from __future__ import annotations

import typing

import attr

from .model import Entity, Resource
from .utils import filter_none, urljoin

if typing.TYPE_CHECKING:
    from .api import HydraAdmin


@attr.s(auto_attribs=True, kw_only=True)
class LogoutRequest(Resource):
    challenge: str
    request_url: str
    rp_initiated: bool
    sid: str
    subject: str

    url_ = "/oauth2/auth/requests/logout"

    def _post_bind(self):
        self.url_ = urljoin(self.parent_.url_, self.url_)

    @classmethod
    def _params(cls, challenge: str) -> dict:
        return {"logout_challenge": challenge}

    @classmethod
    def _get(cls, api: HydraAdmin, challenge: str) -> LogoutRequest:
        url = urljoin(api.url_, cls.url_)
        response = api._request("GET", url, cls._params(challenge))
        # NOTE: we have to inject the challenge here since the endpoint doesn't
        # return it as it's the case for login/consent.
        data = response.json()
        data["challenge"] = challenge
        return cls._from_dict(data, parent=api)

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
        url = urljoin(self.url_, "accept")
        response = self._request(
            "PUT", url, params=self._params(self.challenge), json=data
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
        url = urljoin(self.url_, "reject")
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
        self._request("PUT", url, params=self._params(self.challenge), json=data)
