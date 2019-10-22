from __future__ import annotations

import collections
import typing

import attr
import requests

from . import exceptions

T = typing.TypeVar("T", bound="Entity")
U = typing.TypeVar("U", bound="Resource")


class Entity:
    @classmethod
    def _from_dict(cls: typing.Type[T], data: dict) -> T:
        fields = attr.fields_dict(cls)
        clean_data = {k: v for k, v in data.items() if k in fields}
        return cls(**clean_data)  # type: ignore


class Resource(Entity):
    url_: str

    def _request(
        self, method: str, url: str, params: dict = None, json: dict = None
    ) -> requests.Response:
        try:
            response = typing.cast(
                requests.Response,
                self.session_.request(method, url, params=params, json=json),
            )
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
        ) as exc:
            raise exceptions.ConnectionError from exc
        except requests.exceptions.RequestException as exc:
            raise exceptions.TransportError from exc
        except AttributeError:
            raise exceptions.UnboundResourceError

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            wrapper_exc = exceptions.status_map.get(
                exc.response.status_code, exceptions.HTTPError
            )
            raise wrapper_exc from exc
        return response

    def _post_bind(self) -> None:
        pass

    def _bind(self, parent: Resource) -> None:
        self.parent_ = parent
        self.session_ = getattr(self.parent_, "session_", None)
        self._post_bind()
        for field in attr.fields(self.__class__):
            value = getattr(self, field.name)
            try:
                value._bind(self)
            except AttributeError:
                pass

    @classmethod
    def _from_dict(cls: typing.Type[U], data: dict, parent: Resource = None) -> U:
        instance = super()._from_dict(data)
        if parent is not None:
            instance._bind(parent)
        return instance


class ResourceList(collections.UserList):
    def _bind(self, parent: Resource) -> None:
        for item in self:
            try:
                item._bind(parent)
            except AttributeError:
                pass


def list_attr(klass: typing.Type[Entity], factory=None) -> typing.Any:
    def converter(entity_list: typing.List[dict]) -> ResourceList:
        if entity_list is None:
            entity_list = []
        return ResourceList(klass._from_dict(d) for d in entity_list)

    return attr.ib(converter=converter, factory=factory)


def optional_from_dict(
    klass: typing.Type[T]
) -> typing.Callable[[dict], typing.Optional[T]]:
    def converter(data: dict) -> typing.Optional[T]:
        if data is None:
            return None
        return klass._from_dict(data)

    return converter
