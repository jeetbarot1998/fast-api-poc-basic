from sqlalchemy.orm import sessionmaker
import os
from sqlalchemy import create_engine

# AWS RDS MySQL credentials

host = os.getenv('HOST')
port = int(os.getenv('PORT'))
user = os.getenv('USER')
passwd = os.getenv('PASSWD')
database_name = os.getenv('DATABASE_NAME')

# Create SQLAlchemy URL
SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{user}:{passwd}@{host}:{port}/{database_name}"

# Create engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()
def get_db():
    try:
        yield db
    finally:
        db.close()

def get_db_instance():
    return db

from sqlalchemy.orm import declarative_base

Base = declarative_base()




