from sqlalchemy import create_engine
import os

mysql_host = os.getenv("mysql_host")

print("Connecting to database")
engine = create_engine(mysql_host)
connection = engine.connect()
print("Database connected")
