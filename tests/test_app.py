from httpx import AsyncClient


async def test_app(client: AsyncClient):
    resp = await client.get('/')

    assert resp.status_code == 200
    assert resp.json().get('msg') == 'API works properly'
