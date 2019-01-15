import pytest

from hydra_client.client import OAuth2Client
from hydra_client import exceptions


def test_client_list(hydra_admin, oauth2_client):
    client_list = hydra_admin.clients()
    assert all(isinstance(c, OAuth2Client) for c in client_list)
    # assert oauth2_client in client_list


def test_client_create(hydra_admin):
    client = hydra_admin.create_client()
    assert isinstance(client, OAuth2Client)
    assert client.client_secret


def test_client_get(hydra_admin, oauth2_client):
    client = hydra_admin.client(oauth2_client.client_id)
    assert isinstance(client, OAuth2Client)
    # assert oauth2_client == client


def test_client_update(oauth2_client):
    new_name = "foobar"
    assert oauth2_client.client_name != new_name
    oauth2_client.update(client_name=new_name)
    assert oauth2_client.client_name == new_name


def test_client_delete(hydra_admin, oauth2_client):
    oauth2_client.delete()
    with pytest.raises(exceptions.NotFound):
        hydra_admin.client(oauth2_client.client_id)
