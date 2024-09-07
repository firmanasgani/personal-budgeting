from sqlalchemy import create_engine
import os

hostname = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
username = os.getenv("DB_USER")
password = os.getenv("DB_PASS")
database = os.getenv("DB_NAME")

ENV = os.getenv("NODE_ENV")

print("Connecting to database")
mysql_url = f"mysql+mysqlconnector://{username}:{password}@{hostname}:{port}/{database}"
print(mysql_url)
if ENV == '':
    engine = create_engine(
        mysql_url,
        pool_size=10,
        max_overflow=50,
        pool_timeout=30,
        pool_recycle=1800
    )
else:
    print("This API use Production mode")
    engine = create_engine(mysql_url, pool_size=10, 
    max_overflow=20,        
    pool_timeout=30,      
    pool_recycle=1800 )

engine.execution_options(isolation_level="READ COMMITTED")
connection = engine.connect()
print("Database connected")
