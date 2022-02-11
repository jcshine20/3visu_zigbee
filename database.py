import datetime
import sqlite3
import random
from itertools import count
import math
import numpy as np
import time

conn = sqlite3.connect('data.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
cursor = conn.cursor()

datadict = dict(beschl_x=[], beschl_y=[], beschl_z=[],
                gyro_x=[], gyro_y=[], gyro_z=[],
                mag_x=[], mag_y=[], mag_z=[], time=[])


def insert_highscore(name, highscore, dt=datetime.datetime.now().replace(microsecond=0)):
    cursor.execute("INSERT INTO userscores VALUES (?, ?, ?)", (name, highscore, dt))


def get_usernames():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM userscores")
    entries = cursor.fetchall()
    return {entry for entry in entries}


def get_highscore(name):
    conn = sqlite3.connect('data.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM userscores WHERE username = '{name}'")
    return max(cursor.fetchall())[1]


def insert_user(name, dt=datetime.datetime.now().replace(microsecond=0)):
    conn = sqlite3.connect('data.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM userscores")
    namelist = cursor.fetchall()
    if name not in namelist:
        cursor.execute("INSERT INTO userscores VALUES (?, ?, ?)", (name, 0, dt))
        conn.commit()


#if __name__ == '__main__':
#    conn = sqlite3.connect('data.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
#    cursor = conn.cursor()
#    cursor.execute("SELECT * FROM quaterionen")
#    entries = cursor.fetchall()
#    for entry in entries:
#        print(f" rowID: {entry[0]} x:{entry[1]}   _y:{entry[2]}  _z:{entry[3]} {entry[4]}")


def insert_data(data):
    def format_data(data_part, i, name):
        return data_part[f'{name}_x'][i], data_part[f'{name}_y'][i], data_part[f'{name}_z'][i], data_part["time"][i]

    conn = sqlite3.connect('data.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cursor = conn.cursor()

    tuplelistbeschl = [format_data(data, entry, "beschl") for entry in range(len(data['beschl_x']))]
    tuplelistgyro = [format_data(data, entry, "gyro") for entry in range(len(data['gyro_x']))]
    tuplelistmag = [format_data(data, entry, "mag") for entry in range(len(data['mag_x']))]

    namelist = dict(beschleunigung=tuplelistbeschl, gyroscop=tuplelistgyro, magnetometer=tuplelistmag)
    for name, data in namelist.items():
        cursor.executemany(f"INSERT INTO {name} VALUES (?, ?, ?, ?)", data)
        cursor.execute(f"SELECT rowid, * FROM {name} ")
        entries = cursor.fetchall()
        for entry in entries:
            print(f" rowID: {entry[0]} {name}_x:{entry[1]}   {name}_y:{entry[2]}   {name}_z:{entry[3]} {entry[4]}")


def insert_quater(data):
    conn = sqlite3.connect('data.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cursor = conn.cursor()

    def format_data(data_part, i):
        return data_part["q0"][i], data_part["q1"][i], data_part["q2"][i], data_part["q3"][i], data_part["time"][i]

    tuplelistquater = [format_data(data, entry) for entry in range(len(data['q1']))]
    cursor.executemany(f"INSERT INTO quaterionen VALUES (?, ?, ?, ?, ?)", tuplelistquater)


conn.commit()
conn.close()
