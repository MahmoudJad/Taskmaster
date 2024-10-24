from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import constant

# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:admin@12345@localhost/Todo'


DATABASE_URL = (
    "postgresql://"
    + constant.POSTGRES_USER
    + ":"
    + constant.POSTGRES_PASSWORD
    + "@"
    + constant.POSTGRES_SERVER
    + "/"
    + constant.POSTGRES_DB
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
