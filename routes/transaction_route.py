from flask import Blueprint,request
from services.transaction_services import TransactionService
from repositories.transactions import TransactionRepository
from flask_jwt_extended import jwt_required, get_jwt_identity

transaction_routes = Blueprint("transaction_route", __name__)
repository: TransactionRepository = TransactionRepository()
service: TransactionService = TransactionService(repository=repository)

@transaction_routes.route('/transaction', methods=['POST'])
@jwt_required()
def create_transaction():
    user_id = get_jwt_identity()
    category_id = request.form['category_id']
    amount = request.form['amount']
    description = request.form['description']
    date_transaction = request.form['date_transaction']
    transaction = service.create_transaction(user_id, category_id, amount, description, date_transaction)
    if transaction is None:
        return {"message": "Transaction not created"}, 400
    return {"message": "Success create transaction"}, 200

@transaction_routes.route('/transactions', methods=["GET"])
@jwt_required()
def get_transactions():
    user_id = get_jwt_identity()
    category = request.args.get('category', '', type=str)
    start_date = request.args.get('start_date', '', type=str)
    end_date = request.args.get('end_date', '', type=str)
    transactions = service.get_all_transaction(user_id, category, start_date, end_date)
    if transactions is None:
        return {"message": "Transactions not found"}, 404
    return {"transactions": transactions}, 200

@transaction_routes.route('/transaction_month')
def get_transaction_month():
    transactions = service.get_transactions_month()
    if transactions is None:
        return {"message": "Transactions not found"}, 404
    return {"transactions": transactions}, 200

@transaction_routes.route('/transaction/<id>', methods=["GET"])
@jwt_required()
def get_transaction_by_id(id):
    user_id = get_jwt_identity()
    transaction = service.get_transaction_by_id(id)
    if transaction is None:
        return {"message": "Transaction not found"}, 404
    return {"transaction": transaction}, 200

@transaction_routes.route('/transaction/<id>', methods=["DELETE"])
@jwt_required()
def delete_transaction(id):
    user_id = get_jwt_identity()
    transaction = service.delete_transaction(id, user_id)
    if transaction is None:
        return {"message": "Transaction not deleted"}, 404
    return {"message": "Success delete transaction"}, 200

@transaction_routes.route('/transaction/<id>', methods=["PUT"])
@jwt_required()
def update_transaction(id):
    user_id = get_jwt_identity()
    category_id = request.form['category_id']
    amount = request.form['amount']
    description = request.form['description']
    date_transaction = request.form['date_transaction']
    transaction = service.update_transaction(id, user_id, category_id, amount, description, date_transaction)
    if transaction is None:
        return {"message": "Transaction not updated"}, 404
    return {"message": "Success update transaction"}, 200
