from sqlalchemy import insert, select
from src.auth.models import User, Post
from tests.confest import async_session_maker, client


async def test_add_user():
    async with async_session_maker() as session:
        smtp = insert(Post).values(id=1, title='fk', slug='fkoew', description='geoir')
        await session.execute(smtp)
        await session.commit()

        result = select(Post)
        result_1 = await session.execute(result)
        assert result_1.all()
# assert 1 == 1
# query = select(User)
# result = server.execute(query)
# print(result.all())
# assert result.all() == [(23, 'rtgokopt', 'log@gmail.com', "loglgo", True, False)]


# def test_register_user_id():
#     response = client.post("/users/", json={
#         "email": "zlava@gmail.com",
#         "is_active": True,
#         "is_superuser": False,
#         "full_name": "zlava",
#         "id": 1,
#         "hashed_password": "zlava"
#     })
#     assert response.status_code == 201

# def test_register():
#     client.post('/open/', json={
#         "email": 'zlava@gmail.com',
#         "password": '12345',
#         "full_name": 'lava'
#     })
