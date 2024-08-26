from models.users import Users
from utils.connection import connection
from sqlalchemy.orm import sessionmaker
import uuid


class BaseRepository:
    def __init__(self):
        self.Session = sessionmaker(connection)
        self.db = self.Session()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.db.rollback()
        else:
            self.db.commit()
        self.db.close()

class UserRepository(BaseRepository):
    def insert_user(self, username, fullname, password):
        with self as db:
            id=uuid.uuid4()
            Users(id=id, username=username, fullname=fullname, password=password)
            users = {
                "id": id,
                "username": username,
                "fullname": fullname
            }
            return users

    def get_users(self):
        with self as db:
            users = db.query(Users).all()
            if not users:
                return None
            return users


    def get_user_by_id(self, id):
        with self as db:
            user = db.query(Users).filter(Users.id == id).first()
            if not user:
                return None
            return user
        
    
    def update_user(self, id, username, fullname, password):
        with self as db:
            user = db.query(Users).filter(Users.id == id).first()
            if not user:
                return None
            user.username = username
            user.fullname = fullname
            if password:
                user.password = password
            return user
        
    
    def delete_user(self, id):
        with self as db:
            user = db.query(Users).filter(Users.id == id).first()
            if not user:
                return None
            user.is_deleted = 1
            return user
