from httpx import AsyncClient
import pytest

from tests.test_auth.conftest import USER_DATA
from src.auth.utils import decode_token


async def test_successful_login(client: AsyncClient, create_user):
    login_data = {
        "username": USER_DATA["username"],
        "password": USER_DATA["password"]
    }

    resp = await client.post("/auth/login", data=login_data)
    assert resp.status_code == 200

    token = resp.json().get("access_token")
    payload = decode_token(token)
    assert payload["sub"] == create_user.id
    assert payload["username"] == create_user.username


@pytest.mark.parametrize("username, password", [
    (USER_DATA["username"], "1"),
    ("1", USER_DATA["password"])
])
async def test_wrong_data_login(username, password, client: AsyncClient, create_user, ):
    login_data = {
        "username": username,
        "password": password
    }

    resp = await client.post("/auth/login", data=login_data)
    assert resp.status_code == 401
    assert resp.json().get("detail") == "Wrong username or password"