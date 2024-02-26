from httpx import AsyncClient


async def test_delete_user(
    client: AsyncClient, user_test_samples, get_user, test_auth_headers
):
    test_user_id = 1
    resp = await client.delete(
        f"/user/{test_user_id}", headers=test_auth_headers
    )

    assert resp.status_code == 200

    db_user = await get_user(test_user_id)
    assert db_user is None


async def test_delete_not_found_user(
    client: AsyncClient, create_tables, test_auth_headers
):
    test_user_id = 123
    resp = await client.delete(
        f"/user/{test_user_id}", headers=test_auth_headers
    )

    assert resp.status_code == 404
    assert resp.json().get("detail") == f"User {test_user_id} not found"


async def test_delete_without_auth(client: AsyncClient):
    resp = await client.delete("/user/1")

    assert resp.status_code == 401
    assert resp.json().get("detail") == "Not authenticated"


async def test_delete_with_bad_auth(client: AsyncClient, test_auth_headers):
    test_auth_headers["Authorization"] += "a"
    resp = await client.delete("/user/1", headers=test_auth_headers)

    assert resp.status_code == 401
    assert resp.json().get("detail") == "Invalid token"
