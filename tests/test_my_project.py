from sqlalchemy import insert, select

from src.db.base_class import Base
from src.auth.models import operation
from tests.confest import SessionLocal



def test_add_user():
    server = SessionLocal()
    try:
        smtp = insert(operation).values(id=1, quantity='13', name='hello')
        server.execute(smtp)
        print(smtp)
        server.commit()

        # query = select(User)
        # result = server.execute(query)
        # print(result.all())
        # assert result.all() == [(23, 'rtgokopt', 'log@gmail.com', "loglgo", True, False)]


    finally:
        server.close()

# def test_register():
#     client.post('/open/', json={
#         "email": 'zlava@gmail.com',
#         "password": '12345',
#         "full_name": 'lava'
#     })
