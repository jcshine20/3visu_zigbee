import sqlite3
import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import csv
import math
import numpy as np
import matplotlib.pyplot as plt


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


def computePitchAngle(accx, accz, gyroy, thetaOld, dt):
    accx = float(accx)
    accz = float(accz)
    gyroy = float(gyroy)
    thetaMeasured = -math.atan2(accx / 9.8, accz / 9.8) / 2 / np.pi * 360
    theta = (thetaOld + gyroy * dt) * 0.95 + thetaMeasured * 0.05
    return theta


def computeRollAngle(accy, accz, gyrox, phiOld, dt):
    accy = float(accy)
    accz = float(accz)
    gyrox = float(gyrox)
    phiMeasured = math.atan2(accy / 9.8, accz / 9.8) / 2 / np.pi * 360
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
plt.style.use('fivethirtyeight')
roll_vals = []
pitch_val = []
yaw_vals = []
index = count()

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

datadict = dict(achse_x=[], achse_y=[], achse_z=[], gyro_x=[], gyro_y=[], gyro_z=[], mag_x=[], mag_y=[], mag_z=[])


def insert_highscore(name, highscore):
    cursor.execute("INSERT INTO userscores VALUES (?, ?)", (name, highscore))


def get_usernames():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM userscores")
    entries = cursor.fetchall()
    return {entry for entry in entries}


def get_highscore(name):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM userscores WHERE username = '{name}'")
    return max(cursor.fetchall())[1]


if __name__ == '__main__':
    # for i in range(5):
    #    insert_highscore(f"Username{i}", random.randint(10, 20))
    print(get_usernames())


def insert_data(data):
    tuplelistachse = []

    for entry in range(len(data["achse_x"])):
        tuplelistachse.append((
            data["achse_x"][entry],
            data["achse_y"][entry],
            data["achse_z"][entry]
        ))
    # tuplelistachse[zip(data["achse_x"][entry],
    #                   data["achse_y"][entry],
    #                   data["achse_z"][entry]) for data in range(len(data["achse_x"]))]
    tuplelistgyro = []
    for entry in range(len(data["achse_x"])):
        tuplelistgyro.append((
            data["gyro_x"][entry],
            data["gyro_y"][entry],
            data["gyro_z"][entry]
        ))
    tuplelistmag = []
    for entry in range(len(data["achse_x"])):
        tuplelistmag.append((
            data["mag_x"][entry],
            data["mag_y"][entry],
            data["mag_z"][entry]
        ))
    namelist = dict(achsen=tuplelistachse, gyroscop=tuplelistgyro, quaterionen=tuplelistmag)

    #for name, data in namelist.items():
    #    # cursor.executemany(f"INSERT INTO {name} VALUES (?, ?, ?)", data)
    #    cursor.execute(f"SELECT rowid, * FROM {name} ")
    #    entries = cursor.fetchall()
    #    for entry in entries:
    #        print(f" rowID: {entry[0]} {name}_x:{entry[1]}   {name}_y:{entry[2]}   {name}_z:{entry[3]}")


for set in open('bewegung.txt', 'r'):
    set.strip('\n')
    setlist = set.split(",")
    if 'accx' not in setlist and len(set) > 5:
        datadict["achse_x"].append(setlist[0])
        datadict["achse_y"].append(setlist[1])
        datadict["achse_z"].append(setlist[2])
        datadict["gyro_x"].append(setlist[3])
        datadict["gyro_y"].append(setlist[4])
        datadict["gyro_z"].append(setlist[5])
        datadict["mag_x"].append(setlist[6])
        datadict["mag_y"].append(setlist[7])
        datadict["mag_z"].append(setlist[8])

insert_data(datadict)
conn.commit()
conn.close()
