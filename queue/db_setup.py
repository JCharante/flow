from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import config

Base = declarative_base()

# The naming convention for {table_name}V{table_version} will be used once we finish the mvp. Until then they will stay
# at V1 and you will have to continue to drop the tables.


class UserV1(Base):
	__tablename__ = 'UserV1'
	pk = Column(Integer, primary_key=True)
	aid = Column(String(36))
	username = Column(String(100))
	hashed_password = Column(String(60))
	last_login = Column(DateTime)


class GroupV1(Base):
	__tablename__ = 'GroupV1'
	pk = Column(Integer, primary_key=True)
	group_id = Column(String(36))
	name = Column(String(100))
	owner_aid = Column(String(36))
	invite_code = Column(String(6))


class GroupMemberV1(Base):
	__tablename__ = 'GroupMemberV1'
	pk = Column(Integer, primary_key=True)
	group_id = Column(String(36))
	member_aid = Column(String(36))

engine = create_engine(config.path_to_db)
Base.metadata.create_all(engine)
