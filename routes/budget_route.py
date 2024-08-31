from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from repositories.budget import BudgetRepository
from services.budget_services import BudgetService

budget_routes = Blueprint("budget_route", __name__)
repository: BudgetRepository = BudgetRepository()
service: BudgetService = BudgetService(repository=repository)

@budget_routes.route('/budget', methods=["GET"])
@jwt_required()
def get_budgets():
   user_id = get_jwt_identity()
   budget = service.get_all_budget(user_id)
   if budget is None:
       return {
           "message": "Budget not found"
       }, 404

   return {
       "budget": budget
   }, 200

@budget_routes.route('/budget/<id>', methods=['GET'])
@jwt_required()
def get_budget_by_id(id):
    budget = service.get_budget_by_id(id)
    if budget is None:
        return {
            "message": "Budget not found"
        }, 404

    return {
        "budget": budget
    }, 200

@budget_routes.route('/budget', methods=['POST'])
@jwt_required()
def create_budget():
    user_id = get_jwt_identity()
    category_id = request.form['category_id']
    amount = request.form['amount']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    description = request.form['description']
    budget = service.create_budget(user_id, category_id, amount, start_date, end_date, description)
    if budget is None:
        return {
            "message": "Budget not created"
        }, 404

    return {
        "message": "success create budget", 
    }, 200

@budget_routes.route('/budget/<id>', methods=['PUT'])
@jwt_required()
def update_budget(id):
    user_id = get_jwt_identity()
    category_id = request.form['category_id']
    amount = request.form['amount']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    description = request.form['description']
    budget = service.update_budget(id, user_id, category_id, amount, start_date, end_date, description)
    if budget is None:
        return {
            "message": "Budget not updated"
        }, 404

    return {
        "message": "success update budget"
    }, 200

@budget_routes.route('/budget/<id>', methods=['DELETE'])
@jwt_required()
def delete_budget(id):
    user_id = get_jwt_identity()
    budget = service.delete_budget(id, user_id)
    if budget is None:
        return {
            "message": "Budget not deleted"
        }, 404

    return {
        "message": "Success delete budget"
    }, 200
