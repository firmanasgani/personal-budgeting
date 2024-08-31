from sqlalchemy import create_engine
import os

hostname = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
username = os.getenv("DB_USER")
password = os.getenv("DB_PASS")
database = os.getenv("DB_NAME")

ENV = os.getenv("NODE_ENV")

print("Connecting to database")
mysql_url = f"mysql+mysqlconnector://{username}:{password}@{hostname}/{database}"
print(mysql_url)
if ENV == '':
    print("This API on development mode")
    engine = create_engine(mysql_url, pool_pre_ping=True,
    echo=True, future=True)
else:
    print("This API use Production mode")
    engine = create_engine(mysql_url)

connection = engine.connect()
print("Database connected")
