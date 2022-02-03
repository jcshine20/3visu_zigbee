import random
import timeit

from ursina import *  # import Ursina game engine


class Asteroid(Entity):  # Klasse Asteroid
    def __init__(self, position=(0, 0, 0)):
        super().__init__(
            position=position,
            model='Asteroid', collider='Asteroid', scale=(1, 1, 1),
        )


app = Ursina()  # Initialisierung Ursina

# Fenster Einstellungen
window.title = 'Space Game'
window.borderless = True
window.exit_button.visible = True
window.fps_counter.enabled = True
window.fullscreen = False
toolbar = Text("1 = Ende, 2 = Neustart", y=.5, x=-.25)

Sky(texture='sky')
# Spieler evtl collider sphere??
player = Entity(model='Schiff', color=color.orange, scale=(.3, .3, .3), rotation=(0, 180, 0), collider="box")
player.collider.visible = True

positions = [15, 0, -10, -200, -60, -100]
asteroids = []
lebend = 2
Punktzahl = 0
highscore = 0
for i in range(len(positions)):
    asteroid = Entity(model='Asteroid', color=color.gray,
                      collider="sphere", scale=(.5, .5, .5), rotation=(0, 0, 0),
                      position=(random.randint(-6, 6), random.randint(-5, 5), positions[i]))
    asteroids.append(asteroid)
    asteroid.collider.visible = True

'''Points, Health Bar, HighScore'''
points_text = Text(text=f"Punktzahl: {Punktzahl}", y=.5, x=.6, eternal=True, ignore=False, i=0)
highscore_text = Text(text=f"Highscore: {highscore}", y=.47, x=.6, eternal=True, ignore=False, i=0)



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
    # player.rotation_x = 0
    # player.rotation_z = 0


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
    if kollisionSp.hit:
        lebend -= 1
        print("kollision", kollisionSp.world_point)
        print(lebend)
        if lebend <= 0:
            player.visible = False
            explosion = Entity(model='sphere', color=color.red, scale=1, position=kollisionSp.world_point)
            explosion.animate_scale(3, .3)
            destroy(explosion, delay=.3)
            if highscore < Punktzahl:
                highscore = Punktzahl

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