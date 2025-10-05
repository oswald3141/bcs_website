import argparse
import sys
import bcs

def main(args):
	user_db = bcs.read_db(arguments.user_db)

	if not bcs.is_user(user_db, arguments.username):
		sys.exit("User " + arguments.username + " not found.")

	user_db[:] = [user for user in user_db
		if user['username'] != arguments.username]

	bcs.save_db(user_db, arguments.user_db)

	print("User deleted successfully.")

def parse_arguments():
	parser = argparse.ArgumentParser(
		prog='delete_user',
		description='Deletes a new user from the DB.')
	parser.add_argument('username', help='Username')
	parser.add_argument('user_db', help='User DB')
	args = parser.parse_args()
	return args

if __name__ == '__main__':
	arguments = parse_arguments()
	main(arguments)
