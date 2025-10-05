import argparse
import sys
import bcs

def main(args):
	srv_db = bcs.read_db(arguments.srv_db)
	user_db = bcs.read_db(arguments.user_db)

	srv = bcs.get_server(srv_db, arguments.srv_name)
	if srv is None:
		sys.exit("Server " + arguments.srv_name + " not found.")

	match arguments.type:
		case "awg":
			wg0conf = bcs.generate_wg0_conf(
				user_db, srv['srv_name'], srv['awg_params'])
			bcs.write_file(wg0conf, "wg0.conf", arguments.out_folder)
		case "xray":
			serverjson = bcs.generate_server_json(
				user_db, srv['srv_name'], srv["xray_params"])
			bcs.write_file(serverjson, "server.json", arguments.out_folder)

	clientsTable = bcs.generate_clientsTable(
		user_db, srv['srv_name'], arguments.type)
	bcs.write_file(clientsTable, "clientsTable", arguments.out_folder)

	print("Configs generated successfully.")

def parse_arguments():
	parser = argparse.ArgumentParser(
		prog='generate_srv_conf',
		description='Reads json user and server DBs and generates\
			configuration files for the server.')
	parser.add_argument('srv_name', help='Server name')
	parser.add_argument('type', help='Config type', choices=['awg', 'xray'])
	parser.add_argument('user_db', help='User DB')
	parser.add_argument('srv_db', help='Server DB')
	parser.add_argument('out_folder', help='Folder for output path')
	args = parser.parse_args()
	return args

if __name__ == '__main__':
	arguments = parse_arguments()
	main(arguments)
