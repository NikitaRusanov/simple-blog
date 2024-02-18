import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "test_data",
    [
        (
            {
                "username": "new_test_username",
                "email": "new_tets_email@mail.com",
                "password": "new_test_password",
            }
        ),
        ({"username": "new_test_username"}),
        ({"email": "new_tets_email@mail.com"}),
        ({"password": "new_test_password"}),
        ({"id": "2", "email": "new_test_email@mail.com"}),
        ({}),
    ],
)
async def test_update_user(
    test_data, client: AsyncClient, user_test_samples, get_user, test_auth_headers
):
    test_user = user_test_samples[0].__dict__.copy()
    test_user.pop("_sa_instance_state")
    test_user_id = test_user.get("id")
    test_user.update(test_data)

    resp = await client.patch(
        f"/user/{test_user_id}", json=test_data, headers=test_auth_headers
    )
    assert resp.status_code == 200

    db_user = await get_user(test_user_id)
    assert db_user.username == test_user["username"]
    assert db_user.email == test_user["email"]
    assert db_user.id == test_user_id
    assert db_user.password == test_user["password"]


async def test_user_not_found(client: AsyncClient, create_tables, test_auth_headers):
    test_user_id = 123
    resp = await client.patch(f"/user/{test_user_id}", headers=test_auth_headers)

    assert resp.status_code == 404
    assert resp.json().get("detail") == f"User {test_user_id} not found"


async def test_no_body_create(
    client: AsyncClient, user_test_samples, test_auth_headers
):
    test_user_id = 1
    resp = await client.patch(f"/user/{test_user_id}", headers=test_auth_headers)

    assert resp.status_code == 422
    assert resp.json().get("detail")[0]["type"] == "missing"
