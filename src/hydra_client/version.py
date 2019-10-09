from __future__ import annotations

import typing

import attr

from . import exceptions
from .model import Resource
from .utils import urljoin

if typing.TYPE_CHECKING:
    from .api import HydraAdmin


@attr.s(auto_attribs=True, kw_only=True)
class Version(Resource):

    url_ = "/version"

    @classmethod
    def _get(cls, api: HydraAdmin) -> str:
        url = urljoin(api.url_, cls.url_)
        response = api._request("GET", url)
        payload = response.json()
        return payload["version"]
