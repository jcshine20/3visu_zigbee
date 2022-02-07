import csv
import math
import numpy as np

# TODO
#  1. Zeitstempel
#  2. gesendetes Datenformat vom ZigBee Modul
#  3. Lesen der Daten und das entspechende Formatieren der Daten (in array, \n raus, ...)
#  4. Grafik für Euler-Angle

# global variables
toRad = 2 * np.pi / 360
toDeg = 1 / toRad


def readDataFromTXT():
    with open('bewegung.txt', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        next(csv_reader)
        next(csv_reader)

        array = list(csv_file)
        return array


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


# Main
def main():
    array = readDataFromTXT()
    theta = 0;
    phi = 0;
    for row in array:
        row = str(row)
        row = row.strip('\n')
        row = row.split(",")

        # row[0] = accx, row[1] = accy, row[2] = accz
        # row[3] = gyrox, row[4] = gyroy, row[5] = gyroz
        # row[6] = magx, row[7] = magy, row[8] = magz

        pitch = computePitchAngle(accx=row[0], accz=row[2], gyroy=row[4], thetaOld=theta, dt=0.001)
        theta = pitch

        roll = computeRollAngle(accy=row[1], accz=row[2], gyrox=row[3], phiOld=phi, dt=0.001)
        phi = roll

        yaw = computeYawAngle(theta=pitch, phi=roll, magx=row[6], magy=row[7], magz=row[8])
        print(pitch, roll, yaw)


if __name__ == "__main__":
    main()
