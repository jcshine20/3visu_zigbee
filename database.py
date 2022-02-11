import datetime
import sqlite3
import random
from itertools import count
#import pandas as pd
#import matplotlib.pyplot as plt
#from matplotlib.animation import FuncAnimation
#import csv
import math
import numpy as np
#import matplotlib.pyplot as plt
import time


def get_pitch_data():
    pitchdatalist = []
    cursor.execute("SELECT * FROM achsen ORDER BY ROWID ASC LIMIT 1")
    temp = cursor.fetchall()
    pitchdatalist.append(temp[0][0])
    pitchdatalist.append(temp[0][2])
    cursor.execute("SELECT * FROM gyroscop ORDER BY ROWID ASC LIMIT 1")
    temp = cursor.fetchall()
    pitchdatalist.append(temp[0][1])
    return pitchdatalist


def get_roll_data():
    rolldatalist = []
    cursor.execute("SELECT * FROM achsen ORDER BY ROWID ASC LIMIT 1")
    temp = cursor.fetchall()
    rolldatalist.append(temp[0][1])
    rolldatalist.append(temp[0][2])
    cursor.execute("SELECT * FROM gyroscop ORDER BY ROWID ASC LIMIT 1")
    temp = cursor.fetchall()
    rolldatalist.append(temp[0][2])
    return rolldatalist


def get_yaw_data():
    yawdatalist = []
    cursor.execute("SELECT * FROM achsen ORDER BY ROWID ASC LIMIT 1")
    temp = cursor.fetchall()
    yawdatalist.append(temp[0][0])
    yawdatalist.append(temp[0][1])
    yawdatalist.append(temp[0][2])
    return yawdatalist


def computePitchAngle(beschlx, beschlz, gyroy, thetaOld, dt):
    beschlx = float(beschlx)
    beschlz = float(beschlz)
    gyroy = float(gyroy)
    thetaMeasured = -math.atan2(beschlx / 9.8, beschlz / 9.8) / 2 / np.pi * 360
    theta = (thetaOld + gyroy * dt) * 0.95 + thetaMeasured * 0.05
    return theta


def computeRollAngle(beschly, beschlz, gyrox, phiOld, dt):
    beschly = float(beschly)
    beschlz = float(beschlz)
    gyrox = float(gyrox)
    phiMeasured = math.atan2(beschly / 9.8, beschlz / 9.8) / 2 / np.pi * 360
    phi = (phiOld - gyrox * dt) * 0.95 + phiMeasured * 0.05
    return phi


def computeYawAngle(theta, phi, magx, magy, magz):
    magx = float(magx)
    magy = float(magy)
    magz = float(magz)
    phiRad = phi * toRad
    thetaRad = theta * toRad
    xMagnetometer = magx * math.cos(thetaRad) - magy * math.sin(phiRad) * math.sin(thetaRad) + magz * math.cos(
        phiRad) * math.sin(thetaRad)
    yMagnetometer = magy * math.cos(phiRad) + magz * math.sin(phiRad)
    phi = math.atan2(xMagnetometer, yMagnetometer) * toDeg
    return phi


theta = 0
phi = 0
counter = 12
toRad = 2 * np.pi / 360
toDeg = 1 / toRad
#plt.style.use('fivethirtyeight')
roll_vals = []
pitch_val = []
yaw_vals = []
index = count()

conn = sqlite3.connect('data.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
cursor = conn.cursor()

datadict = dict(beschl_x=[], beschl_y=[], beschl_z=[],
                gyro_x=[], gyro_y=[], gyro_z=[],
                mag_x=[], mag_y=[], mag_z=[], time=[])


def insert_highscore(name, highscore, dt=datetime.datetime.now().replace(microsecond=0)):
    cursor.execute("INSERT INTO userscores VALUES (?, ?, ?)", (name, highscore, dt))
    # cursor.execute("SELECT * FROM userscores")
    # entries = cursor.fetchall()
    # for entry in entries:
    #    print(entry)


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


if __name__ == '__main__':
    #insert_highscore(f"Username{11}", random.randint(10, 20), datetime.datetime.now().replace(microsecond=0))
    conn = sqlite3.connect('data.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM quaterionen")
    entries = cursor.fetchall()
    for entry in entries:
        print(f" rowID: {entry[0]} x:{entry[1]}   _y:{entry[2]}  _z:{entry[3]} {entry[4]}")


# print(get_usernames())


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


for set in open('bewegung.txt', 'r'):
    set.strip('\n')
    setlist = set.split(",")
    if 'accx' not in setlist and len(set) > 5:
        datadict["beschl_x"].append(setlist[0])
        datadict["beschl_y"].append(setlist[1])
        datadict["beschl_z"].append(setlist[2])
        datadict["gyro_x"].append(setlist[3])
        datadict["gyro_y"].append(setlist[4])
        datadict["gyro_z"].append(setlist[5])
        datadict["mag_x"].append(setlist[6])
        datadict["mag_y"].append(setlist[7])
        datadict["mag_z"].append(setlist[8])
        datadict["time"].append(datetime.datetime.now().replace(microsecond=0))

#insert_data(datadict)
conn.commit()
conn.close()
