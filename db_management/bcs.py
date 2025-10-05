import json
import os
import sys
import copy
import bcrypt
import uuid
import base64
from datetime import datetime
from ipaddress import IPv4Network
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import x25519

def write_file(str, fname, folder=""):
	dest = os.path.join(folder, fname)
	with open(dest, 'w', newline='') as file:
		file.write(str)

def read_db(json_file):
	with open(json_file) as f:
		db = json.load(f)
	return db

def save_db(db, json_file, folder=""):
	string = json.dumps(db, indent=4, ensure_ascii=False) + "\n"
	write_file(string, json_file, folder)

def _hash_password(password):
	return bcrypt.hashpw(
			password.encode(),
			bcrypt.gensalt(rounds=10, prefix=b"2a")
		).decode().replace('$2a$', '$2y$')

def is_user(user_db, username):
	return username in [user["username"] for user in user_db]

def get_user(user_db, name):
	return next((item for item in user_db 
		if item["username"] == name), None)

def make_user(username, real_name, password):
	return {
		"username": username,
		"real_name": real_name,
		"password_hash": _hash_password(password),
		"creation_date": datetime.today().strftime("%c"),
		"awg_key_data": [],
		"xray_key_data": []
	}

def is_server(srv_db, srv_name):
	return srv_name in [server["srv_name"] for server in srv_db]

def get_server(srv_db, name):
	return next((item for item in srv_db 
		if item["srv_name"] == name), None)

def __get_key_data(user, srv_name, type):
	return next((item["key_data"] for item in user[type+"_key_data"]
		if item["srv_name"] == srv_name), None)

# AWG
def _extract_awg_peers(user_db, srv_name):
	peers = []

	for user in user_db:
		key_data = __get_key_data(user, srv_name, "awg")
		if key_data is None:
			continue
		key_data = copy.deepcopy(key_data)

		# Sort by the last octet of IP
		key_data = sorted(key_data,
			key=lambda d: int(d['IP'].split('.')[3]))

		for idx, key in enumerate(key_data):
			key["name"] = f"{user['username']}_{idx+1}"
			key["creation_date"] = user['creation_date']
		peers.extend(key_data)

	return peers

def _extract_xray_clients(user_db, srv_name):
	clients = []

	for user in user_db:
		key_data = __get_key_data(user, srv_name, "xray")
		if key_data is None:
			continue

		clients.append({
			'name': user['username'],
			'creation_date': user['creation_date'],
			'id': key_data[0]['id']})

	return clients

def generate_wg0_conf(user_db, srv_name, awg_params):
	# Interface section
	wg0conf = (
		"[Interface]\n"
		f"PrivateKey = {awg_params['priv_key']}\n"
		"Address = 10.8.1.0/24\n"
		f"ListenPort = {awg_params['port']}\n"
		f"Jc = {awg_params['Jc']}\n"
		f"Jmin = {awg_params['Jmin']}\n"
		f"Jmax = {awg_params['Jmax']}\n"
		f"S1 = {awg_params['S1']}\n"
		f"S2 = {awg_params['S2']}\n"
		f"H1 = {awg_params['H1']}\n"
		f"H2 = {awg_params['H2']}\n"
		f"H3 = {awg_params['H3']}\n"
		f"H4 = {awg_params['H4']}\n"
		"\n"
	)

	# Peers section
	peers = _extract_awg_peers(user_db, srv_name)
	for peer in peers:
		wg0conf = (
			f"{wg0conf}"
			f"[Peer] #{peer['name']}\n"
			f"PublicKey = {peer['pub_key']}\n"
			f"PresharedKey = {awg_params['psk_key']}\n"
			f"AllowedIPs = {peer['IP']}/32\n"
			"\n"
		)

	return wg0conf

def generate_server_json(user_db, srv_name, xray_params):
	clients = _extract_xray_clients(user_db, srv_name)
	userids = [cl['id'] for cl in clients]
	cl = [{"flow": "xtls-rprx-vision", "id": ID} for ID in userids]
	
	config = {
		"inbounds": [{
			"port": 443,
			"protocol": "vless",
			"settings": {
				"clients": cl,
				"decryption": "none"
			},
			"streamSettings": {
				"network": "tcp",
				"realitySettings": {
					"dest": xray_params["site"]+":443",
					"privateKey": xray_params["priv_key"],
					"serverNames": [xray_params["site"]],
					"serverNames": [xray_params["short_id"]]
				},
				"security": "reality"
			}
		}],
		"log": {"loglevel": "error"},
		"outbounds": [{"protocol": "freedom"}]
	}

	return json.dumps(config, indent=4)

