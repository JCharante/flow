from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import UserV1, Base, GroupV1, GroupMemberV1
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
	if util.checkpw(stored_password, password):
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


def number_of_users():
	return session.query(UserV1).count()


def wipe_users():
	session.query(UserV1).filter(True).delete()
	session.commit()


def create_group(owner_aid: str, group_name: str):
	if valid_aid(owner_aid) is False:
		raise exceptions.InvalidAid()
	group_id = str(uuid.uuid4())
	invite_code = generate_unique_group_invite_code()
	session.add(GroupV1(
		group_id=group_id,
		owner_aid=owner_aid,
		name=group_name,
		invite_code=invite_code
	))
	session.commit()
	session.add(GroupMemberV1(
		group_id=group_id,
		member_aid=owner_aid
	))
	session.commit()
	return group_id


def generate_unique_group_invite_code():
	invite_code = util.generate_alphanumeric_string(6)
	while invite_code_is_unique(invite_code) is False:
		invite_code = util.generate_alphanumeric_string(6)
	return invite_code


def invite_code_is_unique(invite_code: str):
	row = session.query(GroupV1).filter(GroupV1.invite_code == invite_code).first()
	return row is None


def get_invite_code(group_id: str):
	group = session.query(GroupV1).filter(GroupV1.group_id == group_id).first()
	if group is None:
		raise exceptions.InvalidGroupId()
	return group.invite_code


def join_group_through_invite_link(aid: str, invite_code: str):
	group = session.query(GroupV1).filter(GroupV1.invite_code == invite_code).first()
	if group is None:
		raise exceptions.InvalidGroupInviteCode()
	group = group  # type: GroupV1
	join_group(aid, group.group_id)


def join_group(aid: str, group_id):
	if valid_aid(aid) is False:
		raise exceptions.InvalidAid()
	if is_valid_group_id(group_id) is False:
		raise exceptions.InvalidGroupId()
	session.add(GroupMemberV1(
		group_id=group_id,
		member_aid=aid
	))
	session.commit()


def is_valid_group_id(group_id: str):
	group = session.query(GroupV1).filter(GroupV1.group_id == group_id).first()
	return group is not None