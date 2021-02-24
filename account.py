from hashlib import *
import sqlite3

def create_db(name):
    """
    Function that tries to create a database with a given name
    """
    conn = sqlite3.connect(name + '.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''CREATE TABLE ''' + name + \
        '''(username text, hashpass text, path text)''')
        conn.commit()
        conn.close()
        return True
    except(sqlite3.OperationalError):
        conn.close()
        pass


def update_db(userpass, name):
    """
    Function that updates a given database with supplied map data
    """
    password = userpass[1]
    b = password.encode('utf-8')
    m = sha512()
    m.update(b)
    password = m.digest()
    userpass = (userpass[0], password, "")
    conn = sqlite3.connect(name + '.db')
    cursor = conn.cursor()
    command = userpass
    cursor.execute("INSERT INTO " + name + " VALUES (?,?,?)", command)
    conn.commit()
    conn.close()


def get_data(name):
    """
    Fetches the data from a given sql database and returns the rows in a dict
    """
    conn = sqlite3.connect(name + '.db')
    cursor = conn.cursor()
    command = 'SELECT * FROM ' + name
    users = {}
    for row in cursor.execute(command):
        print(row)
        users[row[0]] = row[1]
    return users


def check_login(usrpass):
    """
    Checks the login that the user entered and compares it to the database
    """
    print(usrpass)
    password = usrpass[1]
    b = password.encode('utf-8')
    m = sha512()
    m.update(b)
    password = m.digest()
    if not usrpass[0] in get_data('users'):
        print("input: ", usrpass[0])
        print("db: ", get_data('users'))
        return False
    if get_data('users')[usrpass[0]] == password:
        return True
    else:
        return False
