import argparse
import sys
import bcs

def main(args):
	user_db = bcs.read_db(arguments.user_db)

	if arguments.username == '*':
		usernames = [user['username'] for user in user_db]
	else:
		usernames = [arguments.username]

	for username in usernames:
		bcs.revoke_access(
			user_db, username, arguments.srv_name, arguments.type)

	bcs.save_db(user_db, arguments.user_db)

	print("Access revoked.")

def parse_arguments():
	parser = argparse.ArgumentParser(
		prog='revoke_access',
		description='Revokes user access to a server.')
	parser.add_argument('username', help='Username')
	parser.add_argument('srv_name', help='Server name')
	parser.add_argument('type', help='Container type', choices=['awg', 'xray'])
	parser.add_argument('user_db', help='User DB')
	args = parser.parse_args()
	return args

if __name__ == '__main__':
	arguments = parse_arguments()
	main(arguments)
