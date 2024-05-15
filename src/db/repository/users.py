from werkzeug.security import generate_password_hash, check_password_hash
from src.db.db import session

from src.db.models.users import Users
from src.db.schemas.users import UserCreate


def get_user_by_tg(tg_user_id: int):
    user = session.query(Users).filter_by(tg_user_id=tg_user_id).first()
    return user if user else None

def get_user(username: str):
    user = session.query(Users).filter_by(username=username).first()
    return user if user else None

def set_password(self, password):
    self.password = generate_password_hash(password)

def check_hash(self, password):
    return check_password_hash(self.password, password)

def create(user: UserCreate):
    try:
        is_user = get_user(user.phone_number)

        if is_user:
            return is_user
        else:
            user = Users(
                first_name = user.first_name,
                phone_number = user.phone_number,
                city_name = user.city_name,
                password = set_password(user.password)
            )
            session.add(user)
            session.commit()

            return user
    except Exception as e:
        print("create user:", e)
        session.rollback()
    finally:
        session.close()

def tg_insert(tg_id: int, tg_username: str, phone: str):
    try:
        user = session.query(Users).filter_by(phone_number=phone).first()

        if user:
            user.tg_user_id = tg_id
            user.tg_username = tg_username

            session.commit()
            return user
        else:
            return None
    except Exception as e:
        print("tg_insert:", e)
        session.rollback()
    finally:
        session.close()