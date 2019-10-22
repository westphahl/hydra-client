from hydra_client.common import OpenIDConnectContext
from hydra_client.oauth2 import OAuth2Client


def test_login_request_create(hydra_admin, login_challenge):
    login_request = hydra_admin.login_request(login_challenge)
    assert login_request
    # Ensure proper subresource init and binding
    assert isinstance(login_request.client, OAuth2Client)
    assert login_request.client.parent_ is login_request
    assert isinstance(login_request.oidc_context, OpenIDConnectContext)


def test_login_request_accept(login_request):
    redirect = login_request.accept("subject")
    assert redirect.startswith("http"), redirect


def test_login_request_reject(login_request):
    redirect = login_request.reject()
    assert redirect.startswith("http"), redirect


def test_invalidate_login_sessions(hydra_admin, accepted_consent_request):
    hydra_admin.invalidate_login_sessions(accepted_consent_request.subject)
