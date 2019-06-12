from __future__ import annotations

import typing

from .abc import AbstractEndpoint, AbstractResource
from .utils import filter_none, urljoin

if typing.TYPE_CHECKING:
    from .client import Hydra


class OAuth2Client(AbstractEndpoint):

    endpoint = "/clients"

    def __init__(self, data: dict, parent: AbstractResource):
        super().__init__(parent)
        self._update(data)
        self.url = urljoin(self.url, self.client_id)

    def _update(self, data: dict):
        self.allowed_cors_origins = data["allowed_cors_origins"]
        self.audience = data["audience"]
        self.backchannel_logout_session_required = data.get(
            "backchannel_logout_session_required"
        )
        self.backchannel_logout_uri = data.get("backchannel_logout_uri")
        self.client_id = data["client_id"]
        self.client_name = data["client_name"]
        self.client_secret = data.get("client_secret")
        self.client_secret_expires_at = data["client_secret_expires_at"]
        self.client_uri = data["client_uri"]
        self.contacts = data["contacts"]
        self.frontchannel_logout_session_required = data.get(
            "frontchannel_logout_session_required"
        )
        self.frontchannel_logout_uri = data.get("frontchannel_logout_uri")
        self.grant_types = data["grant_types"]
        self.jwks = data.get("jwks")
        self.jwks_uri = data.get("jwks_uri", [])
        self.logo_uri = data["logo_uri"]
        self.owner = data["owner"]
        self.policy_uri = data["policy_uri"]
        self.post_logout_redirect_uris = data.get("post_logout_redirect_uris")
        self.redirect_uris = data["redirect_uris"]
        self.request_object_signing_alg = data.get("request_object_signing_alg")
        self.request_uris = data.get("request_uris", [])
        self.response_types = data["response_types"]
        self.scope = data["scope"]
        self.sector_identifier_uri = data.get("sector_identifier_uri")
        self.subject_type = data["subject_type"]
        self.token_endpoint_auth_method = data["token_endpoint_auth_method"]
        self.tos_uri = data["tos_uri"]
        self.updated_at = data["updated_at"]
        self.userinfo_signed_response_alg = data["userinfo_signed_response_alg"]

    @classmethod
    def list(
        cls, hydra: Hydra, limit: int = None, offset: int = None
    ) -> typing.List[OAuth2Client]:
        url = urljoin(hydra.url, cls.endpoint)
        params = filter_none({"limit": limit, "offset": offset})
        response = hydra._request("GET", url, params=params)
        payload = response.json()
        return [OAuth2Client(d, hydra) for d in payload]

    @classmethod
    def create(
        cls,
        hydra: Hydra,
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
        url = urljoin(hydra.url, cls.endpoint)
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
        response = hydra._request("POST", url, json=data)
        return cls(response.json(), hydra)

    @classmethod
    def get(cls, client_id: str, hydra: Hydra) -> OAuth2Client:
        url = urljoin(hydra.url, cls.endpoint, client_id)
        response = hydra._request("GET", url)
        return cls(response.json(), hydra)

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
        response = self._request("PUT", self.url, json=data)
        payload = response.json()
        self._update(payload)
        return self

    def delete(self) -> None:
        self._request("DELETE", self.url)
