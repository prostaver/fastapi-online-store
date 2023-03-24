import random
import string
import logging

from sqlalchemy.orm import Session

from config.database import get_db_connection
from models.user import User
from py_schemas.user import CreateUser
# from services.hash_service import hash_password
from services import user_service


log = logging.getLogger(__name__)


def test_user():
    create_valid_users()
    update_username()
    update_username_and_password()
    get_users()
    get_user()
    delete_user()


def create_valid_users():
    db: Session = get_db_connection().__next__()
    for i in range(10):
        rand_user_range = random.randrange(15, 20)
        rand_pw_range = random.randrange(15, 50)
        rand_username = ''.join(random.choices((string.ascii_letters+string.digits+"@-_"), k=rand_user_range))
        rand_pw = ''.join(random.choices((string.ascii_letters+string.digits+string.punctuation), k=rand_pw_range))
        user = CreateUser(username=rand_username, password=rand_pw)

        assert user_service.create_user(db, user)
    # db.query(User.id).all()


def update_username():
    db: Session = get_db_connection().__next__()
    user_ids = db.query(User.id).all()
    # user_ids = [1, 2, 3, 4, 5]
    user_sub_list = user_ids[:3]
    # print(first_three_ids)
    for user_id in user_sub_list:
        user_input = CreateUser(username=''.join(random.choices((string.ascii_letters+string.digits+"@-_"), k=18)))
        assert user_service.update_user(db, user_input, user_id[0])
        # print(user_id)


def update_username_and_password():
    db: Session = get_db_connection().__next__()
    user_ids = db.query(User.id).all()
    user_sub_list = user_ids[4:]
    for user_id in user_sub_list:
        user_input = CreateUser(
            username=''.join(random.choices((string.ascii_letters + string.digits + "@-_"), k=18)),
            password=''.join(random.choices((string.ascii_letters+string.digits+string.punctuation), k=15))
        )
        assert user_service.update_user(db, user_input, user_id[0])


def get_users():
    db: Session = get_db_connection().__next__()
    assert user_service.get_users(db)


def get_user():
    db: Session = get_db_connection().__next__()
    user_ids = db.query(User.id).all()

    for user_id in user_ids:
        assert user_service.get_user(db, user_id[0])


def delete_user():
    db: Session = get_db_connection().__next__()
    user_ids = db.query(User.id).all()

    for user_id in user_ids:
        assert user_service.delete_user(db, user_id[0])
