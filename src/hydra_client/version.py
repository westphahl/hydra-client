from __future__ import annotations

import typing

import requests

from . import exceptions
from .abc import AbstractEndpoint
from .utils import urljoin

if typing.TYPE_CHECKING:
    from .client import Hydra


class Version(AbstractEndpoint):

    endpoint = "/version"

    @classmethod
    def get(cls, hydra: Hydra) -> str:
        url = urljoin(hydra.url, cls.endpoint)
        response = hydra._request("GET", url)
        payload = response.json()
        return payload["version"]
