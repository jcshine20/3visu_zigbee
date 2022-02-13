import serial
import time
import computation
import matplotlib.pyplot as plt
from drawnow import *

def makeFig():
    plt.subplot(1,2,1)
    plt.ylim(-180, 180)
    plt.ylabel("Angles in Degrees")
    plt.xlabel("Time in s")
    plt.title("Euler Angles")
    plt.plot(pitch_values_euler, time_values_euler, 'ro-', label="Pitch")
    plt.plot(roll_values_euler, time_values_euler, 'bo-', label="Roll")
    plt.plot(yaw_values_euler, time_values_euler, 'go-', label="Yaw")
    plt.legend('upper left')

    plt.subplot(1,2,1)
    plt.ylim(-180, 180)
    plt.ylabel("Angles in Degrees")
    plt.xlabel("Time in s")
    plt.title("Quaternions")
    plt.plot(pitch_values_quat, time_values_quat, 'ro-', label="Pitch")
    plt.plot(roll_values_quat, time_values_quat, 'bo-', label="Roll")
    plt.plot(yaw_values_quat, time_values_quat, 'go-', label="Yaw")
    plt.legend('upper left')


# Create figure for plotting
fig = plt.figure()


time_values_euler = []
time_values_quat = []
roll_values_euler = []
pitch_values_euler = []
yaw_values_euler = []
pitch_values_quat = []
roll_values_quat = []
yaw_values_quat = []
plt.ion()

com = "com5"
Data = serial.Serial(com, 115200)

oldTimeEuler = time.time()
plotTimeEuler = 0

oldTimeQuat = time.time()
plotTimeQuat = 0

phi = 0
theta = 0

counterEuler = 0
counterQuat = 0

while True:
    while (Data.inWaiting() == 0):
        pass
    dataPacket = Data.readline()
    dataPacket = str(dataPacket, 'utf-8')
    dataPacket = dataPacket.strip('\r\n')
    splitPacket = dataPacket.split(",")


    if int(splitPacket[0]) == 0:
        counterEuler += 1
        newTimeEuler = time.time()
        deltaTimeEuler = newTimeEuler - oldTimeEuler
        oldTimeEuler = newTimeEuler
        splitPacket = splitPacket.append(str(deltaTimeEuler))
        plotTimeEuler += deltaTimeEuler
        row = splitPacket

        roll = computation.computeRollAngle(accy=row[2], accz=row[3], gyrox=row[4], phiOld=phi, dt=float(row[11]))
        pitch = computation.computePitchAngle(accx=row[1], accz=row[3], gyroy=row[5], thetaOld=theta, dt=float(row[11]))
        yaw = computation.computeYawAngle(theta=pitch, phi=roll, magx=row[7], magy=row[8], magz=row[9])
        phi = roll
        theta = pitch

        pitch_values_euler.append(pitch)
        roll_values_euler.append(roll)
        yaw_values_euler.append(yaw)
        time_values_euler.append(plotTimeEuler)
        if counterEuler > 20:
            pitch_values_euler.pop(0)
            roll_values_euler.pop(0)
            yaw_values_euler.pop(0)
            time_values_euler.pop(0)
        drawnow(makeFig)
        plt.pause(0.001)

    if int(splitPacket[0]) == 1:
        counterQuat += 1
        newTimeQuat = time.time()
        deltaTimeQuat = newTimeQuat - oldTimeQuat
        oldTimeQuat = newTimeQuat
        splitPacket = splitPacket.append(str(deltaTimeQuat))
        plotTimeQuat += deltaTimeQuat
        row = splitPacket

        q0 = float(row[1])
        q1 = float(row[2])
        q2 = float(row[3])
        q3 = float(row[4])

        roll, pitch, yaw = computation.transformQuatEuler(q0, q1, q2, q3)

        pitch_values_quat.append(pitch)
        roll_values_quat.append(roll)
        yaw_values_quat.append(yaw)
        time_values_quat.append(plotTimeEuler)
        if counterQuat > 20:
            pitch_values_quat.pop(0)
            roll_values_quat.pop(0)
            yaw_values_quat.pop(0)
            time_values_quat.pop(0)
        drawnow(makeFig)
        plt.pause(0.001)