import argparse
import sys
import bcs

def main(args):
	user_db = bcs.read_db(arguments.user_db)

	if bcs.is_user(user_db, arguments.username):
		sys.exit("User " + arguments.username + " already exists.")

	new_user = bcs.make_user(
		arguments.username, arguments.real_name, arguments.password)
	user_db.append(new_user)
	bcs.save_db(user_db, arguments.user_db)

	print("User created successfully.")

def parse_arguments():
	parser = argparse.ArgumentParser(
		prog='create_user',
		description='Creates a new user in the DB.')
	parser.add_argument('username', help='Username')
	parser.add_argument('password', help='Password')
	parser.add_argument('real_name', help='Real name')
	parser.add_argument('user_db', help='User DB')
	args = parser.parse_args()
	return args

if __name__ == '__main__':
	arguments = parse_arguments()
	main(arguments)

