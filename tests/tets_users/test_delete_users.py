from httpx import AsyncClient


async def test_delete_user(client: AsyncClient, user_test_samples, get_user):
    test_user_id = 1
    resp = await client.delete(f'/user/{test_user_id}')

    assert resp.status_code == 200

    db_user = await get_user(test_user_id)
    assert db_user is None


async def test_delete_not_found_user(client: AsyncClient, create_tables):
    test_user_id = 1
    resp = await client.delete(f'/user/{test_user_id}')

    assert resp.status_code == 404
    assert resp.json().get('detail') == f'User {test_user_id} not found'