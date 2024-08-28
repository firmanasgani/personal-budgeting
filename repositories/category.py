from models.category import Category
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

class CategoryRepository(BaseRepository):
    def get_all_categories(self):
        with self as db:
            categories =  db.query(Category).filter(Category.is_deleted==0).all()

            categories_list = [
                {
                    "id": category.id,
                    "name": category.name,
                    "code": category.code,
                    "type": category.type
                } for category in categories
            ]

            if not categories:
                return None
            return categories_list
        
    def get_category_by_id(self, id):
        with self as db:
            category = db.query(Category).filter(Category.id == id).first()

            if not category:
                return None
            if category.is_deleted == 1:
                return None

            categories_list = [
                {
                    "id": category.id,
                    "name": category.name,
                    "code": category.code,
                    "type": category.type
                }
            ]

            return categories_list
        
    def create_category(self, name, code, type, user):
        with self as db:
            code_category = db.query(Category).filter(Category.code == code).first()
            if code_category:
                return None
            
            category = Category(
                id = str(uuid.uuid4()),
                name = name,
                code = code,
                type = type,
                is_deleted = 0,
                created_by = user,
                updated_by = user
            )
            db.add(category)
            db.commit()
            db.refresh(category)
            category_dict= category.__dict__
            category_dict = {
                    key: value for key, value in category_dict.items() if not key.startswith("_")
            }

            return category_dict
        
    def update_category(self, id, name, code, type, user):
        with self as db:
            category = db.query(Category).filter(Category.id == id).first()

            if not category:
                return None

            category.name = name
            category.code = code
            category.type = type
            category.updated_by = user

            db.commit()

          
            return category
        
    def delete_category(self, id):
        with self as db:
            category = db.query(Category).filter(Category.id == id).first()

            if not category:
                return None
            category.is_deleted = 1
            return category