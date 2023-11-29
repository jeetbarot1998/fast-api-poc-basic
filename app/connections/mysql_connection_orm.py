from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.load_environment import host, port, user, passwd, database_name

# Create SQLAlchemy URL
SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{user}:{passwd}@{host}:{port}/{database_name}"
print('==============================='+SQLALCHEMY_DATABASE_URL)

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




