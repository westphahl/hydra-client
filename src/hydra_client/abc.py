from __future__ import annotations

import abc
import typing

import requests

from . import exceptions
from .utils import urljoin

if typing.TYPE_CHECKING:
    from .client import Hydra


class AbstractResource(abc.ABC):
    def __init__(self, resource: AbstractResource = None):
        if resource is not None:
            self._session: requests.Session = resource._session
            self.url: str = resource.url
        else:
            self._session = requests.Session()
            self.url = ""

    def _request(
        self, method: str, url: str, params: dict = None, json: dict = None
    ) -> requests.Response:
        try:
            response = self._session.request(method, url, params=params, json=json)
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
        ) as exc:
            raise exceptions.ConnectionError from exc
        except requests.exceptions.RequestException as exc:
            raise exceptions.TransportError from exc

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            wrapper_exc = exceptions.status_map.get(
                exc.response.status_code, exceptions.HTTPError
            )
            raise wrapper_exc from exc

        return response


class AbstractEndpoint(AbstractResource):
    def __init__(self, resource: AbstractResource = None):
        super().__init__(resource)
        self.url = urljoin(self.url, self.endpoint)

    @abc.abstractproperty
    def endpoint(self) -> str:
        pass
