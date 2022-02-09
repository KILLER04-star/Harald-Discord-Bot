import datetime
import sqlite3

import security
import errorlog


def create_connection(db_file):
    # opens a connection to a sqlite-database containing necessary
    # information about the servers, like in which channel the bot is supposed to send memes
    conn = None

    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        return conn
    except sqlite3.Error as e:
        errorlog.log_error(e, "")
    return conn


def create_tables(conn):
    try:
        c = conn.cursor()

        c.execute('''CREATE TABLE Info (Server_id text, Channel_id text)''')
        c.execute('''CREATE TABLE Webhook_Channels (Server_id text, Channel_id text)''')
        c.execute('''CREATE TABLE Status(Server_id text, Sent text, Notes text)''')

        conn.commit()
    except sqlite3.Error as e:
        errorlog.log_error(e, "")


def get_channel_of_server(conn, server_id, table):
    c = conn.cursor()
    server_id = security.encode(server_id)
    server_id = (server_id,)

    c.execute('SELECT Channel_id FROM ' + table + ' WHERE Server_id=?', server_id)
    result = (str(c.fetchall()).replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace("[",
                                                                                                            "").replace(
        "]", ""))
    result = int(security.decode(str(result)))
    return result


def server_already_existing(server_id, table, conn):
    c = conn.cursor()
    server_id = security.encode(server_id)
    server_id = (server_id,)
    c.execute('SELECT * FROM ' + table + ' WHERE Server_id=?', server_id)

    return len(c.fetchall())


def insert_data(server_id, channel_id, table, conn):
    server_id = security.encode(server_id)
    channel_id = security.encode(channel_id)

    values = [server_id, channel_id]

    c = conn.cursor()

    c.execute('INSERT INTO ' + table + ' VALUES (?,?)', values)

    conn.commit()


def upgrade_channel(Server_id, channel_id, table, conn):
    c = conn.cursor()
    const_server_id = Server_id
    Server_id = security.encode(Server_id)
    Server_id = (Server_id,)

    c.execute('DELETE FROM ' + table + ' WHERE Server_id=?', Server_id)

    conn.commit()

    insert_data(const_server_id, channel_id, table, conn)


def delete_channel(server_id, table, conn):
    c = conn.cursor()
    my_server_id = security.encode(server_id)
    my_server_id = (my_server_id,)

    c.execute('DELETE FROM ' + table + ' WHERE Server_id=?', my_server_id)

    conn.commit()

    delete_server_status(server_id=server_id, conn=conn)


def delete_server_status(server_id, conn):
    c = conn.cursor()
    server_id = security.encode(server_id)
    my_server_id = (server_id,)

    print("Delete Server Status for: " + server_id + " " + str(datetime.datetime.today()))
    c.execute('DELETE FROM Status WHERE Server_id=?', my_server_id)

    conn.commit()


def set_server_status(server_id, status, notes, conn):

    c = conn.cursor()

    server_id = security.encode(server_id)

    values = [server_id, status, notes]

    c.execute('INSERT INTO Status VALUES (?,?,?)', values)

    conn.commit()

    print("Setting Status for: " + server_id + " Time: " + str(datetime.datetime.today()))
