from hydra_client.common import OpenIDConnectContext
from hydra_client.consent import ConsentRequest, ConsentSession
from hydra_client.oauth2 import OAuth2Client

from urllib.parse import parse_qs, urlsplit
import pytest


def test_consent_request_create(hydra_admin, consent_challenge):
    consent_request = hydra_admin.consent_request(consent_challenge)
    assert consent_request
    # Ensure proper subresource init and binding
    assert isinstance(consent_request.client, OAuth2Client)
    assert consent_request.client.parent_ is consent_request
    assert isinstance(consent_request.oidc_context, OpenIDConnectContext)


def test_consent_request_accept(consent_request):
    redirect = consent_request.accept()
    assert redirect.startswith("http"), redirect


def test_consent_request_reject(consent_request):
    redirect = consent_request.reject()
    assert redirect.startswith("http"), redirect


def test_list_consent_sessions(hydra_admin, accepted_consent_request):
    session_iter = hydra_admin.consent_sessions(accepted_consent_request.subject)
    session_list = list(session_iter)
    assert session_list
    assert all(isinstance(c, ConsentSession) for c in session_list)
    consent_session = session_list[0]
    assert isinstance(consent_session.consent_request, ConsentRequest)
    assert consent_session.consent_request.parent_ is consent_session
    assert consent_session.session is None
    # assert accepted_consent_request in session_list


def test_revoke_consent_sessions(hydra_admin, accepted_consent_request):
    hydra_admin.revoke_consent_sessions(accepted_consent_request.subject)
    session_iter = hydra_admin.consent_sessions(accepted_consent_request.subject)
    assert not list(session_iter)
