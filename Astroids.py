"""

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'                                                                    '     
'       #     #####  ####### ######  ####### ### ######   #####      ' 
'      # #   #     #    #    #     # #     #  #  #     # #     #     '
'     #   #  #          #    #     # #     #  #  #     # #           '
'    #     #  #####     #    ######  #     #  #  #     #  #####      '
'    #######       #    #    #   #   #     #  #  #     #       #     '
'    #     # #     #    #    #    #  #     #  #  #     # #     #     '
'    #     #  #####     #    #     # ####### ### ######   #####      '
'                                                                    '     
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

LOAD GAME IN BROWSER:
    Open the link below and run it (first button)
    http://www.codeskulptor.org/#user38_BwfKxjSzbo9UwxW_0.py
    note - Please use google chrome
    
HOW TO PLAY:
    UP 		- accelerate spacecraft
    RIGHT 	- rotate scpacecraft anti-clockwise
    LEFT 	- rotate spcarecraft clockwise
    SPACE 	- shoot missile    

AUTHOR:
    Name 		- Adesh Shah
    LinkedIn	- linkedin.com/in/adeshshah/
    Email		- Adesh [dot] Shah [dot] 28 [at] gmail [dot] com
    
TEST:    
    Completed 	- 10NOV2014
    Python		- 2.6
    Tested in 	- Google Chrome 38.0.2125.111 m

"""

# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated
    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 100)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 6.28/60
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
        self.acc  = [0,0]
        self.rotate = False
        self.rotate_direction = 1
        self.ship_img_thruster_center = [self.image_center[0]+90, self.image_center[0]]
        
    def draw(self,canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "White", "White")
        if self.thrust == True:
            canvas.draw_image(self.image, self.ship_img_thruster_center, self.image_size, self.pos, self.image_size, self.angle)
        elif self.thrust == False:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
            
    def update(self):
        if self.thrust == True:        
            for i in range(len(self.acc)):
                self.acc[i] += 0.05*angle_to_vector(self.angle)[i]
        elif self.thrust == False:
            for i in range(len(self.acc)):
                self.acc[i] = 0	
        
        for i in range(len(self.vel)):
            self.vel[i] += self.acc[i]
            self.vel[i] *= 0.9			#friction
            self.pos[i] += self.vel[i]
            
        self.pos[0] = (self.pos[0])%WIDTH
        self.pos[1] = (self.pos[1])%HEIGHT            
            
        if self.rotate == True:
            if self.rotate_direction == 1:
                self.angle += self.angle_vel
            elif self.rotate_direction == -1:
                self.angle -= self.angle_vel      
    
    def rotateShip(self,direction):
        if direction == 1:
            self.rotate = True
            self.rotate_direction = 1  
        elif direction == -1:
            self.rotate = True
            self.rotate_direction = -1
        elif direction == 0:
            self.rotate = False
    
    def thrusters(self, on):
        if on == 1:
            self.thrust = True
        elif on == 0:
            self.thrust = False
    
    def shoot(self):#35 is ship radius
        global missile_group
        a_missile_pos = [self.pos[0] + 35*angle_to_vector(self.angle)[0], self.pos[1] + 35*angle_to_vector(self.angle)[1]] 
        a_missile_vel = [self.vel[0] + angle_to_vector(self.angle)[0]*2.5, self.vel[1] + angle_to_vector(self.angle)[1]*2.5]       
        missile_group.add( Sprite(a_missile_pos, a_missile_vel, 0, 0, missile_image, missile_info, missile_sound) )
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius  
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
        
    def draw(self, canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "Red", "Red")
        if self.animated == True:
            image_location = (self.image_center[0] + self.image_size[0] * self.age, self.image_center[1])
            canvas.draw_image(self.image, image_location, self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
            
    def update(self):
        for i in range(len(self.vel)):
            self.pos[i] += self.vel[i]
        
        self.pos[0] = (self.pos[0])%WIDTH
        self.pos[1] = (self.pos[1])%HEIGHT          
        self.angle = (self.angle + self.angle_vel)%6.14
        
        self.age = self.age + 1
        if self.age >= self.lifespan:
            return False
        else:
            return True
   
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius    

    def collide(self,other_object):
        if dist(self.get_position(), other_object.get_position()) <= (self.get_radius() + other_object.get_radius()):
            return True
        else:
            return False
        
def draw(canvas):
    global time, started, lives, score
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    
    canvas.draw_text('Score: '+ str(score), (WIDTH-90, 20), 20, 'White')
    canvas.draw_text('Life: '+ str(lives), (10, 20), 20, 'White')
    
    my_ship.draw(canvas)
    my_ship.update()
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
    
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())

    if group_collide(rock_group, my_ship) == True:
        lives -= 1

    missiles_collided_with_rocks = group_group_collide(missile_group, rock_group)
    score += missiles_collided_with_rocks
    
    if lives<1:
        started = False
        #set.clear() is not there in python 2.6 so a way arround for that below
        for a_rock in set(rock_group):
            rock_group.remove(a_rock)
    
