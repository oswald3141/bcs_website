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
		bcs.grant_access(
			user_db, username, arguments.srv_name, arguments.n, arguments.type)

	bcs.save_db(user_db, arguments.user_db)

	print("Access granted.")

def parse_arguments():
	parser = argparse.ArgumentParser(
		prog='grant_access',
		description='Grants user access to a server.\
			If the user already has access, gives it more keys.')
	parser.add_argument('username', help='Username')
	parser.add_argument('srv_name', help='Server name')
	parser.add_argument('type', help='Container type', choices=['awg', 'xray'])
	parser.add_argument('n', help='Number of keys to grant', type=int)
	parser.add_argument('user_db', help='User DB')
	args = parser.parse_args()
	return args

if __name__ == '__main__':
	arguments = parse_arguments()
	main(arguments)
