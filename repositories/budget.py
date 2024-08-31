from models.budget import Budget
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
        self.db.close()
        if exc_type:
            self.db.rollback()
        else:
            self.db.commit()

class BudgetRepository(BaseRepository):
    def get_all_budget(self, user_id):
        with self as db:
            budget = db.query(Budget).filter(Budget.userid == user_id).filter(Budget.is_deleted == 0).all()
            if budget is None:
                return None

            budget_list = [
                {
                    "id": budget.id,
                    "userid": budget.userid,
                    "categoryid": budget.categoryid,
                    "amount": budget.amount,
                    "start_date": budget.start_date,
                    "end_date": budget.end_date,
                    "description": budget.description
                } for budget in budget
            ]

            return budget_list
        
    def get_budget_by_id(self, id):
        with self as db:
            budget = db.query(Budget).filter(Budget.id == id).filter(Budget.is_deleted==0).first()
            if budget is None:
                return None
            budget_list = budget.__dict__
            budget_list = {
                key: value for key, value in budget_list.items() if not key.startswith("_")
            }

            return budget_list
        
    def create_budget(self, user_id, category_id, amount, start_date,  end_date, description):
        with self as db:
            budget = Budget(
                id = str(uuid.uuid4()),
                userid = user_id,
                categoryid = category_id,
                amount = amount,
                start_date = start_date,
                end_date = end_date,
                description = description,
                is_deleted = 0,
                created_by = user_id,
                updated_by = user_id

            )
            db.add(budget)
            db.commit()
            db.refresh(budget)
           

            return budget
        
    def update_budget(self, id, user_id, category_id, amount, start_date, end_date, description):
        with self as db:
            budget = db.query(Budget).filter(Budget.id == id).first()

            if not budget:
                return None
            
            if user_id != budget.userid:
                return None
            
            budget.categoryid = category_id
            budget.amount = amount
            budget.start_date = start_date
            budget.end_date = end_date
            budget.description = description
            budget.updated_by = user_id
            db.commit()

            return budget
        
    def delete_budget(self, id, user_id):
         with self as db:
            budget = db.query(Budget).filter(Budget.id == id).first()

            if not budget:
                return None
            
            if user_id != budget.userid:
                return None
            
            budget.is_deleted = 1
            budget.updated_by = user_id
            db.commit()

            return budget
         
