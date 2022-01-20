import timeit

from ursina import *                                                # import Ursina game engine





class Asteroid(Entity):                                             #Klasse Asteroid
    def __init__(self, position=(0,0,0)):
        super().__init__(
            position=position,
            model='Asteroid', collider= 'Asteroid', scale=(1,1,1),
        )

app=Ursina()                                                        #Initialisierung Ursina

#Fenster Einstellungen
window.title ='Space Game'
window.borderless = True
window.exit_button.visible = True
window.fps_counter.enabled = True
window.fullscreen = False
toolbar = Text("1 = Ende, 2 = Neustart", y=.5, x=-.25)

Sky(texture='sky')

#Spieler evtl collider sphere??
player = Entity(model='sphere', color=color.black, scale=(1,1,1), rotation=(0,180,0), collider='box')
player.collider.visible = True
lebend = True


positions = [10, 0, -10, -20, -60, -100]

#for i in range(len(positions)):
    #asteroid = Entity(model='Asteroid', color=color.gray, collider="box", scale=(.5, .5, .5), rotation=(0, 0, 0), position=(random.randint(-6, 6 ), random.randint(-6, 6), positions[0]))


asteroid0 = Entity(model='Asteroid1', collider="box", scale=(.5, .5, .5), rotation=(0, 0, 0), position=(random.randint(-6, 6), random.randint(-6, 6), positions[0]))
asteroid1 = Entity(model='Asteroid', color=color.gray, collider="sphere", scale=(.5, .5, .5), rotation=(0, 0, 0), position=(random.randint(-6, 6), random.randint(-6, 6), positions[1]))
asteroid2 = Entity(model='Asteroid', color=color.gray, collider="box", scale=(.5, .5, .5), rotation=(0, 0, 0), position=(random.randint(-6, 6), random.randint(-6, 6), positions[2]))
asteroid3 = Entity(model='Asteroid', color=color.gray, collider="box", scale=(.5, .5, .5), rotation=(0, 0, 0), position=(random.randint(-6, 6), random.randint(-6, 6), positions[3]))
asteroid4 = Entity(model='Asteroid', color=color.gray, collider="box", scale=(.5, .5, .5), rotation=(0, 0, 0), position=(random.randint(-6, 6), random.randint(-6, 6), positions[4]))
asteroid5 = Entity(model='Asteroid', color=color.gray, collider="box", scale=(.5, .5, .5), rotation=(0, 0, 0), position=(random.randint(-6, 6), random.randint(-6, 6), positions[5]))

asteroid0.collider.visible = True
asteroid1.collider.visible = True
asteroid2.collider.visible = True
asteroid3.collider.visible = True
asteroid4.collider.visible = True
asteroid5.collider.visible = True

def input (key):
    if held_keys['space']:
        print(player.rotation_x)
    if held_keys['1']:
        quit()
    if held_keys['2']:
        player.visible = True
        player.setPos(0,0,0)
        player.collider.setScale(1)
        global lebend
        lebend = True

def update():
    #steuerung Spieler
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


    #Asteroiden
    #for i in range(len(positions)):

        #asteroid.z -= wert * time.dt
        #asteroid.rotation_x -= 5
        #endpos = 25
        #if asteroid.z <= -2:
            #asteroid.setPos(random.randint(-6, 6), random.randint(-6, 6), endpos)
    asteroid0.z -= wert * time.dt
    asteroid0.rotation_x -= 5
    endpos = 25
    if asteroid0.z <= -2:
        asteroid0.setPos(random.randint(-6, 6), random.randint(-6, 6), endpos)
    asteroid1.z -= wert * time.dt
    asteroid1.rotation_x -= 5
    asteroid1.rotation_y -= 4
    endpos = 25
    if asteroid1.z <= -2:
        asteroid1.setPos(random.randint(-6,6), random.randint(-6,6), endpos)
    asteroid2.z -= wert * time.dt
    asteroid2.rotation_x -= 5
    asteroid2.rotation_y -= 1
    endpos = 25
    if asteroid2.z <= -2:
        asteroid2.setPos(random.randint(-6, 6), random.randint(-6, 6), endpos)
    asteroid3.z -= wert * time.dt
    asteroid3.rotation_x -= 5
    asteroid3.rotation_y += 2
    endpos = 25
    if asteroid3.z <= -2:
        asteroid3.setPos(random.randint(-6, 6), random.randint(-6, 6), endpos)
    asteroid4.z -= wert * time.dt
    asteroid4.rotation_x -= 5
    asteroid4.rotation_y += 6
    endpos = 25
    if asteroid4.z <= -2:
        asteroid4.setPos(random.randint(-6, 6), random.randint(-6, 6), endpos)
    asteroid5.z -= wert * time.dt
    asteroid5.rotation_x -= 5
    asteroid5.rotation_y += 3
    endpos = 25
    if asteroid5.z <= -2:
        asteroid5.setPos(random.randint(-6, 6), random.randint(-6, 6), endpos)

    #kollision
    kollision = player.intersects()
    if kollision.hit:
        global lebend
        while lebend == True:
            print("kollision")
            player.visible = False
            player.collider.setScale(0)
            explosion = Entity(model='sphere', color=color.red, scale=1, position=kollision.world_point)
            explosion.animate_scale(3,.3)
            destroy(explosion, delay=.3)
            lebend = False


    #Punktzahl
    #punktzahl



app.run()


