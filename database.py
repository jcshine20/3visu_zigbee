import sqlite3
import random

conn = sqlite3.connect('data.db')

cursor = conn.cursor()

datadict = {"achse_x": [],
            "achse_y": [],
            "achse_z": [],
            "gyro_x": [],
            "gyro_y": [],
            "gyro_z": [],
            "mag_x": [],
            "mag_y": [],
            "mag_z": []
            }
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


def insert_data(data: dict):
    tuplelistachse = []
    for entry in range(len(data["achse_x"])):
        tuplelistachse.append((
            data["achse_x"][entry],
            data["achse_y"][entry],
            data["achse_z"][entry]
        ))
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
    namelist = {"achsen": tuplelistachse,
                "gyroscop": tuplelistgyro,
                "quaterionen": tuplelistmag}

    for name, data in namelist.items():
        # cursor.executemany(f"INSERT INTO {name} VALUES (?, ?, ?)", data)
        cursor.execute(f"SELECT rowid, * FROM {name} ")

    # print(cursor.fetchall())
    entries = cursor.fetchall()
    print(entries)
    for entry in entries:
        print(f" rowID: {entry[0]} xachse:{entry[1]}   yachse:{entry[2]}   zachse:{entry[3]}")


def get_pitch():
    pitchdatalist = []
    cursor.execute("SELECT * FROM achsen ORDER BY ROWID ASC LIMIT 1")
    temp = cursor.fetchall()
    pitchdatalist.append(temp[0][0])
    pitchdatalist.append(temp[0][2])
    cursor.execute("SELECT * FROM gyroscop ORDER BY ROWID ASC LIMIT 1")
    temp = cursor.fetchall()
    pitchdatalist.append(temp[0][1])
    return pitchdatalist


def get_roll():
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


print(get_pitch())
print(get_roll())
print(get_yaw_data())

# insert_data(datadict)
conn.commit()
conn.close()

# cursor.executemany("INSERT INTO achsen VALUES (?, ?, ?)", simulated_values)

# cursor.execute("SELECT rowid, * FROM achsen LIMIT 50")

# cursor.execute("""UPDATE achsen SET x_achse = 999 WHERE y_achse = 22 """)
# cursor.executemany("INSERT INTO achsen VALUES (?, ?, ?)", simulated_values)
# cursor.execute("SELECT rowid, * FROM achsen")
# entries = cursor.fetchall()
# for entry in entries:
#    print(f" rowID: {entry[0]} xachse:{entry[1]}   yachse:{entry[2]}   zachse:{entry[3]}")
#
