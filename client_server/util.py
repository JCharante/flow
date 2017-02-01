import os
import subprocess


def path_to_this_files_directory():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	return dir_path + '/'


def get_git_revision_hash(return_bytes=False):
	if return_bytes:
		return subprocess.check_output(['git', 'rev-parse', 'HEAD'])
	else:
		return str(subprocess.check_output(['git', 'rev-parse', 'HEAD']), 'utf-8')


def get_git_revision_short_hash(return_bytes=False):
	if return_bytes:
		return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])
	else:
		return str(subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']), 'utf-8')
