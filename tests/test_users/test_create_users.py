import pytest
from httpx import AsyncClient

import src.auth.utils as auth_utils


async def test_create_user(client: AsyncClient, get_user):
    test_data = {
        "username": "test_user",
        "email": "test@mail.com",
        "password": "test_pass",
    }
    resp = await client.post("/user/", json=test_data)
    resp_data = resp.json()

    assert resp.status_code == 201

    db_user = await get_user(resp_data.get("id"))
    assert db_user.username == test_data["username"]
    assert db_user.email == test_data["email"]
    assert auth_utils.check_password(test_data["password"], db_user.password)


@pytest.mark.parametrize(
    "test_data, expected_type",
    [
        ({"username": "test_user", "password": "test_pass"}, "missing"),
        ({"username": "test_user", "email": "test@mail.com"}, "missing"),
        ({"password": "test_pass", "email": "test@mail.com"}, "missing"),
        (
            {
                "username": "test_user",
                "email": "test",
                "password": "test_pass",
            },
            "value_error",
        ),
    ],
)
async def test_wrong_data_create(
    test_data, expected_type, client: AsyncClient
):
    resp = await client.post("/user/", json=test_data)

    assert resp.status_code == 422
    assert resp.json().get("detail")[0].get("type") == expected_type


async def test_exta_data_create(client: AsyncClient, create_tables):
    test_data = {
        "username": "test_user",
        "email": "test@mail.com",
        "password": "test_pass",
        "id": "123",
    }
    resp = await client.post("/user/", json=test_data)
    assert resp.status_code == 201
    assert resp.json().get("id") == 1
