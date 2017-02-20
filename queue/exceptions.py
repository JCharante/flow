class InvalidAid(Exception):
	pass


class InsecurePasswordException(Exception):
	pass


class UsernameNotUniqueException(Exception):
	pass


class InvalidGroupId(Exception):
	pass


class InvalidGroupInviteCode(Exception):
	pass


class InvalidCredentials(Exception):
	pass


class AlreadyNotAGroupMember(Exception):
	pass


class NotAGroupMember(Exception):
	pass


class GroupDoesNotExist(Exception):
	pass


class AlreadyAGroupMember(Exception):
	pass
