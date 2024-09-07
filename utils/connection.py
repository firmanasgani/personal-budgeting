from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import os

hostname = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
username = os.getenv("DB_USER")
password = os.getenv("DB_PASS")
database = os.getenv("DB_NAME")

ENV = os.getenv("NODE_ENV")

print("Connecting to database")
mysql_url = f"mysql+mysqlconnector://{username}:{password}@{hostname}:{port}/{database}"
# print(mysql_url)

try:
    if ENV == '':
        engine = create_engine(
            mysql_url,
            pool_size=100, 
            max_overflow=50,        
            pool_timeout=100,      
            pool_recycle=1800,
            pool_pre_ping=True,
            echo=True,
        )
    else:
        print("This API uses Production mode")
        engine = create_engine(
            mysql_url,
            max_overflow=40,        
            pool_timeout=10,      
            pool_recycle=180,
            pool_pre_ping=True,pool_use_lifo=True,
        )

    connection = engine.execution_options(isolation_level="READ COMMITTED")
   
    

except SQLAlchemyError as e:
    print(f"An error occurred while connecting to the database: {e}")
