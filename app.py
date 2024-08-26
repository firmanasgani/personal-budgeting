from flask import Flask
from dotenv import load_dotenv
from utils.connection import connection

app = Flask(__name__)
load_dotenv()
@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == "__main__":
    app.run(debug=True)