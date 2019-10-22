from __future__ import annotations

import typing

import attr

from .common import OpenIDConnectContext
from .model import Entity, optional_from_dict, Resource
from .oauth2 import OAuth2Client
from .utils import filter_none, urljoin

if typing.TYPE_CHECKING:
    from .api import HydraAdmin


@attr.s(auto_attribs=True, kw_only=True)
class ConsentRequest(Resource):
    acr: str
    challenge: str
    client: OAuth2Client = attr.ib(
        converter=OAuth2Client._from_dict  # type: ignore
    )
    context: dict = attr.ib(factory=dict)
    login_challenge: str
    login_session_id: str
    oidc_context: OpenIDConnectContext = attr.ib(
        converter=OpenIDConnectContext._from_dict  # type: ignore
    )
    request_url: str
    requested_access_token_audience: typing.List[str]
    requested_scope: typing.List[str]
    skip: bool
    subject: str

    url_ = "/oauth2/auth/requests/consent"

    def _post_bind(self) -> None:
        self.url_ = urljoin(self.parent_.url_, self.url_)

    @classmethod
    def _params(cls, challenge: str) -> dict:
        return {"consent_challenge": challenge}

    @classmethod
    def _get(cls, api: HydraAdmin, challenge: str) -> ConsentRequest:
        url = urljoin(api.url_, cls.url_)
        response = api._request("GET", url, params=cls._params(challenge))
        payload = response.json()
        return cls._from_dict(payload, parent=api)

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
class ConsentRequestSession(Entity):
    access_token: dict
    id_token: dict


@attr.s(auto_attribs=True, kw_only=True)
class ConsentSession(Resource):
    consent_request: ConsentRequest = attr.ib(
        converter=ConsentRequest._from_dict  # type: ignore
    )
    grant_access_token_audience: typing.List[str]
    grant_scope: typing.List[str]
    remember: bool
    remember_for: int
    session: typing.Optional[ConsentRequestSession] = attr.ib(
        converter=optional_from_dict(ConsentRequestSession),  # type: ignore
        default=None,
    )

    url_ = "/oauth2/auth/sessions/consent"

    @classmethod
    def _params(cls, subject: str, client: str = None) -> dict:
        return filter_none({"subject": subject, "client": client})

    @classmethod
    def _list(cls, api: HydraAdmin, subject: str) -> typing.Iterator[ConsentSession]:
        url = urljoin(api.url_, cls.url_)
        response = api._request("GET", url, params=cls._params(subject))
        session_list = response.json()
        for consent_session in session_list:
            yield ConsentSession._from_dict(consent_session, parent=api)

    @classmethod
    def _revoke(
        cls, api: HydraAdmin, subject: str, client: typing.Optional[str]
    ) -> None:
        url = urljoin(api.url_, cls.url_)
        # This returns 204/201 without any content
        api._request("DELETE", url, params=cls._params(subject, client))
