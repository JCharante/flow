from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from db_setup import UserV1, Base, GroupV1, GroupMemberV1
import util
import config
import uuid
from typing import Tuple, List, Dict
from datetime import datetime
import exceptions

# Connects to the database
engine = create_engine(config.path_to_db)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)


def create_user(username: str, password: str) -> str:
	session = DBSession()
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
	session.close()
	return aid


def login(username: str, password: str) -> Tuple[bool, str]:
	session = DBSession()
	stored_user = session.query(UserV1).filter(UserV1.username == username).first()
	session.close()
	if stored_user is None:
		raise exceptions.InvalidCredentials
	stored_password = stored_user.hashed_password
	if util.checkpw(stored_password, password):
		update_last_login(stored_user.aid)
		return stored_user.aid
	else:
		raise exceptions.InvalidCredentials()


def valid_aid(aid: str) -> bool:
	session = DBSession()
	stored_user = session.query(UserV1).filter(UserV1.aid == aid).first()
	session.close()
	return stored_user is not None


def get_username(aid: str) -> str:
	session = DBSession()
	row = session.query(UserV1).filter(UserV1.aid == aid).first()
	session.close()
	if row is not None:
		return row.username
	else:
		raise exceptions.InvalidAid()


def update_last_login(aid: str) -> None:
	session = DBSession()
	user = session.query(UserV1).filter(UserV1.aid == aid).first()
	if user is not None:
		user.last_login = datetime.now()
		session.commit()
	session.close()


def get_last_login(aid: str) -> str:
	session = DBSession()
	row = session.query(UserV1).filter(UserV1.aid == aid).first()
	session.close()
	if row is not None:
		row = row  # type: UserV1
		return row.last_login
	else:
		raise exceptions.InvalidAid()


def number_of_users():
	session = DBSession()
	x = session.query(UserV1).count()
	session.close()
	return x


def wipe_users():
	session = DBSession()
	session.query(UserV1).filter(True).delete()
	session.commit()
	session.close()


def create_group(owner_aid: str, group_name: str):
	session = DBSession()
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
	session.add(GroupMemberV1(
		group_id=group_id,
		member_aid=owner_aid
	))
	session.commit()
	session.close()
	return group_id


def generate_unique_group_invite_code():
	invite_code = util.generate_alphanumeric_string(6)
	while invite_code_is_unique(invite_code) is False:
		invite_code = util.generate_alphanumeric_string(6)
	return invite_code


def invite_code_is_unique(invite_code: str):
	session = DBSession()
	row = session.query(GroupV1).filter(GroupV1.invite_code == invite_code).first()
	session.close()
	return row is None


def get_invite_code(group_id: str):
	session = DBSession()
	group = session.query(GroupV1).filter(GroupV1.group_id == group_id).first()
	session.close()
	if group is None:
		raise exceptions.InvalidGroupId()
	return group.invite_code


def join_group_invite_code(aid: str, invite_code: str):
	session = DBSession()
	if valid_aid(aid) is False:
		session.close()
		raise exceptions.InvalidAid()
	group = session.query(GroupV1).filter(GroupV1.invite_code == invite_code).first()
	session.close()
	if is_group_member(aid, group.group_id):
		raise exceptions.AlreadyAGroupMember()
	if group is None:
		raise exceptions.InvalidGroupInviteCode()
	group = group  # type: GroupV1
	join_group(aid, group.group_id)


def join_group(aid: str, group_id):
	if valid_aid(aid) is False:
		raise exceptions.InvalidAid()
	if is_valid_group_id(group_id) is False:
		raise exceptions.InvalidGroupId()
	session = DBSession()
	session.add(GroupMemberV1(
		group_id=group_id,
		member_aid=aid
	))
	session.commit()
	session.close()


def leave_group(aid: str, group_id: str):
	if valid_aid(aid) is False:
		raise exceptions.InvalidAid()
	if is_valid_group_id(group_id) is False:
		raise exceptions.InvalidGroupId()
	session = DBSession()
	membership = session.query(GroupMemberV1).filter(GroupMemberV1.group_id == group_id).filter(GroupMemberV1.member_aid == aid).first()
	if membership is None:
		session.close()
		raise exceptions.AlreadyNotAGroupMember()
	session.query(GroupMemberV1).filter(GroupMemberV1.group_id == group_id).filter(GroupMemberV1.member_aid == aid).delete()
	session.commit()
	session.close()


def remove_user_from_groups(aid: str):
	if valid_aid(aid) is False:
		raise exceptions.InvalidAid()
	session = DBSession()
	session.query(GroupMemberV1).filter(GroupMemberV1.member_aid == aid).delete()
	session.commit()
	session.close()


def delete_user(aid: str):
	if valid_aid(aid) is False:
		raise exceptions.InvalidAid()
	session = DBSession()
	remove_user_from_groups(aid)
	session.query(UserV1).filter(UserV1.aid == aid).delete()
	session.commit()
	session.close()


def is_valid_group_id(group_id: str):
	session = DBSession()
	group = session.query(GroupV1).filter(GroupV1.group_id == group_id).first()
	session.close()
	return group is not None


def groups_user_is_in(aid: str) -> List[Dict]:
	if valid_aid(aid) is False:
		raise exceptions.InvalidAid()
	session = DBSession()
	groups = []
	for group_member in session.query(GroupMemberV1).filter(GroupMemberV1.member_aid == aid).all():
		group = session.query(GroupV1).filter(GroupV1.group_id == group_member.group_id).first()
		if group is not None:
			group = group  # type: GroupV1
			try:
				group_owner_username = get_username(group.owner_aid)
			except exceptions.InvalidAid:
				session.close()
				group_owner_username = 'Error Fetching Owner'
			groups.append({
				'name': group.name,
				'group_id': group.group_id,
				'owner': group_owner_username
			})
	session.close()
	return groups


def is_group_member(aid: str, group_id: str):
	if valid_aid(aid) is False:
		raise exceptions.InvalidAid()
	if is_valid_group_id(group_id) is False:
		raise exceptions.InvalidGroupId()
	session = DBSession()
	membership = session.query(GroupMemberV1).filter(GroupMemberV1.member_aid == aid).filter(GroupMemberV1.group_id == group_id).first()
	session.close()
	return membership is not None


def get_group_details(aid: str, group_id: str):
	if valid_aid(aid) is False:
		raise exceptions.InvalidAid()
	if is_valid_group_id(group_id) is False:
		raise exceptions.InvalidGroupId()
	if is_group_member(aid, group_id) is False:
		raise exceptions.NotAGroupMember()

	session = DBSession()
	group = session.query(GroupV1).filter(GroupV1.group_id == group_id).first()
	session.close()
	if group is None:
		raise exceptions.GroupDoesNotExist()

	try:
		group_owner_username = get_username(group.owner_aid)
	except exceptions.InvalidAid:
		group_owner_username = 'Error Fetching Owner'

	return {
		'name': group.name,
		'owner': group_owner_username,
		'group_id': group.group_id,
		'invite_code': group.invite_code
	}
