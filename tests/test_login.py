def test_login_request_create(hydra_admin, login_challenge):
    login_request = hydra_admin.login_request(login_challenge)
    assert login_request


def test_login_request_accept(login_request):
    redirect = login_request.accept("subject")
    assert redirect.startswith("http"), redirect


def test_login_request_reject(login_request):
    redirect = login_request.reject()
    assert redirect.startswith("http"), redirect


def test_invalidate_login_sessions(hydra_admin, accepted_consent_request):
    hydra_admin.invalidate_login_sessions(accepted_consent_request.subject)