def generate_clientsTable(user_db, srv_name, type):
	table = []

	match type:
		case "awg":
			peers = _extract_awg_peers(user_db, srv_name)

			for peer in peers:
				table.append({
					"clientId": peer["pub_key"],
					"userData": {
						"clientName": peer["name"],
						"creationDate": peer["creation_date"]
					}
				})
		case "xray":
			clients = _extract_xray_clients(user_db, srv_name)

			for client in clients:
				table.append({
					"clientId": client["id"],
					"userData": {
						"clientName": client["name"],
						"creationDate": client["creation_date"]
					}
				})
		case _ :
			table = None

	return json.dumps(table, indent=4, ensure_ascii=False) + "\n"

def _generate_xray_cliend_id():
	return str(uuid.uuid4())

def _generate_awg_keypair():
	private_key = x25519.X25519PrivateKey.generate()
	public_key = private_key.public_key()

	private_bytes = private_key.private_bytes_raw()
	public_bytes = public_key.public_bytes_raw()

	priv_key = base64.b64encode(private_bytes).decode()
	pub_key = base64.b64encode(public_bytes).decode()

	return priv_key, pub_key

def _get_awg_ip_iterator(peers):
	ips = [peer['IP'] for peer in peers]
	ip_stem = '.'.join(ips[0].split('.')[:-1]) + '.' if ips else '10.8.1.'
	ips.append(ip_stem + '1')
	net = IPv4Network(ip_stem + '0' + '/24')
	ip_it = (ip for ip in net.hosts() if str(ip) not in ips)
	return ip_it

def _grant_awg_access(user, ip_it, srv_name):
	next_ip = next(ip_it)
	if next_ip is None:
		sys.exit("Not enough IP addresses.")
	priv_key, pub_key = _generate_awg_keypair()

	new_key_data = {
		"IP": str(next_ip),
		"priv_key": priv_key,
		"pub_key": pub_key
	}

	kd = __get_key_data(user, srv_name, "awg")
	if kd is None:
		user['awg_key_data'].append({
			'srv_name': srv_name,
			'key_data': [new_key_data]
		})
	else:
		kd.append(new_key_data)

def _grant_xray_access(user, srv_name):
	kd = __get_key_data(user, srv_name, "xray")

	if kd is None:
		user['xray_key_data'].append({
			'srv_name': srv_name,
			'key_data': {"id": _generate_xray_cliend_id()}
		})
	else:
		sys.exit("Multiple keys for Xray is not supported.")

def grant_access(user_db, username, srv_name, n, type):
	if not is_user(user_db, username):
		sys.exit("User " + username + " not found.")
	if n > 1 and type == "xray":
		sys.exit("Multiple keys for Xray is not supported.")

	user = get_user(user_db, username)

	match type:
		case "awg":
			peers = _extract_awg_peers(user_db, srv_name)
			ip_it = _get_awg_ip_iterator(peers)
			for _ in range(n):
				_grant_awg_access(user, ip_it, srv_name)
		case "xray":
			_grant_xray_access(user, srv_name)

def revoke_access(user_db, username, srv_name, type):
	if not is_user(user_db, username):
		sys.exit("User " + username + " not found.")
	user = get_user(user_db, username)

	key_data = user[type+'_key_data']
	key_data[:] = [kd for kd in key_data
		if kd['srv_name'] != srv_name]

def _get_awg_params_template():
	return {
		"port": "",
		"Jmax": "",
		"Jc": "",
		"MTU": "1420",
		"H2": "",
		"H1": "",
		"Jmin": "",
		"pub_key": "",
		"priv_key": "",
		"H4": "",
		"psk_key": "",
		"S2": "",
		"S1": "",
		"H3": ""
	}

def _get_xray_params_template():
	return {
		"site": "",
		"short_id": "",
		"pub_key": "",
		"priv_key": ""
	}

def make_empty_server(srv_name, awg=False, xray=False):
	awg_params = _get_awg_params_template() if awg else {}
	xray_params = _get_xray_params_template() if xray else {}

	return {
		"srv_name": srv_name.lower(),
		"display_name": srv_name.title(),
		"location": "",
		"description": "",
		"display_order": 0,
		"key_name": "",
		"dns1": "172.29.172.254",
		"dns2": "1.0.0.1",
		"host_name": "",
		"awg_params": awg_params,
		"xray_params": xray_params
	}
