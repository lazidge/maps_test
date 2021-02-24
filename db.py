import sqlite3
from store import Node

def create_db(name):
    """
    Function that tries to create a database with a given name
    """
    conn = sqlite3.connect(name + '.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''CREATE TABLE ''' + name + \
        '''(id int, lat decimal, long decimal, neighbors text)''')
        conn.commit()
        conn.close()
        return True
    except(sqlite3.OperationalError):
        conn.close()
        pass


def update_db(nodes, name):
    """
    Function that updates a given database with supplied map data
    """
    conn = sqlite3.connect(name + '.db')
    cursor = conn.cursor()
    command = []
    for node in nodes:
        neighbors = ":".join(nodes[node].neighbors)
        command.append((nodes[node].id, nodes[node].lat, nodes[node].lng, \
        neighbors))
    cursor.executemany("INSERT INTO " + name + " VALUES (?,?,?,?)", command)
    conn.commit()
    conn.close()


def get_data(name):
    """
    Fetches the data from a given sql database and returns the rows in a dict
    """
    conn = sqlite3.connect(name + '.db')
    cursor = conn.cursor()
    command = 'SELECT * FROM ' + name
    nodes = {}
    neighbor = {}
    for row in cursor.execute(command):
        nodes[str(row[0])] = Node(row[0], row[1], row[2])
        neighbor[str(row[0])] = row[3]
    for node in neighbor:
        nodes[node].neighbors = neighbor[node].split(':')
    return nodes


def purge_data(name):
    """
    Deletes all data from database 'name'
    """
    conn = sqlite3.connect(name + '.db')
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM ' + name)
        conn.commit()
        conn.close
    except:
        conn.close()
