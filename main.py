import random
import time
import timeit
import datetime
import serial
import database
from ursina import *  # import Ursina game engine
from ursina.shaders import lit_with_shadows_shader
from computation import transformQuatEuler
from computation import *
from configparser import ConfigParser

class Asteroid(Entity):  # Klasse Asteroid
    def __init__(self, position=(0, 0, 0)):
        super().__init__(
            position=position,
            model='Asteroid',
            collider="box",
            color=color.dark_gray,
            scale=(.5, .5, .5),
            rotation=(0, 0, 0),
            shader=lit_with_shadows_shader
        )


# Class for Explosion
class Explosion(Entity):
    def __init__(self, x, y, z):
        super().__init__()
        self.x = x
        self.y = y
        self.z = z
        self.dx = random.randint(-2, 2) / 50  # speed of how x coordinate changes
        self.dy = random.randint(-2, 2) / 50  # speed of how y coordinate changes
        self.dz = random.randint(-2, 2) / 50  # speed of how z coordinate changes
        self.rx = random.randint(-5, 5)  # speed of x rotation
        self.ry = random.randint(-5, 5)  # speed of y rotation
        self.rz = random.randint(-5, 5)  # speed of z rotation
        self.ds = random.randint(1, 3) / 150  # speed of how scale changes

        if player.leben <= 0:
        # if lebend <= 0:
            j = random.randint(0, 9)
            if (j % 3) == 0:  # 40% mini-asteroids, 60% red spheres
                self.color = color.gray
                self.model = 'Asteroid'
                self.scale = 0.2
                self.shader = shader=lit_with_shadows_shader
            else:
                self.color = color.red
                self.model = 'sphere'
                self.scale = 0.4
        else:
            self.model = 'Asteroid'
            self.scale = 0.25
            self.color = color.gray
            self.shader = shader = lit_with_shadows_shader

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


class EndMenu(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
            model = 'quad',
            scale = (.6, .8),
            origin = (0,0),
            position = (0,0),
            texture = 'white_cube',
            # texture_scale=(5, 8),
            color=color.rgb(0,0,0,200)
        )

class Player(Entity):
    def __init__(self):
        super().__init__(
            model='Schiff',
            color=color.dark_gray,
            scale=(.2, .2, .2),
            rotation=(0, 180, 0),
            collider="box"
        )
        self.leben=3
        self.schild=0
        self.punktzahl=0
        self.highscore=0
        self.collision_time=0
    def toggleColour(self):
        self.color = color.red

def createExplosion(vec, num):
    x = vec.x
    y = vec.y
    z = vec.z
    e = [None] * num
    for count in range(num):
        e[count] = Explosion(x, y, z)

class Schild(Entity):
    def __init__(self, position=(0,0,0),scale=(.03, .03, .03),):
        super().__init__(
            position=position,
            model='Schild',
            collider="box",
            scale=(scale),
            rotation=(0,70,0) ,
            color=color.yellow,
        )


class Stern(Entity):
    def __init__(self, position=(0,0,0)):
        super().__init__(
            position=position,
            model='Stern',
            collider="box",
            scale=(.7, .7, .7),
            color=color.random_color(),
        )




def createEndMenu(highscore):
    endMenu = EndMenu()
    if player.highscore > player.punktzahl:
        Text(text=f"Your Score is {player.punktzahl}", parent=endMenu, position=(0, .25), origin=(0, 0),
                               scale=3, font=gamefont, background=True, visible=True)
    else:
        Text(text=f"Your Score is {player.punktzahl}\nNew Highscore !", parent=endMenu, position=(0, .25), origin=(0, 0),
                               scale=3, font=gamefont, background=True, visible=True)
    Text(text="Press 2\nto play again", parent=endMenu, position=(-0.15, -0.25), origin=(0,0), scale=3, font=gamefont,
         background=False, visible=True)


    return endMenu

file = 'config.ini'
config = ConfigParser()
config.read(file)
com = config["comport"]["port"]
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

# Sky(texture='sky')
Entity(model ='quad', texture="images\space.jpg", scale = (100,50), double_sided = True, position=(0,0,100))
player = Player()
player.collider.visible = False

amounts = dict(easy=1, medium=2, hard=4, very_hard=6)
amount = config["user"]["difficulty"]
positions = [15, 0, -10, -200, -60, -100]
positionsH = [4, 5, 6]

