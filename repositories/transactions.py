from models.transaction import Transaction
from models.category import Category
from models.budget import Budget
from utils.connection import connection
from sqlalchemy import desc, asc, func, case, and_
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy.exc import SQLAlchemyError
import uuid

class BaseRepository:
    def __init__(self):
        self.Session = sessionmaker(connection)
        self.db = self.Session()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(exc_type, exc_val, exc_tb)
            self.db.rollback()
            if isinstance(exc_val, SQLAlchemyError):
                print(f"SQLAlchemy Error: {exc_val}")
            
        else:
            self.db.commit()
        self.db.close()
class TransactionRepository(BaseRepository):
    def get_all_transaction(self, user_id, category, start_date, end_date):
        try:
            with self as db:
                transactions = (
                   db.query(Transaction)
                    .options(joinedload(Transaction.category)) 
                    .filter(
                        Transaction.userid == user_id, 
                        Transaction.date_transaction.between(start_date,end_date),
                        Transaction.category.has(type='expenses')
                    )
                    .order_by(asc(Transaction.date_transaction))
                )

                if category:
                    transactions = transactions.filter(Transaction.categoryid == category)

                transactions = transactions.all()


                if not transactions:
                    return None
                transactions_list = [
                    {
                        "id": transaction.id,
                        "userid": transaction.userid,
                        "categoryid": transaction.categoryid,
                        "categoryName": transaction.category.name,
                        "amount": transaction.amount,
                        "date_transaction": transaction.date_transaction,
                        "description": transaction.description
                    }
                    for transaction in transactions
                ]
                return transactions_list
        except SQLAlchemyError as e:
            print(f"SQLAlchemy Error: {e}")
            self.db.rollback()
            return None

        
    def get_transactions_month(self):
        with self as db:
            transactions = db.query(
                Category.name.label('categoryName'),
                func.count(Transaction.amount).label('jumlah_trx'),
                func.sum(Transaction.amount).label('total_amount'),
                func.coalesce(Budget.amount, 0).label('budget_limit'),
               case(
                # Pass conditions as positional arguments
                (func.sum(Transaction.amount) > Budget.amount, 'overbudget'),
                (Budget.amount == None, 'not in budget'),
                else_='budget is okey'
                ).label('status_budget'),
                Budget.description.label('budget_description')
                ).join(Category, Transaction.categoryid == Category.id) \
                .outerjoin(Budget, Budget.categoryid == Category.id) \
                .filter(
                    Category.type == 'expenses',
                    Transaction.date_transaction.between('2024-06-25', '2024-07-24')
                ).group_by(
                    Transaction.categoryid,
                    Category.name,
                    Budget.amount,
                    Budget.description) \
                .order_by(func.count(Transaction.amount).desc())
            
            results = transactions.all()
            results_as_dicts = [
                {
                    'categoryName': row.categoryName,
                    'jumlah_trx': row.jumlah_trx,
                    'total_amount': row.total_amount,
                    'budget_limit': row.budget_limit,
                    'status_budget': row.status_budget,
                    'budget_description': row.budget_description
                }
                for row in results
            ]
            return results_as_dicts
            


    def get_transaction_by_id(self, id):
        with self as db:
            transaction = db.query(Transaction).options(joinedload(Transaction.category)).filter(Transaction.id == id).first()
            
            if transaction is None:
                return None
            transaction_dict = {
                'id': transaction.id,
                'userid': transaction.userid,
                'categoryid': transaction.categoryid,
                'categoryName': transaction.category.name,
                'amount': transaction.amount,
                'description': transaction.description,
                'date_transaction': transaction.date_transaction
            }
            return transaction_dict

        
    def create_transactions(self, user_id, category_id, amount, description, date_transaction):
        with self as db:
            transaction = Transaction(
                id = str(uuid.uuid4()),
                userid = user_id,
                categoryid = category_id,
                amount = amount,
                description = description,
                date_transaction = date_transaction,
                created_by = user_id,
                updated_by = user_id
            )
            db.add(transaction)
            db.commit()
            return transaction
        
    def update_transaction(self, id, user_id, category_id, amount, description, date_transaction):
        with self as db:
            transaction = db.query(Transaction).filter(Transaction.id == id).first()
            if not transaction:
                return None
            if user_id != transaction.userid:
                return None
            transaction.categoryid = category_id
            transaction.amount = amount
            transaction.description = description
            transaction.date_transaction = date_transaction
            transaction.updated_by = user_id
            db.commit()
            return transaction
        
    def delete_transaction(self, id, user_id):
        with self as db:
            transaction = db.query(Transaction).filter(Transaction.id == id).first()
            if not transaction:
                return None
            if user_id != transaction.userid:
                return None
            db.delete(transaction)
            db.commit()
            return transaction
        