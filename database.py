import sqlite3
import random

conn = sqlite3.connect('data.db')

cursor = conn.cursor()


f = {
    "achse_x": [x for x in range(100)],
    "achse_y": [x for x in range(100)],
    "achse_z": [x for x in range(100)],
    "gyro_x": [x for x in range(100)],
    "gyro_y": [x for x in range(100)],
    "gyro_z": [x for x in range(100)],
    "mag_x": [x for x in range(100)],
    "mag_y": [x for x in range(100)],
    "mag_z": [x for x in range(100)],
}


# for n in range(100):
#    simulated_values.append(
#        (random.randint(1, 10), random.randint(11, 20), random.randint(21, 30))
#    )

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

    #for name, data in namelist.items():
    #   cursor.executemany(f"INSERT INTO {name} VALUES (?, ?, ?)", data)
    #   cursor.execute(f"SELECT rowid, * FROM {name} ")
#
    #print(cursor.fetchall())
    entries = cursor.fetchall()
    print(entries)
    for entry in entries:
       print(f" rowID: {entry[0]} xachse:{entry[1]}   yachse:{entry[2]}   zachse:{entry[3]}")


insert_data(f)
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

