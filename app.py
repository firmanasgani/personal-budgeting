from flask import Flask
from dotenv import load_dotenv
from utils.connection import connection
from models.users import Users
from sqlalchemy.orm import sessionmaker
from routes.user_route import users_routes
from flask_jwt_extended import JWTManager
import os
from datetime import timedelta
load_dotenv()

app = Flask(__name__)
app.register_blueprint(users_routes)

jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = os.getenv("SECRET")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=int(os.getenv("TOKEN_EXPIRES")))
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(hours=int(os.getenv("REFRESH_TOKEN_EXPIRES")))



@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.user_id

@jwt.user_identity_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    Session = sessionmaker(connection)
    db = Session()
    user = db.query(Users).filter(Users.id == identity).first()
    db.close()
    return user

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