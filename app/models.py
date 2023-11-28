from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class UserTable(Base):
    __tablename__ = "user_table"

    id = Column(Integer, primary_key=True, index=True)
    # phone_number = Column(Integer, unique= True, index=True, nullable=True )
    username = Column(String(50), index=True, nullable=True)
    email = Column(String(50), unique= True, index=True, nullable=True)
    password = Column(String(255), nullable=False)
    emergency_contact1 = Column(Integer, nullable=True)
    emergency_contact2 = Column(Integer, nullable=True)
    emergency_contact3 = Column(Integer, nullable=True)
    # verified = Column(Boolean, nullable=True)
    map = relationship("UserLocation", back_populates="location")


class UserLocation(Base):
    __tablename__ = "user_location"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(100), nullable=False)

    longitude = Column(DECIMAL(10, 8))  # Adjust precision and scale as needed
    latitude = Column(DECIMAL(10, 8))  # Adjust precision and scale as needed
    map_id = Column(Integer, ForeignKey('user_table.id'))  # Define the foreign key
    expiration_time = Column(DateTime)  # Modify as needed
    location = relationship("UserTable", back_populates="map")

# ========== CREATE TABLES START ==========
# def create_tables():
#     Base.metadata.create_all(bind=engine)
# create_tables()
# ========== CREATE TABLES END ==========