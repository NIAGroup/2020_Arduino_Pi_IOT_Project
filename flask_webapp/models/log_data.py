import sqlite3
import sys


def log_devices(name, connected):

    conn=sqlite3.connect('pid_app.db')
    # create a cursor => handle to access the db
    cur = conn.cursor()

    # Create a Table if it doesn't already exist
    create_table = "CREATE TABLE IF NOT EXISTS devices(rDatetime, name TEXT, connected INTEGER)"
    cur.execute(create_table)

    # write to the table
    attributes = (name, connected)
    insert_device = "INSERT INTO devices values(datetime(CURRENT_TIMESTAMP, 'localtime'), (?), (?))"
    cur.execute(insert_device,attributes)
    conn.commit()
    conn.close()

## add test values
#name = "test1"
#connected = 1 
#
#if name is not None and connected is not None:
#    log_devices(name, connected)
#else:
#    log_devices(1, -999, -999)
#
#name = "test2"
#connected = 0 
#log_devices(name, connected)


