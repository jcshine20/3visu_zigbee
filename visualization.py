from vpython import *
from ComputationEulerAngles import *

# GLOBAL VARIABLES
toRad = 2 * np.pi / 360
toDeg = 1 / toRad

# scene.range = 5
# scene.forward = vector(-1, -1, -1)
# scene.width = 600
# scene.height = 600
# scene.title = "<b>3D Visualization Euler Angles</b>"

def createCanvas():
    return canvas(range = 5, forward = vector(-1,-1,-1), width = 600, height = 600)

def createEulerGraph():
    gd = graph(title="3D Visualization", xtitle="<b>Time in s</b>", ytitle="Angels in Degrees",
               foreground=color.black, background=color.white, fast=False)
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


def main():
    '''Build up Graph for Euler Angels'''
    gd, pitchCurve, rollCurve, yawCurve = createEulerGraph()
    gd.align = "right"

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


    # gd, pitchCurve, rollCurve, yawCurve = createEulerGraph()


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
            """
            Computation of Euler Angles with help of sensor data
            """
            row = list[i].split(",")
            roll = computeRollAngle(accy=row[1], accz=row[2], gyrox=row[3], phiOld=phi, dt=0.050) * toRad
            pitch = computePitchAngle(accx=row[0], accz=row[2], gyroy=row[4], thetaOld=theta, dt=0.050) * toRad
            yaw = computeYawAngle(theta=pitch, phi=roll, magx=row[6], magy=row[7], magz=row[8]) * toRad
            theta = pitch * toDeg
            phi = roll * toDeg
            # print(pitch * toDeg, roll * toDeg, yaw * toDeg)

            '''
            Update Graphics
            '''
            pitchCurve.plot(pos=(deltaTime, theta))
            rollCurve.plot(pos=(deltaTime, phi))
            yawCurve.plot(pos=(deltaTime, yaw * toDeg))

            rate(20)
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

            frontArrowEuler.axis = frontVector
            frontArrowEuler.length = 2
            sideArrowEuler.axis = sideVectorRotated
            sideArrowEuler.length = 2
            upArrowEuler.axis = upVectorRotated
            upArrowEuler.length = 2

            eulerObj.axis = frontVector
            eulerObj.up = upVectorRotated

            deltaTime = deltaTime + 0.05

if __name__ == "__main__":
    main()
