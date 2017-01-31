from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import UserV1, Base
import util
import config
import uuid
from typing import Tuple
from datetime import datetime
import exceptions

# Connects to the database
engine = create_engine(config.path_to_db)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def create_user(username: str, password: str) -> str:
	if util.secure_password(password) is False:
		raise exceptions.InsecurePasswordException()
	if session.query(UserV1).filter(UserV1.username == username).first() is not None:
		raise exceptions.UsernameNotUniqueException()
	aid = str(uuid.uuid4())
	hashed_password = util.encrypt_new_password(password)
	session.add(UserV1(aid=aid,
					   username=username,
					   hashed_password=hashed_password,
					   last_login=datetime.now()
					   ))
	session.commit()
	return aid


def login(username: str, password: str) -> Tuple[bool, str]:
	stored_user = session.query(UserV1).filter(UserV1.username == username).first()
	if stored_user is None:
		return False, "username doesn't exist"
	stored_password = stored_user.hashed_password
	if util.encrypt_password(stored_password, password) == stored_password:
		update_last_login(stored_user.aid)
		return True, stored_user.aid
	else:
		return False, "wrong password"


def valid_aid(aid: str) -> bool:
	stored_user = session.query(UserV1).filter(UserV1.aid == aid).first()
	return stored_user is not None


def get_username(aid: str) -> str:
	row = session.query(UserV1).filter(UserV1.aid == aid).first()
	if row is not None:
		return row.username
	else:
		raise exceptions.InvalidAid()


def update_last_login(aid: str) -> None:
	user = session.query(UserV1).filter(UserV1.aid == aid).first()
	if user is not None:
		user.last_login = datetime.now()
		session.commit()


def get_last_login(aid: str) -> str:
	row = session.query(UserV1).filter(UserV1.aid == aid).first()
	if row is not None:
		row = row  # type: UserV1
		return row.last_login
	else:
		raise exceptions.InvalidAid()
