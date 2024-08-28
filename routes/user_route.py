from flask import Blueprint, request
from services.user_services import UserService
from repositories.users import UserRepository
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    current_user,
)

users_routes = Blueprint("users_route", __name__)
repository: UserRepository = UserRepository()
service: UserService = UserService(repository=repository)


@users_routes.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    users = service.get_all_users()
    if users is None:
        return {"message": "Users not found"}, 404
    return {"users": users}, 200

@users_routes.route('/user/<id>', methods=['GET'])
@jwt_required()
def get_users_by_id(id):
    user = service.get_users_by_id(id)
    if user is None:
        return {"message": "User not found"}, 404
    return {"user": user}, 200


@users_routes.route('/user', methods=['POST'])
def create_user():
    username = request.form['username']
    fullname = request.form['fullname']
    password = request.form['password']
    try:
        user = service.create_user(username, fullname, password)

        if user is None:
            return {"message": "User could not be created"}, 400
        return {"user": user}, 201
    except ValueError as e:
        return {"message": str(e)}, 400

@users_routes.route('/user/<id>', methods=['PUT'])
@jwt_required()   
def update_users(id):
    username = request.form['username']
    fullname = request.form['fullname']
    password = request.form['password'] if 'password' in request.form else None
   
    
    try:
        user = service.update_user(id, username, fullname, password)
        if user is None:
            return {"message": "User not found"}, 404
        return {"message": "success update user"}, 200
    except ValueError as e:
        return {"message": str(e)}, 400
    

@users_routes.route('/user/<id>', methods=['DELETE'])
@jwt_required()
def delete_users(id):
    try:
        user = service.delete_user(id)
        if user is None:
            return {"message": "User not found"}, 404
        return {"message": "success delete user"}, 200
    except ValueError as e:
        return {"message": str(e)}, 400
 