#hanlder group_collide
def group_collide(group, other_object):
    global explosion_group
    result = False
    for a_thing in set(group):
        if a_thing.collide(other_object) == True:
            explosion_group.add(Sprite(a_thing.get_position(), [0,0], 0, 0, explosion_image, explosion_info, explosion_sound))
            group.remove(a_thing)
            result = True
    return result

#missile_group, rock_group
def group_group_collide(group1, group2):
    missiles_collided_with_rocks = 0
    for a_thing_of_g1 in set(group1):
        if group_collide(group2, a_thing_of_g1) == True:
            missiles_collided_with_rocks += 1
            group1.discard(a_thing_of_g1)
    return missiles_collided_with_rocks
    
#hanlder for rocks update and draw
def process_sprite_group(group,canvas):
    for a_thing in group:
        a_thing.draw(canvas)
    for a_thing in set(group):
        if a_thing.update() == False:
        #remove item from list
            group.remove(a_thing)
    
# timer handler that spawns a rock    
def rock_spawner():
    #Make sure you generated rocks that spin in both directions.
    #global a_rock
    if started == True:
        global rock_group
        dir_array = [-1, 1]
        random.shuffle(dir_array)
        if len(rock_group) < 13:
            #When you spawn rocks, you want to make sure they are some distance away from the ship. Otherwise, you can die when a rock spawns on top of you, which isn't much fun. One simple way to achieve this effect to ignore a rock spawn event if the spawned rock is too close to the ship
            temp_pos = [ my_ship.get_position()[0] + 2*my_ship.get_radius() + random.randrange(0, WIDTH/4), my_ship.get_position()[1] + 2*my_ship.get_radius() + random.randrange(0, HEIGHT/4) ]
            #Experiment with varying the velocity of rocks based on the score to make game play more difficult as the game progresses
            temp_vel = [0,0]
            if score<10:
                temp_vel = [random.randrange(-2, 2) , random.randrange(-1, 1)]
            elif score>=10 and score<30:
                temp_vel = [random.randrange(-3, 3) , random.randrange(-2, 2)]
            elif score>=30 and score<50:
                temp_vel = [random.randrange(-4, 4) , random.randrange(-4, 4)]
            elif score>=50:
                temp_vel = [random.randrange(-5, 5) , random.randrange(-5, 5)]
            rock_group.add( Sprite(temp_pos, temp_vel, 0, dir_array[0]*6.14/random.randrange(30, 120), asteroid_image, asteroid_info) )
    
#keyboard handlder
#key_dictionary = {"up":, "down":func2, "left":func3, "right":func4}
def keydown(key):
    global my_ship
    if key == simplegui.KEY_MAP['left']:    
        my_ship.rotateShip(-1)
    elif key == simplegui.KEY_MAP['right']:    
        my_ship.rotateShip(1)
    elif key == simplegui.KEY_MAP['up']:
        my_ship.thrusters(1)
        ship_thrust_sound.play()
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
        missile_sound.rewind()
        missile_sound.play()        
        
def keyup(key):
    global my_ship
    if key == simplegui.KEY_MAP['left'] or key == simplegui.KEY_MAP['right']:    
        my_ship.rotateShip(0)
    elif key == simplegui.KEY_MAP['up']:
        my_ship.thrusters(0)
        ship_thrust_sound.rewind()

# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, lives, score
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:        
        started = True
        lives = 3 
        score = 0
        soundtrack.rewind()
        soundtrack.play()
        
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
