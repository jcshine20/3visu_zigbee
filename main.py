import random
import timeit

import serial
from ursina import *  # import Ursina game engine
from ursina.shaders import lit_with_shadows_shader
from computation import transformQuatEuler


class Asteroid(Entity):  # Klasse Asteroid
    def __init__(self, position=(0, 0, 0)):
        super().__init__(
            position=position,
            model='Asteroid', collider='Asteroid', scale=(1, 1, 1),
        )

# Class for Explosion
class Explosion(Entity):
    def __init__(self, x, y, z):
        super().__init__()
        self.x = x
        self.y = y
        self.z = z
        self.dx = random.randint(-2, 2) / 50    # speed of how x coordinate changes
        self.dy = random.randint(-2, 2) / 50    # speed of how y coordinate changes
        self.dz = random.randint(-2, 2) / 50    # speed of how z coordinate changes
        self.rx = random.randint(-5, 5)         # speed of x rotation
        self.ry = random.randint(-5, 5)         # speed of y rotation
        self.rz = random.randint(-5, 5)         # speed of z rotation
        self.ds = random.randint(1, 3) / 150    # speed of how scale changes

        j = random.randint(0,9)
        if (j % 3) == 0:                        # 40% mini-asteroids, 60% red spheres
            self.color = color.gray
            self.model = 'Asteroid'
            self.scale = 0.2
        else:
            self.color = color.red
            self.model = 'sphere'
            self.scale = 0.4

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.z += self.dz
        self.rotation_x += self.rx
        self.rotation_y += self.ry
        self.rotation_z += self.rz
        self.scale -= self.ds
        if self.scale <= 0.005:
            destroy(self)


def createExplosion(vec):
    num = 9
    x = vec.x
    y = vec.y
    z = vec.z
    e = [None] * num
    for count in range(num):
        e[count] = Explosion(x, y, z)


com = "com7"
Data = serial.Serial(com, 115200)  # arduino anpassen!!!!

app = Ursina()  # Initialisierung Ursina

# Fenster Einstellungen
window.title = 'Space Game'
window.borderless = True
window.exit_button.visible = True
window.fps_counter.enabled = True
window.fullscreen = False
toolbar = Text("1 = Ende, 2 = Neustart", y=.5, x=-.25)
DirectionalLight(y=2, z=3, shadows=True, rotation=(45, -45, 45))

Sky(texture='sky')
# Spieler evtl collider sphere??
player = Entity(model='Schiff', color=color.dark_gray, scale=(.2, .2, .2), rotation=(0, 180, 0), collider="box")
player.collider.visible = False

positions = [15, 0, -10, -200, -60, -100]
positionsH = [4, 5, 6]
asteroids = []
herzen = []
lebend = 2
Punktzahl = 0
highscore = 0
for i in range(len(positions)):
    asteroid = Entity(model='Asteroid', color=color.gray,
                      collider="box", scale=(.5, .5, .5), rotation=(0, 0, 0),
                      shader=lit_with_shadows_shader,
                      position=(random.randint(-6, 6), random.randint(-5, 5), positions[i]))
    asteroids.append(asteroid)
    asteroid.collider.visible = False

'''Points, Health Bar, HighScore'''
gamefont = 'fonts/Pixeboy-z8XGD.ttf'
points_text = Text(text=f"Punktzahl: {Punktzahl}", y=.5, x=.6, scale=1.5, eternal=True, ignore=False, i=0,
                   font=gamefont)
highscore_text = Text(text=f"Highscore: {highscore}", y=.47, x=.6, scale=1.5, eternal=True, ignore=False, i=0,
                      font=gamefont)

'''Leben'''
for i in range(len(positionsH)):
    herz = Entity(model='Sphere', color=color.red,
                  scale=(.3, .3, .3), position=(positionsH[i], -3, -3))
    herzen.append(herz)


# 1 und 2
def input(key):
    if held_keys['space']:
        print(player.rotation_x)
    if held_keys['1']:
        quit()
    if held_keys['2']:
        global lebend
        global Punktzahl
        lebend = 2
        Punktzahl = 0
        player.visible = True
        player.setPos(0, 0, 0)
        player.collider.setScale(1)
        for i in range(len(positionsH)):
            herzen[i].visible = True
        # herzen[0].visible = True
        # herzen[1].visible = True
        # herzen[2].visible = True


