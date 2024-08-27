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
    def insert_user(self, username: str, fullname: str, password: str) -> Users:
        """Insert a new user into the database."""
        with self as db:
            check_username = db.query(Users).filter(Users.username == username).first()
            if check_username:
                return None
            user = Users(
                id=str(uuid.uuid4()),
                username=username,
                fullname=fullname,
                is_deleted=0
            )

            user.set_password(password)
            db.add(user)
            db.commit()
            users = {
                "id": user.id,
                "username": user.username,
                "fullname": user.fullname
            }
            return users
            

    def get_users(self):
        with self as db:
            users = db.query(Users).filter(Users.is_deleted==0).all()
            users_list = [
                {
                    "id": user.id,
                    "username": user.username,
                    "fullname": user.fullname
                }
                for user in users
            ]
        
            if not users:
                return None
            return users_list


    def get_user_by_id(self, id):
        with self as db:
            user = db.query(Users).filter(Users.id == id).filter(Users.is_deleted==0).first()
            if not user:
                return None
            
            if user.is_deleted == 1:
                return None
            
            user_list = [
                {
                    "id": user.id,
                    "username": user.username,
                    "fullname": user.fullname
                }
            ]
            return user_list
        
    
    def update_user(self, id, username, fullname, password):
        with self as db:
            user = db.query(Users).filter(Users.id == id).first()
            if not user:
                return None
            user.username = username
            user.fullname = fullname
            if password:
                user.set_password(password)
            return user
        
    
    def delete_user(self, id):
        with self as db:
            user = db.query(Users).filter(Users.id == id).first()
            if not user:
                return None
            user.is_deleted = 1
            return user
