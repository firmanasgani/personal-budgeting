from flask import Blueprint, request
from services.category_services import CategoryService
from repositories.category import CategoryRepository
from flask_jwt_extended import jwt_required, get_jwt_identity

categories_routes = Blueprint("categories_route", __name__)

repository: CategoryRepository = CategoryRepository() 
service: CategoryService = CategoryService(repository=repository)

@categories_routes.route('/category', methods=['POST'])
@jwt_required()
def create_category():
    name = request.form['name']
    code = request.form['code']
    type = request.form['type']
    user = get_jwt_identity()

    try:
        category = service.create_category(name, code, type, user)

        if category is None:
            return {"message": "Category could not be created"}, 400
        return {"category": category}, 201
    except ValueError as e:
        return {"message": str(e)}, 400

@categories_routes.route('/category', methods=['GET'])
@jwt_required()
def get_all_categories():
    type = request.args.get('type', '', type=str)
    user = get_jwt_identity()
    categories = service.get_all_categories(type, user)

    if categories is None:
        return {"message": "Categories not found"}, 404

    return {"categories": categories}, 200

@categories_routes.route('/category/<id>', methods=['GET'])
@jwt_required()
def get_category_by_id(id):
    category = service.get_category_by_id(id)

    if category is None:
        return {"message": "Category not found"}, 404

    return {"category": category}, 200

@categories_routes.route('/category/<id>', methods=['PUT'])
@jwt_required()
def update_category(id):
    name = request.form['name']
    code = request.form['code']
    type = request.form['type']
    user = get_jwt_identity()

    try:
        category = service.update_category(id, name, code, type, user)

        if category is None:
            return {"message": "Category not found"}, 404
        return {"category": category}, 200
    except ValueError as e:
        return {"message": str(e)}, 400

@categories_routes.route('/category/<id>', methods=['DELETE'])
@jwt_required()
def delete_category(id):
    return service.delete_category(id)
