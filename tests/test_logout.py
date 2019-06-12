def test_logout_request_create(hydra_admin, logout_challenge):
    logout_request = hydra_admin.logout_request(logout_challenge)
    assert logout_request


def test_logout_request_accept(logout_request):
    redirect = logout_request.accept("subject")
    assert redirect.startswith("http"), redirect


def test_logout_request_reject(logout_request):
    # Only making sure this is returnin a 2xx status code
    logout_request.reject()
