from models.users import Users
from utils.connection import connection
from sqlalchemy.orm import sessionmaker

class BaseRepository:
    def __init__(self):
        self.Session = sessionmaker(connection)
        self.db = self.Session()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()
        if exc_type:
            self.db.rollback()
        else:
            self.db.commit()

class AuthRepository(BaseRepository):
    def login(self, username: str, password: str) -> Users:
        with self as db:
            user = db.query(Users).filter(Users.username == username).filter(Users.is_deleted==0).first()
            if not user or not user.check_password(password):
                return None
            users = {
                "id": user.id,
                "username": user.username,
                "fullname": user.fullname
            }

            return users
        