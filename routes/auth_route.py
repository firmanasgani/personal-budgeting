from flask import Blueprint, request
from services.auth_services import AuthService
from repositories.auth import AuthRepository
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
)

auth_routes = Blueprint("auth_route", __name__)
repository: AuthRepository = AuthRepository()
service: AuthService = AuthService(repository=repository)

@auth_routes.route('/login', methods=['POST'])
def login():
    try:
        username = request.form['username']
        password = request.form['password']
        users = service.login(username, password)
        if users is None:
            return {"message": "Invalid username or password"}, 400
        print(users["id"])
        access_token = create_access_token(identity=users["id"], additional_claims={
            "username": users['username'],
            "fullname": users['fullname']
        })

        refresh_token = create_refresh_token(identity=users["id"])
        return {
            "users": users,
            "access_token": access_token,
            "refresh_token": refresh_token
        }, 200
    except KeyError:
        return {"message": "Invalid username or password"}, 400
  
 