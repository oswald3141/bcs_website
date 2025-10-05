import argparse
import sys
import bcs

def main(args):
	srv_db = bcs.read_db(arguments.srv_db)

	if bcs.is_server(srv_db, arguments.srv_name):
		sys.exit("Server " + arguments.srv_name + " already exists.")

	new_server = bcs.make_empty_server(
		arguments.srv_name, arguments.awg, arguments.xray)
	srv_db.append(new_server)
	bcs.save_db(srv_db, arguments.srv_db)

	print("Server created successfully.")

def parse_arguments():
	parser = argparse.ArgumentParser(
		prog='create_empty_server',
		description='Creates a new empty server in the DB.')
	parser.add_argument('srv_name', help='Server name')
	parser.add_argument('srv_db', help='Server DB')
	parser.add_argument('--awg', help='Add AWG container template',
		action='store_true')
	parser.add_argument('--xray', help='Add Xray container template',
		action='store_true')
	args = parser.parse_args()
	return args

if __name__ == '__main__':
	arguments = parse_arguments()
	main(arguments)

