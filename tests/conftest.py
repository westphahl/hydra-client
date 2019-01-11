import os
from urllib.parse import urlsplit, parse_qs

import betamax
import pytest
from betamax.fixtures.pytest import _casette_name
from requests_oauthlib import OAuth2Session

from hydra_client import HydraAdmin


@pytest.fixture(scope="session", autouse=True)
def configure_betamax():
    path = os.path.join(os.path.dirname(__file__), "cassettes")
    config = betamax.Betamax.configure()
    config.cassette_library_dir = path
    record_mode = os.environ.get("BETAMAX_RECORD_MODE", "once")
    config.default_cassette_options["record_mode"] = record_mode


@pytest.fixture
def oauth2_session():
    # Allow connecting non-encrypted OAuth2 endpoint for testing
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "ok"
    client_id = os.environ.get("OAUTH2_CLIENT_ID", "test-client")
    # TODO: Get client config from environ
    redirect_uri = "http://client.local"
    oauth = OAuth2Session(
        client_id, redirect_uri=redirect_uri, scope=["openid", "offline"]
    )
    return oauth


@pytest.fixture
def betamax_oauth2_session(request, oauth2_session):
    cassette_name = _casette_name(request, parametrized=True)
    recorder = betamax.Betamax(oauth2_session)
    recorder.use_cassette(cassette_name)
    recorder.start()
    request.addfinalizer(recorder.stop)
    return oauth2_session


@pytest.fixture
def login_challenge(betamax_session, betamax_oauth2_session):
    # TODO: get public URL from environ
    url, state = betamax_oauth2_session.authorization_url(
        "http://localhost:4444/oauth2/auth", state="iampredictable"
    )
    response = betamax_session.get(url, allow_redirects=False)
    params = parse_qs(urlsplit(response.headers["Location"]).query)
    return params["login_challenge"][0]


@pytest.fixture
def hydra_admin(betamax_session):
    # TODO: get admin URL from environ
    hydra_admin = HydraAdmin("http://localhost:4445")
    hydra_admin.session = betamax_session
    return hydra_admin


@pytest.fixture
def login_request(hydra_admin, login_challenge):
    return hydra_admin.login_request(login_challenge)


@pytest.fixture
def consent_challenge(hydra_admin, betamax_session, login_request):
    redirect = login_request.accept(subject="foobar")
    response = betamax_session.get(redirect, allow_redirects=False)
    params = parse_qs(urlsplit(response.headers["Location"]).query)
    return params["consent_challenge"][0]


@pytest.fixture
def consent_request(hydra_admin, consent_challenge):
    return hydra_admin.consent_request(consent_challenge)
