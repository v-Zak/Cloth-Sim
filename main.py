import pygame
import math
pygame.init()
run = True

width = 1500
height = 800
pointSpacing = 50
size = width,height
screen = pygame.display.set_mode(size)
fpsFont = pygame.font.SysFont('Comic Sans MS', 30)
clock = pygame.time.Clock()

def update(dt, gravity, friction, bounce, width, height):
    for i in range(len(points)):
        points[i].update(dt, gravity, friction, bounce)

    #iterate over to make the length of each stick more accurate
    for j in range(3):
        for i in range(len(sticks)):
            sticks[i].update()

        for i in range(len(points)):
            points[i].constrain(friction, width, height)


def draw():
    screen.fill((0,0,0))
    for i in range(len(points)):
        points[i].draw()
    
    for i in range(len(sticks)):
        sticks[i].draw()

class Point:
    def __init__(self, position):
        self.position = position.copy()
        self.previousPosition = position.copy()
        self.colour = [255,255,255]
        self.radius = 5
        self.pinned = False

    def pin(self):
        self.pinned = True
        self.colour = [255,0,0]

    def constrain(self, friction, width, height):
        if not self.pinned:
            p = self.position
            prevP = self.previousPosition
            velocity = p.sub(prevP)
            velocity = velocity.multiply(friction)            
            if p.x > width:
                p.x = width
                prevP.x = p.x + velocity.x * bounce
            elif p.x < 0:
                p.x = 0
                prevP.x = p.x + velocity.x * bounce
            if p.y > height:
                p.y = height
                prevP.y = p.y + velocity.y * bounce
            elif p.y < 0:
                p.y = 0
                prevP.y = p.y + velocity.y * bounce
    
    def update(self, dt, gravity, friction, bounce):
        if not self.pinned:
            velocity = self.position.sub(self.previousPosition)
            velocity = velocity.multiply(friction)
            self.previousPosition = self.position.copy()
            self.position = self.position.add(velocity)
            self.position = self.position.add(gravity)

    def draw(self):
        p = (self.position.x, self.position.y)
        pygame.draw.circle(screen, self.colour, p, self.radius, 1)

class Stick:
    def __init__(self, p0, p1):
        self.p0 = p0
        self.p1 = p1
        self.length = p0.position.distance(p1.position)
        self.colour = [255,255,255]

    def update(self):
        #ensure sticks are same length as when initiated
        dx = self.p1.position.x - self.p0.position.x
        dy = self.p1.position.y - self.p0.position.y
        currentLength = math.sqrt(dx * dx + dy * dy)
        difference = self.length - currentLength
        # / 2 because we want half the change to correct each point
        percent = (difference / currentLength) / 2
        offsetX = dx * percent
        offsetY = dy * percent
        #check if pinned before moving points then apply offset away from centre of stick
        if not self.p0.pinned:
            self.p0.position.x -= offsetX
            self.p0.position.y -= offsetY
        if not self.p1.pinned:
            self.p1.position.x += offsetX
            self.p1.position.y += offsetY


    def draw(self):
        p0 = (self.p0.position.x, self.p0.position.y)
        p1 = (self.p1.position.x, self.p1.position.y)
        pygame.draw.line(screen, self.colour, p0, p1)

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def copy(self):
        x = self.x
        y = self.y
        return Vector(x,y)

    def add(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x,y)

    def sub(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Vector(x,y)

    def multiply(self, value):
        x = self.x * value
        y = self.y * value
        return Vector(x,y)

    def divide(self, value):
        x = self.x / value
        y = self.y / value
        return Vector(x,y)

    def distance(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return math.sqrt(x * x + y * y)

numColumns = math.floor(width / pointSpacing) - 1
numRows = math.floor(height / pointSpacing) - 1

#create grid of points
points = []
for i in range(numRows):
    for j in range(numColumns):
        pos = Vector(j * pointSpacing + pointSpacing, i * pointSpacing + pointSpacing)
        p = Point(pos)
        points.append(p)

for i in range(0, numColumns, 2):
    points[i].pin()

sticks = []
#create all horizontal sticks
for i in range(len(points) - 1):
    if not (i % numColumns == numColumns - 1):
        sticks.append(Stick(points[i], points[i + 1]))

#create vertical sticks
for i in range(len(points) - numColumns):
    sticks.append(Stick(points[i], points[i + numColumns]))

while not clock.get_fps():
    clock.tick(60)
    clock.get_fps()

#global variables that alter the simulation
gravity = Vector(0, 0.5)
friction = 0.999
bounce = 0.9

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    fps = clock.get_fps()
    #show fps in topleft
    fpsSurface = fpsFont.render(f"FPS: {str(int(fps))}", False, [0,255,0])
    dt = 1 / clock.get_fps()
    update(dt, gravity, friction, bounce, width, height)
    draw()
    screen.blit(fpsSurface, [0,0])
    pygame.display.update()
    clock.tick(60)

    