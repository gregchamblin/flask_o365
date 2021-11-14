import sqlite3
from sqlite3 import Error

path = "private/sqlite3.db"

def create_structure(db_file):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute('''CREATE TABLE brands
             (id, brand, subbrand, active)''')
    c.execute('''CREATE TABLE phases
             (workphase,hwtype, hwlabel, hwdescription)''')
    c.execute('''CREATE TABLE o365clientwide
             (client_id, client_secret, tenant, api_version)''')
    c.execute('''CREATE TABLE o365teamspecific
             (team_name, use_desc, type, o365_id, path)''')
    conn.close()

if __name__ == '__main__':
    create_structure(path)