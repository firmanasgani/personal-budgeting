from flask import Flask
from dotenv import load_dotenv
from utils.connection import connection
from sqlalchemy.orm import sessionmaker
from models.users import Users
from flask_jwt_extended import JWTManager
import os
from datetime import timedelta
from flask_cors import CORS

from routes.user_route import users_routes
from routes.auth_route import auth_routes
from routes.category_route import categories_routes
from routes.budget_route import budget_routes
from routes.transaction_route import transaction_routes

load_dotenv()

app = Flask(__name__)
app.register_blueprint(users_routes)
app.register_blueprint(auth_routes)
app.register_blueprint(categories_routes)
app.register_blueprint(budget_routes)
app.register_blueprint(transaction_routes)
CORS(app, resources={r"/*": {"origins": "*"}})
jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = os.getenv("SECRET")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=int(os.getenv("TOKEN_EXPIRES")))
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(hours=int(os.getenv("REFRESH_TOKEN_EXPIRES")))



# @jwt.user_identity_loader
# def user_identity_lookup(users):
#     return users

# @jwt.user_identity_loader
# def user_lookup_callback(_jwt_header, jwt_data):
#     identity = jwt_data["sub"]
#     print(identity)
#     Session = sessionmaker(connection)
#     db = Session()
#     user = db.query(Users).filter(Users.id == identity).first()
#     db.close()
    #return user

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
    return ({"message": "Token has expired", "error": "token_expired"}), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        ({"message": "Signature verification failed", "error": "invalid_token"}),
        401,
    )


@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        (
            {
                "message": "Request doesnt contain valid token",
                "error": "authorization_header",
            }
        ),
        401,
    )

@app.route('/')
def hello_world():
    
    return 'Hello, World!'



@app.errorhandler(404)
def page_not_found(e):
     return {
         'message': 'Page not found',
     }, 404

if __name__ == "__main__":
    app.run(debug=True)