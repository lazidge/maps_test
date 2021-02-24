from lib import run_server, get, read_html, post
from store import Node, extract_osm_nodes, add_neighbors
from algorithms import get_closest_node_id, find_shortest_path
from collections import defaultdict
import account
import login
import json
from db import *

if create_db("ostgdb"):
    nodes = extract_osm_nodes('map.osm')
    nodes = add_neighbors(nodes)
    lonely= []

    for node in nodes:
        if not nodes[node].neighbors:
            lonely.append(node)

    for node in lonely:
        del nodes[node]
    update_db(nodes, "ostgdb")

nodes = get_data("ostgdb")
tiles = defaultdict(lambda: [])

for node in nodes:
    tiles[format(nodes[node].lat, '.3f'), format(nodes[node].lng, '.3f')].append(nodes[node].id)

@get('/')
def index():
     return read_html('templates/index.html')


@get('/favicon.ico')
def favicon():
    icon = open("data/favicon.ico", "rb")
    return icon.read()


@post('/shortest-path')
def shortest_path(body):
    body = json.loads(body)
    source_id = get_closest_node_id(nodes, tiles, Node('-1', body['lat1'], body['lng1']))
    target_id = get_closest_node_id(nodes, tiles, Node('-1', body['lat2'], body['lng2']))
    print("source:",nodes[str(source_id)].neighbors)
    print("target:",nodes[str(target_id)].neighbors)
    path = find_shortest_path(nodes, source_id, target_id)
    for i in range(len(path)):
        node_id = path[i]
        path[i] = (nodes[str(node_id)].lat, nodes[str(node_id)].lng)
    response = {'path': path} # The front-end expects the response to have a 'path' key
    return json.dumps(response)


@post('/register')
def register(registerinput):
    this_input = registerinput.split(',')
    this_input[0] = this_input[0][13:-1]
    this_input[1] = this_input[1][12:-2]
    registerinput = (this_input[0], this_input[1])
    try:
        usrpass = account.get_data("users")
    except:
        account.create_db("users")
        usrpass = account.get_data("users")

    if account.check_login(registerinput):
        print("no fuck u")
        return '{"status": "False"}'
    else:
        account.update_db((registerinput[0], registerinput[1]), "users")
        return '{"status": "True", "username": ' + '"' + this_input[0] + '"' + '}'


@post('/login')
def login(logininput):
    this_input = logininput.split(',')
    this_input[0] = this_input[0][13:-1]
    this_input[1] = this_input[1][12:-2]
    logininput = (this_input[0], this_input[1])
    if account.check_login(logininput):
        print('{"status": "True", "username": ' + '"' + this_input[0] + '"' + '}')
        return '{"status": "True", "username": ' + '"' + this_input[0] + '"' + '}'
    else:
        return '{"login": "False"}'
        usrpass = account.get_data("users")

    if account.check_login(registerinput):
        return False
    else:
        account.update_db((registerinput[0], registerinput[1]), "users")


run_server(1340)
