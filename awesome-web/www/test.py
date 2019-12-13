import orm
from models import User, Blog, Comment

def test():
    yield from orm.create_connect_pool(db='awesome')

    u = User(name='Test', email='test@example.com', passwd='123')

    yield from u.save()

for x in test():
    pass