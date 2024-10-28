from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import constant

SQLALCHEMY_DATABASE_URL = 'postgresql://taskmaster_db_owner:RwWlB9bscgX0@ep-proud-hall-a55sfpxz.us-east-2.aws.neon.tech/taskmaster_db?sslmode=require'


# DATABASE_URL = (
#     "postgresql://"
#     + constant.POSTGRES_USER
#     + ":"
#     + constant.POSTGRES_PASSWORD
#     + "@"
#     + constant.POSTGRES_SERVER
#     + "/"
#     + constant.POSTGRES_DB
# )

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