datadict = dict(beschl_x=[], beschl_y=[], beschl_z=[],
                gyro_x=[], gyro_y=[], gyro_z=[],
                mag_x=[], mag_y=[], mag_z=[], time=[])
quater_dict = dict(q0=[], q1=[], q2=[], q3=[], time=[])

for entry in range(amounts[amount]):
    if entry % 2 == 0:
        pos = random.randint(-200, -100)
    else:
        pos = random.randint(100, 200)
    if pos not in positions:
        positions.append(pos)

asteroids = []
herzen = []
schilder = []
stars = []
lebend = 2
schildAnz = 0
starAnz = 0
Punktzahl = 0
highscore = 0
roll = 0
pitch = 0
yaw = 0
toRad = 2 * np.pi / 360
toDeg = 1 / toRad
for i in range(len(positions)):
    asteroid = Asteroid(position=(random.randint(-6, 6), random.randint(-5, 5), positions[i]))
    asteroids.append(asteroid)
    asteroid.collider.visible = False

'''Points, Health Bar, HighScore'''
gamefont = 'fonts/Pixeboy-z8XGD.ttf'
points_text = Text(text=f"Punktzahl: {player.punktzahl}", y=.5, x=.6, scale=1.5, eternal=True, ignore=False, i=0,
                   font=gamefont)
highscore_text = Text(text=f"Highscore: {player.highscore}", y=.47, x=.6, scale=1.5, eternal=True, ignore=False, i=0,
                      font=gamefont)
endMenu = None


'''Audio'''
collision_audio = Audio('audio\mixkit-short-explosion-1694.wav', loop=False, autoplay=False)
dead_audio = Audio('audio\mixkit-system-break-2942.wav', loop=False, autoplay=False)
star_audio = Audio('audio\mixkit-space-coin-win-notification-271.wav', loop=False, autoplay=False)
shield_down = Audio('audio\mixkit-tech-break-fail-2947.wav', loop=False, autoplay=False)
shield_collect = Audio('audio\mixkit-achievement-completed-2068.wav', loop=False, autoplay=False)
sound = Audio('audio\mixkit-1980-290.mp3',loop=True, autoplay=True, volume=0.1)


'''Leben'''
for i in range(len(positionsH)):
    herz = Entity(model='Herz', color=color.red,
                  scale=(.1, .1, .1), position=(positionsH[i], -3, -3), rotation=(3,-10,0))
    herzen.append(herz)

'''Schild'''
shield = Schild(position=(3,-3,-3),scale=(.02, .02, .02))
shield.visible = False


# 1 und 2
def input(key):
    if held_keys['space']:
        print(player.rotation_x)
    if held_keys['1']:
        quit()
    if held_keys['2']:
        player.leben = 3
        player.punktzahl = 0
        player.visible = True
        player.setPos(0, 0, 0)
        player.collider.setScale(1)
        for i in range(len(positionsH)):
            herzen[i].visible = True
        destroy(endMenu)



