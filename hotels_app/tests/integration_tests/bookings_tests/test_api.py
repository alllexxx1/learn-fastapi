# import pytest
#
# from httpx import AsyncClient
#
#
# @pytest.mark.parametrize(
#     'room_id, date_from, date_to, status_code',
#     [(4, '2029-06-01', '2029-07-21', 201),
# ]
# )
# async def test_add_and_get_booking(room_id, date_from, date_to, status_code, authed_async_client: AsyncClient):
#     response = await authed_async_client.post('/bookings/add', params={
#         'room_id': room_id,
#         'date_from': date_from,
#         'date_to': date_to
#     })
#
#     assert response.status_code == status_code
