from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import config

Base = declarative_base()


class UserV1(Base):
	__tablename__ = 'UserV1'
	pk = Column(Integer, primary_key=True)
	aid = Column(String())
	username = Column(String())
	hashed_password = Column(String())
	last_login = Column(DateTime)

engine = create_engine(config.path_to_db)
Base.metadata.create_all(engine)