def update():
    # steuerung Spieler
    global lebend
    global Punktzahl
    global highscore
    global roll
    global pitch
    global endMenu
    global schildAnz
    global starAnz
    wertSteuer = 4
    speeds = dict(easy=10, medium=15, hard=20, very_hard=25)
    speed = speeds[f'{config["user"]["difficulty"]}']
    max = 15

    try:

        while (Data.inWaiting() == 0):
            # sleep(0.001)
            pass
        dataPacket = Data.readline()
        dataPacket = str(dataPacket, 'utf-8')
        dataPacket = dataPacket.strip('\r\n')
        splitPacket = dataPacket.split(",")
        row = splitPacket

        if int(splitPacket[0]) == 1:
            # quaterionen
            q0 = float(row[1])
            q1 = float(row[2])
            q2 = float(row[3])
            q3 = float(row[4])
            try:
                quater_dict["q0"].append(q0)
                quater_dict["q1"].append(q1)
                quater_dict["q2"].append(q2)
                quater_dict["q3"].append(q3)
                quater_dict["time"].append(datetime.datetime.now().replace(microsecond=0))
                if len(quater_dict["time"]) >= 60:
                    database.insert_quater(quater_dict)
                    for key in quater_dict.keys():
                        quater_dict[key].clear()
            except:
                print("?????????????????????")
            roll, pitch, yaw = transformQuatEuler(q0, q1, q2, q3)
            roll = -(roll * toDeg)
            pitch = pitch * toDeg

        elif int(splitPacket[0]) == 0:
            try:
                relevant = splitPacket[1:10]
                datadict["beschl_x"].append(relevant[0])
                datadict["beschl_y"].append(relevant[1])
                datadict["beschl_z"].append(relevant[2])
                datadict["gyro_x"].append(relevant[3])
                datadict["gyro_y"].append(relevant[4])
                datadict["gyro_z"].append(relevant[5])
                datadict["mag_x"].append(relevant[6])
                datadict["mag_y"].append(relevant[7])
                datadict["mag_z"].append(relevant[8])
                datadict["time"].append(datetime.datetime.now().replace(microsecond=0))
                if len(datadict["time"]) >= 60:
                    database.insert_data(datadict)
                    for key in datadict.keys():
                        datadict[key].clear()
            except:
                print("!!!!!!!!!!!!!!!!!!")
    except:
        pass

    player.rotation_x = 0
    player.rotation_z = 0

    if roll >= 20:
        player.x += -wertSteuer * time.dt
        player.rotation_z = roll
    if roll <= -20:
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
        asteroid.z -= speed * time.dt
        asteroid.rotation_x -= random.randint(3, 6)
        asteroid.rotation_y -= random.randint(2, 8)
        if asteroid.z <= -2:
            asteroid.setPos(x=random.randint(-6, 6), y=random.randint(-5, 5), z=random.randint(30, 40))
            # if lebend > 0:
            if player.leben > 0:
                player.punktzahl += 1
            else:
                player.punktzahl = player.punktzahl

    # kollision Spieler

    kollisionSp = player.intersects()
    if isinstance(kollisionSp.entity, Asteroid):
        if (player.leben > 0) & (player.schild < 1) :
            player.leben -= 1
            print("kollision", kollisionSp.world_point)
            print(player.leben)
            if player.leben <= 0:
                player.visible = False
                createExplosion(kollisionSp.world_point, 9)
                dead_audio.play()
                # global endMenu
                endMenu = createEndMenu(player.highscore)
                player.position = (0,0,-5)
                if player.highscore < player.punktzahl:
                    player.highscore = player.punktzahl
            else:
                createExplosion(kollisionSp.world_point, 4)
                player.collision_time = time.time()
                s1=Sequence(0, Func(player.blink, duration=.5), loop=False)
                s1.start()
                collision_audio.play()
                # EditorCamera()
                # if lebend <= 0:d
        else:
            player.schild -= 1
            shield_down.play()
            print(player.schild)
            #schild.visible = False

    if isinstance(kollisionSp.entity, Schild):
        if player.schild < 1:
            player.schild += 1
            shield_collect.play()

    if isinstance(kollisionSp.entity, Stern):
        player.punktzahl += 20




    '''Leben wird weniger'''
    if player.leben == 2:
        herzen[2].visible = False
    if player.leben == 1:
        herzen[1].visible = False
    if player.leben == 0:
        herzen[0].visible = False

    'Asteroid'
    for asteroid in asteroids:
        kollisionAs = asteroid.intersects()
        if kollisionAs.hit:
            asteroid.setPos(random.randint(-6, 6), random.randint(-6, 6), random.randint(30, 40))

    destroy(points_text)
    points_text.text = f"Punktzahl: {player.punktzahl}"

    destroy(highscore_text)
    highscore_text.text = f"Highscore: {player.highscore}"

    'Stern'
    if(player.punktzahl) >= starAnz * 70 + 70:
        star = Stern(position=(random.randint(-6, 6), random.randint(-5, 5), 50))
        stars.append(star)
        starAnz += 1
    for star in stars:
        star.z -= speed *time.dt
        star.rotation_y += 3
        kollisionSt = star.intersects()
        if kollisionSt.hit:
            star_audio.play()
            star.disable()


    'Schild'
    if (player.punktzahl) >= schildAnz * 60 + 60:
        schild = Schild(position=(random.randint(-6, 6), random.randint(-5, 5), 50))
        schilder.append(schild)
        schildAnz += 1
    for schild in schilder:
        schild.z -= speed * time.dt
        schild.rotation_y -= 4
    if player.schild == 1:
        shield.visible = True
    if player.schild == 0:
        shield.visible = False


app.run()
