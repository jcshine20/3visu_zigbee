from vpython import *
from ComputationEulerAngles import *

# GLOBAL VARIABLES
toRad = 2 * np.pi / 360
toDeg = 1 / toRad


def createCanvas():
    return canvas(range=5, forward=vector(-1, -1, -1), width=600, height=600)


def createEulerGraph():
    gd = graph(title="3D Visualization", xtitle="<b>Time in s</b>", ytitle="Angels in Degrees",
               foreground=color.black, background=color.white, fast=False, scroll=True, xmin=0, xmax=5)
    pitchCurve = gdots(color=color.red, label="pitch")
    rollCurve = gdots(color=color.green, label="roll")
    yawCurve = gdots(color=color.blue, label="yaw")
    return gd, pitchCurve, rollCurve, yawCurve


def axisVis():
    """
    This function initializes the coordinates systems axis
    :return:
    """
    xArrow = arrow(axis=vector(1, 0, 0), length=4, shaftwidth=.1, color=color.red, opacity=0.5)
    yArrow = arrow(axis=vector(0, 1, 0), length=4, shaftwidth=.1, color=color.green, opacity=0.5)
    zArrow = arrow(axis=vector(0, 0, 1), length=4, shaftwidth=.1, color=color.blue, opacity=0.5)

    frontArrow = arrow(axis=vector(1, 0, 0), length=2, shaftwidth=.1, color=color.purple)
    upArrow = arrow(axis=vector(0, 1, 0), length=2, shaftwidth=.1, color=color.magenta)
    sideArrow = arrow(axis=vector(0, 0, 1), length=2, shaftwidth=.1, color=color.orange)

    return xArrow, yArrow, zArrow, frontArrow, upArrow, sideArrow


def sensorVis():
    """
    This function initialises and visualizes the whole sensor in 3D
    :return: compound of utilized 3D objects that displays the sensor
    """
    bno = box(length=1, width=.75, height=.1, pos=vector(0, 0, 0), color=color.blue)
    middleBoard1 = box(length=2, width=.75, height=.1, pos=vector(0.5, -0.5, 0), opacity=0.6, color=vector(0, 0.5, 0))
    middleBoard2 = box(length=1, width=.75, height=.1, pos=vector(0, -0.5, -0.75), opacity=0.6, color=vector(0, 0.5, 0))
    bottomBoard = box(width=2, length=2, height=.1, pos=vector(0.5, -1, 0), opacity=0.6, color=vector(0, 0.5, 0))

    vertical1 = box(length=.75, width=0.1, height=0.5 - 0.2, pos=vector(0, -0.25, 0), opacity=0.6, color=color.black)
    vertical2 = box(length=.5, width=0.1, height=0.5 - 0.1, pos=vector(0, -0.75, -0.75), opacity=0.6, color=color.black)
    vertical3 = box(length=.5, width=0.1, height=0.5 - 0.1, pos=vector(1.2, -0.75, 0.15), opacity=0.6,
                    color=color.black)

    yellowBox = box(length=0.3, width=0.3, height=0.4, pos=vector(0.5, -0.75, 0.75), opacity=0.6, color=color.yellow)
    bottomCylinder = cylinder(radius=0.15, axis=vector(0, 0.3, 0), pos=vector(0.5, -0.75 + 0.2, 0.75), opacity=0.6,
                              color=color.black)
    redCylinder1 = cylinder(radius=0.15, axis=vector(0, 0.05, 0), pos=vector(0.5, -0.75 + 0.2 + 0.3, 0.75), opacity=0.6,
                            color=color.red)
    middleCylinder = cylinder(radius=0.15, axis=vector(0, 0.05, 0), pos=vector(0.5, -0.75 + 0.2 + 0.3 + 0.05, 0.75),
                              opacity=0.6, color=color.black)
    redCylinder2 = cylinder(radius=0.15, axis=vector(0, 0.05, 0),
                            pos=vector(0.5, -0.75 + 0.2 + 0.3 + 0.05 + 0.05, 0.75), opacity=0.6, color=color.red)
    topCylinder = cylinder(radius=0.15, axis=vector(0, 0.3, 0),
                           pos=vector(0.5, -0.75 + 0.2 + 0.3 + 0.05 + 0.05 + 0.05, 0.75), opacity=0.6,
                           color=color.black)

    allObj = compound([bno, middleBoard1, middleBoard2, bottomBoard, vertical1, vertical2, vertical3,
                       yellowBox, bottomCylinder, redCylinder1, middleCylinder, redCylinder2, topCylinder],
                      origin=vector(bno.pos))

    return allObj


