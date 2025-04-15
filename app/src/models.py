from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID, BYTEA
import uuid

Base = declarative_base()

class Business(Base):
    __tablename__ = "Business"
    id = Column(UUID(as_uuid=True), unique=True, primary_key=True, index=True, default=uuid.uuid4)
    email = Column(String)
    name = Column(String)
    description = Column(String)
    location = Column(String)
    hashed_pass = Column(BYTEA)    
    image = Column(String, default=None)
    salt = Column(BYTEA)
    
class Client(Base):
    __tablename__ = "Client"
    id = Column(UUID(as_uuid=True), unique=True, primary_key=True, index=True, default=uuid.uuid4)
    email = Column(String)
    name = Column(String)
    age = Column(Integer)
    location = Column(String)
    gender = Column(String)
    hashed_pass = Column(BYTEA)
    salt = Column(BYTEA)

class LoyalProgram(Base):
    __tablename__ = "LoyalProgram"
    id = Column(UUID(as_uuid=True), unique=True, primary_key=True, index=True, default=uuid.uuid4)
    business_id = Column(UUID(as_uuid=True))
    name = Column(String)
    goal = Column(Integer)
    reward = Column(String)
    points_per_activation = Column(Integer)
    max_activations = Column(Integer)
    type = Column(String)

class LoyalProgramProgress(Base):
    __tablename__ = "LoyalProgramProgress"
    id = Column(UUID, unique=True, primary_key=True, index=True, default=uuid.uuid4)
    loyal_id = Column(UUID(as_uuid=True))
    client_id = Column(UUID(as_uuid=True))
    reward_count = Column(Integer)
    point_count = Column(Integer)

class LoyalProgramStats(Base):
    __tablename__ = "LoyalProgramStats"
    id = Column(UUID, unique=True, primary_key=True, index=True, default=uuid.uuid4)
    business_id = Column(UUID, unique=True, primary_key=True, index=True)
    total_points = Column(Integer, default=0)
    total_rewarded = Column(Integer, default=0)
    total_clients = Column(Integer, default=0)
    male_count = Column(Integer, default=0)
    female_count = Column(Integer, default=0)
    children = Column(Integer, default=0)
    youngsters = Column(Integer, default=0)
    middle_aged = Column(Integer, default=0)
    old = Column(Integer, default=0)
    very_old = Column(Integer, default=0)