def update():
    # steuerung Spieler
    global lebend
    global Punktzahl
    global highscore
    global roll
    global pitch
    wertSteuer = 4
    wert = 10
    max = 15

    # if increment < len(list):
    #     row = list[increment].split(",")
    #     increment += 1
    #
    #     roll = computeRollAngle(accy=row[1], accz=row[2], gyrox=row[3], phiOld=roll, dt=0.050)
    #     player.rotation_z =  roll
    #
    #     pitch = computePitchAngle(accx=row[0], accz=row[2], gyroy=row[4], thetaOld=pitch, dt=0.050)
    #     player.rotation_x = pitch
    #
    #     if roll >= 20:
    #         player.x += -wertSteuer * time.dt
    #     if roll <=-20:
    #         player.x += wertSteuer * time.dt
    #     if pitch >= 20:
    #         player.y += wertSteuer * time.dt
    #     if pitch <= -20:
    #         player.y += -wertSteuer * time.dt
    #
    # else:
    #     increment = 0
    #     player.setPos(0,0,0)
    #     print("List durch")
    #
    #
    #

    while (Data.inWaiting() == 0):
        #sleep(0.001)
        pass
    dataPacket = Data.readline()
    dataPacket = str(dataPacket, 'utf-8')
    dataPacket = dataPacket.strip('\r\n')
    splitPacket = dataPacket.split(",")
    row = splitPacket

    if int(splitPacket[0]) == 1:
        q0 = float(row[1])
        q1 = float(row[2])
        q2 = float(row[3])
        q3 = float(row[4])
        roll, pitch, yaw = transformQuatEuler(q0, q1, q2, q3)

    player.rotation_x = 0
    player.rotation_z = 0

    if roll >= 20:
        player.x += -wertSteuer * time.dt
        player.rotation_z = roll
    if roll <=-20:
        player.x += wertSteuer * time.dt
        player.rotation_z = roll
    if pitch >= 20:
        player.y += wertSteuer * time.dt
        player.rotation_x = pitch
    if pitch <= -20:
        player.y += -wertSteuer * time.dt
        player.rotation_x = pitch

    if held_keys['w']:
        player.y += wertSteuer * time.dt
        player.rotation_x = max
    if held_keys['s']:
        player.y += -wertSteuer * time.dt
        player.rotation_x = -max
    if held_keys['d']:
        player.x += wertSteuer * time.dt
        player.rotation_z = -max
    if held_keys['a']:
        player.x += -wertSteuer * time.dt
        player.rotation_z = max
    while player.y >= 5:
        player.y -= 1
    while player.y <= -5:
        player.y += 1
    while player.x >= 6:
        player.x -= 1
    while player.x <= -6:
        player.x += 1

    for asteroid in asteroids:
        asteroid.z -= wert * time.dt
        asteroid.rotation_x -= random.randint(3, 6)
        asteroid.rotation_y -= random.randint(2, 8)
        if asteroid.z <= -2:
            asteroid.setPos(x=random.randint(-6, 6), y=random.randint(-5, 5), z=random.randint(30, 40))
            if lebend > 0:
                Punktzahl += 1
            else:
                Punktzahl = Punktzahl

    # kollision Spieler

    kollisionSp = player.intersects()
    # temp = kollisionSp.entity
    if kollisionSp.hit:
        lebend -= 1
        print("kollision", kollisionSp.world_point)
        print(lebend)
        if lebend <= 0:
            player.visible = False
            # explosion = Entity(model='sphere', color=color.red, scale=1, position=kollisionSp.world_point)
            # explosion.animate_scale(3, .3)
            # destroy(explosion, delay=.3)
            createExplosion(kollisionSp.world_point)
            if highscore < Punktzahl:
                highscore = Punktzahl

    '''Leben wird weniger'''
    if lebend == 2:
        herzen[2].visible = False
    if lebend == 1:
        herzen[1].visible = False
    if lebend == 0:
        herzen[0].visible = False

    for asteroid in asteroids:
        kollisionAs = asteroid.intersects()
        if kollisionAs.hit:
            asteroid.setPos(random.randint(-6, 6), random.randint(-6, 6), random.randint(30, 40))
        # if lebend <= 0:
        #     player.visible = False
        #     explosion = Entity(model='sphere', color=color.red, scale=1, position=kollisionSp.world_point)
        #     explosion.animate_scale(3,.3)
        #     destroy(explosion, delay=.3)

    destroy(points_text)
    points_text.text = f"Punktzahl: {Punktzahl}"

    destroy(highscore_text)
    highscore_text.text = f"Highscore: {highscore}"


app.run()
