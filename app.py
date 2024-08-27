from flask import Flask
from dotenv import load_dotenv
from utils.connection import connection
from routes.user_route import users_routes

app = Flask(__name__)
app.register_blueprint(users_routes)
load_dotenv()
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