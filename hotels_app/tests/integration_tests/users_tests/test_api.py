import pytest

from httpx import AsyncClient

from hotels_app.tests.conftest import authed_async_client



@pytest.mark.parametrize(
    'email, password, status_code',
    [('pass@gmail.com', '123pass', 200),
    ('pass@gmail.com', 'new_password', 409),
    ('wrong_emailgmail.com', 'brand_new', 422)]
)
async def test_register_user(
    email,
    password,
    status_code,
    async_client: AsyncClient
):
    response = await async_client.post('api/auth/register', json={
        'email': email,
        'password': password
    })
    assert response.status_code == status_code


@pytest.mark.parametrize(
    'email, password, status_code',
    [('test@test.com', 'test', 200),
    ('alex@example.com', 'pppwww', 200),
    ('alex@example.com', 'some_pass', 401)]
)
async def test_login(
    email,
    password,
    status_code,
    async_client: AsyncClient
):
    response = await async_client.post('/api/auth/login', json={
        'email': email,
        'password': password
    })
    assert response.status_code == status_code


@pytest.mark.parametrize(
    'authed, email, status_code',
    [(True, 'test@test.com', 200),
    (False, 'alex@example.com', 200)]
)
async def test_read_current_user_info(authed, email, status_code, authed_async_client: AsyncClient):
    response = await authed_async_client.get('/api/auth/me')
    response_body = response.json()

    assert response.status_code == status_code
    if authed:
        assert response_body['email'] == email
    else:
        assert response_body['email'] != email
        assert response_body['email'] == 'test@test.com'