def visualizeQuaternion(row, frontArrowQuat, upArrowQuat, sideArrowQuat,
                        quaternionObj):
    """
    This function updates the 3D visualization of the sensor according to the data received
    :param row: values of current quaternion
    :param curves: list of curves for the 4 values of one quaternion
    :param frontArrowQuat:
    :param upArrowQuat:
    :param sideArrowQuat:
    :param quaternionObj:
    :return:
    """

    q0 = float(row[1])
    q1 = float(row[2])
    q2 = float(row[3])
    q3 = float(row[4])

    # Transformation quaternions into euler angels
    roll = -math.atan2(2 * (q0 * q1 + q2 * q3), 1 - 2 * (q1 * q1 + q2 * q2))
    pitch = math.asin(2 * (q0 * q2 - q3 * q1))
    yaw = -math.atan2(2 * (q0 * q3 + q1 * q2), 1 - 2 * (q2 * q2 + q3 * q3))  # - np.pi/2

    # Update Graph
    # curves[0].plot((q0, row[5]))
    # curves[1].plot((q1, row[5]))
    # curves[2].plot((q2, row[5]))
    # curves[3].plot((q3, row[5]))

    frontVector, upVectorRotated, sideVectorRotated = computeAxis(pitch, roll, yaw)

    frontArrowQuat.axis = frontVector
    frontArrowQuat.length = 2
    sideArrowQuat.axis = sideVectorRotated
    sideArrowQuat.length = 2
    upArrowQuat.axis = upVectorRotated
    upArrowQuat.length = 2

    quaternionObj.axis = frontVector
    quaternionObj.up = upVectorRotated


def visualizeEuler(row, frontArrowEuler, upArrowEuler, sideArrowEuler, eulerObj, deltaTime, phi, theta):
    """
    Computation of Euler Angles with help of sensor data
    """
    roll = computeRollAngle(accy=row[1], accz=row[2], gyrox=row[3], phiOld=phi, dt=0.050) * toRad
    pitch = computePitchAngle(accx=row[0], accz=row[2], gyroy=row[4], thetaOld=theta, dt=0.050) * toRad
    yaw = computeYawAngle(theta=pitch, phi=roll, magx=row[6], magy=row[7], magz=row[8]) * toRad

    phi = roll * toDeg
    theta = pitch * toDeg
    # print(pitch * toDeg, roll * toDeg, yaw * toDeg)

    '''
    Update Graphics
    '''
    # curves[0].plot(pos=(deltaTime, roll * toDeg))
    # curves[1].plot(pos=(deltaTime, pitch * toDeg))
    # curves[2].plot(pos=(deltaTime, yaw * toDeg))

    frontVector, upVectorRotated, sideVectorRotated = computeAxis(pitch, roll, yaw)

    frontArrowEuler.axis = frontVector
    frontArrowEuler.length = 2
    sideArrowEuler.axis = sideVectorRotated
    sideArrowEuler.length = 2
    upArrowEuler.axis = upVectorRotated
    upArrowEuler.length = 2

    eulerObj.axis = frontVector
    eulerObj.up = upVectorRotated

    deltaTime = deltaTime + 0.05

    return phi, theta, deltaTime


def computeAxis(pitch, roll, yaw):
    """
    This functions computes the new alignment body-fixed coordinate system of the sensor
    :param pitch: pitch angle in radians
    :param roll: roll angle in radians
    :param yaw: yaw angle in radians
    :return: vectors describing the new alignment of the body-fixed coordinate system axis
    """

    """
     Computation of new x,y,z coordinates of sensor with help of euler angles
    """
    frontVector = vector(cos(yaw) * cos(pitch), sin(pitch), sin(yaw) * cos(pitch))
    y = vector(0, 1, 0)
    sideVector = cross(frontVector, y)
    upVector = cross(sideVector, frontVector)

    '''
    Computation of y- and z-Axis because they are influenced by roll rotations
    '''
    upVectorRotated = upVector * cos(roll) + cross(frontVector, upVector) * sin(roll)
    sideVectorRotated = cross(frontVector, upVectorRotated)

    return frontVector, upVectorRotated, sideVectorRotated


def main():
    # '''Build up Graph for Euler Angels'''
    # gd, pitchCurve, rollCurve, yawCurve = createEulerGraph()
    # gd.align = "right"

    '''Build up Scene for Euler Angels'''
    scene = createCanvas()
    scene.title = "<b>3D Visualization Euler Angles</b>"
    # scene.align = "left"
    scene.append_to_caption('\n\n')
    xArrowEuler, yArrowEuler, zArrowEuler, frontArrowEuler, upArrowEuler, sideArrowEuler = axisVis()
    eulerObj = sensorVis()

    '''Build up Scene for Quaternions'''
    quaternionScene = createCanvas()
    quaternionScene.title = "<b>3D Visualization Quaternions</b>"
    quaternionScene.align = "left"
    quaternionScene.select()
    xArrowQuat, yArrowQuat, zArrowQuat, frontArrowQuat, upArrowQuat, sideArrowQuat = axisVis()
    quaternionObj = sensorVis()

    theta = 0
    phi = 0
    deltaTime = 0

    list = readDataFromTXT()
    for i in range(len(list)):
        dataPacket = str(list[i])
        dataPacket = dataPacket.strip('\n')
        list[i] = dataPacket
        # print(list[i])

    while True:
        for i in range(len(list)):
            rate(20)
            row = list[i].split(",")
            # print(row)
            if True:
                phi, theta, deltaTime = visualizeEuler(row, frontArrowEuler, upArrowEuler,
                                                       sideArrowEuler, eulerObj, deltaTime, phi, theta)
            else:
                try:
                    visualizeQuaternion(row, frontArrowQuat, upArrowQuat, sideArrowQuat,
                                        quaternionObj)
                except:
                    pass


if __name__ == "__main__":
    main()
