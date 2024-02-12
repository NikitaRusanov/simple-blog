from httpx import AsyncClient

from src import User


async def test_get_all_users(user_test_samples: list[User], client: AsyncClient):
    resp = await client.get("/user")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert len(resp_data) == 3

    assert resp_data[0].get("id") == user_test_samples[0].id
    assert resp_data[1].get("id") == user_test_samples[1].id
    assert resp_data[2].get("id") == user_test_samples[2].id

    assert resp_data[0].get("username") == user_test_samples[0].username
    assert resp_data[1].get("username") == user_test_samples[1].username
    assert resp_data[2].get("username") == user_test_samples[2].username

    assert resp_data[0].get("email") == user_test_samples[0].email
    assert resp_data[1].get("email") == user_test_samples[1].email
    assert resp_data[2].get("email") == user_test_samples[2].email

    assert all(["password" not in user for user in resp_data])


async def test_get_all_users_empty(create_tables, client: AsyncClient):
    resp = await client.get("/user/")

    assert resp.status_code == 200
    assert len(resp.json()) == 0


async def test_get_one_user(user_test_samples: list[User], client: AsyncClient):
    target_user = user_test_samples[1]
    resp = await client.get(f"/user/{target_user.id}")
    resp_data = resp.json()

    assert resp_data.get("id") == target_user.id
    assert resp_data.get("username") == target_user.username
    assert resp_data.get("email") == target_user.email


async def test_ueser_not_found(client: AsyncClient, create_tables):
    test_user_id = 1
    resp = await client.get(f"/user/{test_user_id}")

    assert resp.status_code == 404
    assert resp.json().get("detail") == f"User {test_user_id} not found"
