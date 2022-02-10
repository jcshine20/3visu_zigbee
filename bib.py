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