import typing

import attr

from .model import Entity


@attr.s(auto_attribs=True, kw_only=True)
class OpenIDConnectContext(Entity):
    acr_values: typing.List[str] = attr.ib(factory=list)
    display: str = ""
    id_token_hint_claims: dict = attr.ib(factory=dict)
    login_hint: str = ""
    ui_locales: typing.List[str] = attr.ib(factory=list)
