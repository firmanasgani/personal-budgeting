from models.transaction import Transaction
from utils.connection import connection
from sqlalchemy import desc, asc
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

class TransactionRepository(BaseRepository):
    def get_all_transaction(self, user_id):
        with self as db:
            transactions = db.query(Transaction).filter(Transaction.userid == user_id).order_by(desc(Transaction.date_transaction)).all()
            if transactions is None:
                return None
            transactions_list = [
                 {
                     "id": transaction.id,
                     "userid": transaction.userid,
                     "categoryid": transaction.categoryid,
                     "amount": transaction.amount,
                     "date_created": transaction.date_created,
                     "description": transaction.description,
                     "date_created": transaction.date_created
                 } for transaction in transactions
             ]

            return transactions_list
        
    def get_transaction_by_id(self, id):
        with self as db:
            transaction = db.query(Transaction).filter(Transaction.id == id).first()
            if transaction is None:
                return None
            transaction_list = transaction.__dict__
            transaction_list = {
                key: value for key, value in transaction_list.items() if not key.startswith("_")
            }

            return transaction_list
        
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
            db.delete()
            return transaction
        