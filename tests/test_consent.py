from urllib.parse import parse_qs, urlsplit
import pytest


def test_consent_request_create(hydra_admin, consent_challenge):
    consent_request = hydra_admin.consent_request(consent_challenge)
    assert consent_request


def test_consent_request_accept(consent_request):
    redirect = consent_request.accept()
    assert redirect.startswith("http"), redirect


def test_consent_request_reject(consent_request):
    redirect = consent_request.reject()
    assert redirect.startswith("http"), redirect
