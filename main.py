import random
import timeit

from ursina import *  # import Ursina game engine
from ursina.shaders import lit_with_shadows_shader

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
DirectionalLight(y=2, z=3, shadows=True, rotation=(45, -45, 45))

Sky(texture='sky')
# Spieler evtl collider sphere??
player = Entity(model='Schiff', color=color.dark_gray, scale=(.2, .2, .2), rotation=(0, 180, 0), collider="box")
player.collider.visible = False

positions = [15, 0, -10, -200, -60, -100, 20, 30]
positionsH = [4,5,6]
asteroids = []
herzen  =[]
lebend = 3
Punktzahl = 0
for i in range(len(positions)):
    asteroid = Entity(model='Asteroid', color=color.light_gray,
                      collider="box", scale=(.5, .5, .5), rotation=(0, 0, 0),
                      position=(random.randint(-6, 6), random.randint(-5, 5), positions[i]))
    asteroids.append(asteroid)
    asteroid.collider.visible = False


# 1 und 2
def input(key):
    if held_keys['space']:
        print(player.rotation_x)
    if held_keys['1']:
        quit()
    if held_keys['2']:
        lebend = 3
        player.visible = True
        player.setPos(0, 0, 0)
        player.collider.setScale(1)


def update():
    # steuerung Spieler
    global lebend, herz2, herz1, herz0
    global Punktzahl
    wertSteuer = 4
    wert = 10
    max = 15
    player.rotation_x = 0
    player.rotation_z = 0

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
            Punktzahl += 1

    # kollision Spieler

    kollisionSp = player.intersects()
    if kollisionSp.hit:
        lebend -= 1

        print("kollision", kollisionSp.world_point)
        print(lebend)
        if lebend <= 0:
            player.visible = False
            explosion = Entity(model='sphere', color=color.red, scale=1, position=kollisionSp.world_point, shader = False)
            explosion.animate_scale(3, .3)
            destroy(explosion, delay=.3)

    for asteroid in asteroids:
        kollisionAs = asteroid.intersects()
        if kollisionAs.hit:
            asteroid.setPos(random.randint(-6, 6), random.randint(-6, 6), random.randint(30, 40))


    #Herzen

    for i in range(len(positionsH)):
        herz = Entity(model='Sphere', color=color.red,
                      scale=(.3, .3, .3), position=(positionsH[i], -3, -3))
        herzen.append(herz)
    if lebend == 2:
        herzen[2].visible = False
    if lebend == 1:
        herzen[1].visible = False
    if lebend == 0:
        herzen[0].visible = False




    #Punktzahl
    #Punktzahl = Text("Punktzahl:",y=.5,x=.6 )

    # Punktzahl

    Punktzahl_text = Text(text=f"Punktzahl: {Punktzahl}", y=.5, x=.6, eternal=True, ignore=False,i=0)
    #text_entity = Text('text' + str(Punktzahl))

    # wp = WindowPanel(content=text_entity, popup=True, enabled=False)
    # to update the text



app.run()


