from __future__ import annotations

from datetime import datetime
import typing

import attr
import dateutil.parser

from .model import Entity, list_attr, optional_from_dict, Resource
from .utils import filter_none, urljoin

if typing.TYPE_CHECKING:
    from .api import HydraAdmin


@attr.s(auto_attribs=True, kw_only=True)
class JSONWebKey(Entity):
    alg: str
    crv: str
    d: str
    dp: str
    dq: str
    e: str
    k: str
    kid: str
    kty: str
    n: str
    p: str
    q: str
    qi: str
    use: str
    x: str
    x5c: str
    y: str


@attr.s(auto_attribs=True, kw_only=True)
class JSONWebKeySet(Entity):
    keys: typing.List[JSONWebKey] = list_attr(JSONWebKey, factory=list)


@attr.s(auto_attribs=True, kw_only=True)
class OAuth2Client(Resource):
    allowed_cors_origins: typing.List[str]
    audience: typing.List[str]
    backchannel_logout_session_required: bool = False
    backchannel_logout_uri: str = ""
    client_id: str
    client_name: str
    client_secret: typing.Optional[str] = None
    client_secret_expires_at: datetime = attr.ib(
        converter=datetime.fromtimestamp  # type: ignore
    )
    client_uri: str
    contacts: typing.List[str]
    frontchannel_logout_session_required: bool = False
    frontchannel_logout_uri: str = ""
    grant_types: typing.List[str]
    jwks: typing.Optional[JSONWebKeySet] = attr.ib(
        converter=optional_from_dict(JSONWebKeySet),  # type: ignore
        default=None,
    )
    jwks_uri: str = ""
    logo_uri: str
    owner: str
    policy_uri: str
    post_logout_redirect_uris: typing.List[str] = attr.ib(factory=list)
    redirect_uris: typing.List[str] = attr.ib(factory=list)
    request_object_signing_alg: typing.Optional[str] = None
    request_uris: typing.List[str] = attr.ib(factory=list)
    response_types: typing.List[str]
    scope: str
    sector_identifier_uri: typing.Optional[str] = None
    subject_type: str
    token_endpoint_auth_method: str
    tos_uri: str
    updated_at: datetime = attr.ib(converter=dateutil.parser.parse)
    userinfo_signed_response_alg: str

    url_ = "/clients"

    def _post_bind(self):
        self.url_ = urljoin(self.parent_.url_, self.url_, self.client_id)

    @classmethod
    def _list(
        cls, api: HydraAdmin, limit: int = None, offset: int = None
    ) -> typing.List[OAuth2Client]:
        url = urljoin(api.url_, cls.url_)
        params = filter_none({"limit": limit, "offset": offset})
        response = api._request("GET", url, params=params)
        payload = response.json()
        return [OAuth2Client._from_dict(d, parent=api) for d in payload]

    @classmethod
    def create(
        cls,
        api: HydraAdmin,
        allowed_cors_origins: typing.List[str] = None,
        audience: typing.List[str] = None,
        backchannel_logout_session_required: bool = None,
        backchannel_logout_uri: str = None,
        client_id: str = None,
        client_name: str = None,
        client_secret: str = None,
        client_secret_expires_at: int = None,
        client_uri: str = None,
        contacts: typing.List[str] = None,
        frontchannel_logout_session_required: bool = None,
        frontchannel_logout_uri: str = None,
        grant_types: typing.List[str] = None,
        jwks: dict = None,
        jwks_uri: str = None,
        logo_uri: str = None,
        owner: str = None,
        policy_uri: str = None,
        post_logout_redirect_uris: typing.List[str] = None,
        redirect_uris: typing.List[str] = None,
        redirect_object_signing_alg: str = None,
        request_uris: typing.List[str] = None,
        response_uris: typing.List[str] = None,
        scope: str = None,
        sector_identifier_uri: str = None,
        subject_type: str = None,
        token_endpoint_auth_method: str = None,
        tos_uri: str = None,
        userinfo_signed_response_alg: str = None,
    ) -> OAuth2Client:
        url = urljoin(api.url_, cls.url_)
        data = filter_none(
            {
                "allowed_cors_origins": allowed_cors_origins,
                "audience": audience,
                "backchannel_logout_session_required": backchannel_logout_session_required,
                "backchannel_logout_uri": backchannel_logout_uri,
                "client_id": client_id,
                "client_name": client_name,
                "client_secret": client_secret,
                "client_secret_expires_at": client_secret_expires_at,
                "client_uri": client_uri,
                "contacts": contacts,
                "frontchannel_logout_session_required": frontchannel_logout_session_required,
                "frontchannel_logout_uri": frontchannel_logout_uri,
                "grant_types": grant_types,
                "jwks": jwks,
                "jwks_uri": jwks_uri,
                "logo_uri": logo_uri,
                "owner": owner,
                "policy_uri": policy_uri,
                "post_logout_redirect_uris": post_logout_redirect_uris,
                "redirect_uris": redirect_uris,
                "redirect_object_signing_alg": redirect_object_signing_alg,
                "request_uris": request_uris,
                "response_uris": response_uris,
                "scope": scope,
                "sector_identifier_uri": sector_identifier_uri,
                "subject_type": subject_type,
                "token_endpoint_auth_method": token_endpoint_auth_method,
                "tos_uri": tos_uri,
                "userinfo_signed_response_alg": userinfo_signed_response_alg,
            }
        )
        response = api._request("POST", url, json=data)
        return cls._from_dict(response.json(), parent=api)

    @classmethod
    def _get(cls, api: HydraAdmin, client_id: str) -> OAuth2Client:
        url = urljoin(api.url_, cls.url_, client_id)
        response = api._request("GET", url)
        return cls._from_dict(response.json(), parent=api)

    def update(
        self,
        allowed_cors_origins: typing.List[str] = None,
        audience: typing.List[str] = None,
        backchannel_logout_session_required: bool = None,
        backchannel_logout_uri: str = None,
        client_id: str = None,
        client_name: str = None,
        client_secret: str = None,
        client_secret_expires_at: int = None,
        client_uri: str = None,
        contacts: typing.List[str] = None,
        frontchannel_logout_session_required: bool = None,
        frontchannel_logout_uri: str = None,
        grant_types: typing.List[str] = None,
        jwks: dict = None,
        jwks_uri: str = None,
        logo_uri: str = None,
        owner: str = None,
        policy_uri: str = None,
        post_logout_redirect_uris: typing.List[str] = None,
        redirect_uris: typing.List[str] = None,
        redirect_object_signing_alg: str = None,
        request_uris: typing.List[str] = None,
        response_uris: typing.List[str] = None,
        scope: str = None,
        sector_identifier_uri: str = None,
        subject_type: str = None,
        token_endpoint_auth_method: str = None,
        tos_uri: str = None,
        userinfo_signed_response_alg: str = None,
    ) -> OAuth2Client:
        data = filter_none(
            {
                "allowed_cors_origins": allowed_cors_origins,
                "audience": audience,
                "backchannel_logout_session_required": backchannel_logout_session_required,
                "backchannel_logout_uri": backchannel_logout_uri,
                "client_id": client_id,
                "client_name": client_name,
                "client_secret": client_secret,
                "client_secret_expires_at": client_secret_expires_at,
                "client_uri": client_uri,
                "contacts": contacts,
                "frontchannel_logout_session_required": frontchannel_logout_session_required,
                "frontchannel_logout_uri": frontchannel_logout_uri,
                "grant_types": grant_types,
                "jwks": jwks,
                "jwks_uri": jwks_uri,
                "logo_uri": logo_uri,
                "owner": owner,
                "policy_uri": policy_uri,
                "post_logout_redirect_uris": post_logout_redirect_uris,
                "redirect_uris": redirect_uris,
                "redirect_object_signing_alg": redirect_object_signing_alg,
                "request_uris": request_uris,
                "response_uris": response_uris,
                "scope": scope,
                "sector_identifier_uri": sector_identifier_uri,
                "subject_type": subject_type,
                "token_endpoint_auth_method": token_endpoint_auth_method,
                "tos_uri": tos_uri,
                "userinfo_signed_response_alg": userinfo_signed_response_alg,
            }
        )
        response = self._request("PUT", self.url_, json=data)
        payload = response.json()
        # Create another instance, so all converters are run
        other = self._from_dict(payload, parent=self.parent_)
        self.__dict__.update(other.__dict__)
        return self

    def delete(self) -> None:
        self._request("DELETE", self.url_)
