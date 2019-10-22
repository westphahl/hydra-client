from __future__ import annotations

import typing

import attr

from .common import OpenIDConnectContext
from .model import Resource
from .oauth2 import OAuth2Client
from .utils import filter_none, urljoin

if typing.TYPE_CHECKING:
    from .api import HydraAdmin


@attr.s(auto_attribs=True, kw_only=True)
class LoginRequest(Resource):
    challenge: str
    client: OAuth2Client = attr.ib(
        converter=OAuth2Client._from_dict  # type: ignore
    )
    oidc_context: OpenIDConnectContext = attr.ib(
        converter=OpenIDConnectContext._from_dict  # type: ignore
    )

    request_url: str
    requested_access_token_audience: typing.List[str]
    requested_scope: typing.List[str]
    session_id: str
    skip: bool
    subject: str
    url_ = "/oauth2/auth/requests/login"

    def _post_bind(self):
        self.url_ = urljoin(self.parent_.url_, self.url_)

    @classmethod
    def _params(cls, challenge: str) -> dict:
        return {"login_challenge": challenge}

    @classmethod
    def _get(cls, api: HydraAdmin, challenge: str) -> LoginRequest:
        url = urljoin(api.url_, cls.url_)
        response = api._request("GET", url, cls._params(challenge))
        return cls._from_dict(response.json(), parent=api)

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
    ) -> str:
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
        response = self._request(
            "PUT", url, params=self._params(self.challenge), json=data
        )
        payload = response.json()
        return payload["redirect_to"]


@attr.s(auto_attribs=True, kw_only=True)
class LoginSession(Resource):

    url_ = "/oauth2/auth/sessions/login"

    def _post_bind(self):
        self.url_ = urljoin(self.parent_.url_, self.url_)

    @classmethod
    def _params(cls, subject: str) -> dict:
        return {"subject": subject}

    @classmethod
    def _invalidate_all(cls, api: HydraAdmin, subject: str) -> None:
        url = urljoin(api.url_, cls.url_)
        # This returns 204/201 without any content
        api._request("DELETE", url, params=cls._params(subject))
