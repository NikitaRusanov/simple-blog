from httpx import AsyncClient


async def test_create_user(client: AsyncClient, get_user):
    test_data = {
        'username': 'test_user',
        'email': 'test@mail.com',
        'password': 'test_pass'
    }
    resp = await client.post('/user/', json=test_data)
    resp_data = resp.json()

    assert resp.status_code == 201
    
    db_user = await get_user(resp_data.get('id'))
    assert db_user.username == test_data['username']
    assert db_user.email == test_data['email']
    assert db_user.password == test_data['password']