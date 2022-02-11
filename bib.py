#cursor.execute("""UPDATE achsen SET x_achse = 999 WHERE y_achse = 22 """)
#cursor.execute(""" DROP TABLE achsen """)

cursor.execute("""CREATE TABLE userscores (
           username text,
           highscore integer
           )""")


#cursor.execute("""CREATE TABLE quaterionen (
#           x_quaterion real,
#           y_quaterion real,
#           z_quaterion real
#           )""")
#
#cursor.execute("""CREATE TABLE gyroscop (
#           x_quaterion real,
#           y_quaterion real,
#           z_quaterion real
#           )""")
#
#cursor.execute("""CREATE TABLE achsen (
#           x_achse real,
#           y_achse real,
#           z_achse real
#           )""")

# cursor.executemany("INSERT INTO achsen VALUES (?, ?, ?)", simulated_values)

# cursor.execute("SELECT rowid, * FROM achsen LIMIT 50")

# cursor.execute("""UPDATE achsen SET x_achse = 999 WHERE y_achse = 22 """)
# cursor.executemany("INSERT INTO achsen VALUES (?, ?, ?)", simulated_values)
# cursor.execute("SELECT rowid, * FROM achsen")
# entries = cursor.fetchall()
# for entry in entries:
#    print(f" rowID: {entry[0]} xachse:{entry[1]}   yachse:{entry[2]}   zachse:{entry[3]}")
#

# cursor.executemany(
# "INSERT INTO achsen VALUES (?, ?, ?)", simulated_values)

# cursor.execute("SELECT rowid, * FROM achsen LIMIT 50")

# cursor.execute("""UPDATE achsen SET x_achse = 999 WHERE y_achse = 22 """)
# cursor.executemany("INSERT INTO achsen VALUES (?, ?, ?)", simulated_values)
# cursor.execute("SELECT rowid, * FROM achsen")
# entries = cursor.fetchall()
# for entry in entries:
#    print(f" rowID: {entry[0]} xachse:{entry[1]}   yachse:{entry[2]}   zachse:{entry[3]}")
#
# cursor.executemany("INSERT INTO achsen VALUES (?, ?, ?)", simulated_values)

# cursor.execute("SELECT rowid, * FROM achsen LIMIT 50")

# cursor.execute("""UPDATE achsen SET x_achse = 999 WHERE y_achse = 22 """)
# cursor.executemany("INSERT INTO achsen VALUES (?, ?, ?)", simulated_values)
# cursor.execute("SELECT rowid, * FROM achsen")
# entries = cursor.fetchall()
# for entry in entries:
#    print(f" rowID: {entry[0]} xachse:{entry[1]}   yachse:{entry[2]}   zachse:{entry[3]}")
#
# for i in range(12, 190):
#    counter += 1
#    print(get_pitch_data())
#    pitch = computePitchAngle(accx=get_pitch_data()[0], accz=get_pitch_data()[1], gyroy=get_pitch_data()[2],
#                              thetaOld=theta, dt=0.001)
#    theta = pitch
#
#    roll = computeRollAngle(accy=get_roll_data()[0], accz=get_roll_data()[1], gyrox=get_roll_data()[2],
#                            phiOld=phi, dt=0.001)
#    phi = roll
#
#    yaw = computeYawAngle(theta=pitch, phi=roll, magx=get_yaw_data()[0], magy=get_yaw_data()[1],
#                          magz=get_yaw_data()[2])
#    cursor.execute(f"DELETE from achsen where rowid = {counter}")
#    cursor.execute(f"DELETE from gyroscop where rowid = {counter}")
#    cursor.execute(f"DELETE from quaterionen where rowid = {counter}")
#    roll_vals.append(roll)
#    pitch_val.append(pitch)
#    yaw_vals.append(yaw)
#
# values = [x for x in range(178)]


# plt.plot(values, roll_vals, label="roll")
# plt.plot(values, yaw_vals, label="yaw")
# plt.plot(values, pitch_val, label="pitch")
# plt.tight_layout()
# plt.show()

# ani = FuncAnimation(plt.gcf(), animate, 100)



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
