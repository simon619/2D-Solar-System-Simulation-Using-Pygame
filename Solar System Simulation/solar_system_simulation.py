from itertools import count
import pygame
import math
pygame.init()
background = pygame.image.load('images/star.jpg')
height, width = 800, 800
window = pygame.display.set_mode((height, width))
pygame.display.set_caption('Solar System Simulation')
blue = (0, 0, 255)
copper_red = (230, 115, 51)
white = (255, 255, 255)
yellow = (255,255,0)
grey_white = (213, 193, 170)
dark_grey = (100, 100, 100)

class Planet():

    AU = 146 * 10 ** 6 * 1000
    G = 6.67428e-11
    Scale = 200 / AU
    Time_scale = 3600 * 24


    def __init__(self, name, x, y, radius, color, mass):
        self.name = name
        self.x = x
        self.y = y
        self.mass = mass
        self.radius = radius
        self.color = color
        self.vel_x = 0
        self.vel_y = 0
        self.orbit = []


    def moon_coordinate(self, x, y):
        x_rad = 50
        y_rad = 25
        global count        
        x1 = int(math.cos(count * math.pi / 180) *  x_rad) + x
        y1 = int(math.sin(count * math.pi / 180) *  y_rad) + y            
        if count == 360:
            count = 0
        else:
            count += 10
        return x1, y1

    
    def draw(self, window):
        x = self.x * self.Scale + width / 2
        y = self.y * self.Scale + height / 2
        if len(self.orbit) > 2:
            for i in self.orbit:
                (x, y) = i
                x = x * self.Scale + width / 2
                y = y * self.Scale + height / 2
        if self.name == 'earth':
            m, n = self.moon_coordinate(x, y)
            pygame.draw.circle(window, white, (m, n), 5)    
        pygame.draw.circle(window, self.color, (x, y), self.radius)


    def force(self, other_planet):
        other_planet_x, other_planet_y = other_planet.x, other_planet.y
        dis_x, dis_y = other_planet_x - self.x, other_planet_y - self.y
        dis = math.sqrt(dis_x ** 2 + dis_y ** 2)
        force = self.G * self.mass * other_planet.mass / dis ** 2
        theta = math.atan2(dis_y , dis_x)
        force_x = force * math.cos(theta)
        force_y = force * math.sin(theta)
        return force_x, force_y


    def coordinate(self, planets):
        total_fx, total_fy = 0, 0
        for other_planet in planets:
            if self == other_planet:
                continue
            f_x, f_y = self.force(other_planet)
            total_fx += f_x
            total_fy += f_y
            
        self.vel_x += total_fx / self.mass * self.Time_scale
        self.vel_y += total_fy / self.mass * self.Time_scale

        self.x += self.vel_x * self.Time_scale
        self.y += self.vel_y * self.Time_scale
        self.orbit.append((self.x, self.y)) 
        

def main():
    running = True
    global count
    count = 0
    sun = Planet('sun', 0, 0, 30, yellow, 1.9889 * 10**30)
    marcury = Planet('marcury', 0.387 * Planet.AU, 0, 8, dark_grey, 3.30 * 10 ** 23)
    marcury.vel_y = -47.6 * 1000
    earth = Planet('earth', -1 * Planet.AU, 0, 15, blue, 5.9742 * 10**24)
    earth.vel_y = 29.821 * 1000 
    mars =  Planet('mars', -1.524 * Planet.AU, 0, 12, copper_red, 6.19 * 10 ** 23)
    mars.vel_y = 24.279 * 1000
    jupyter = Planet('jupyter', -1.77 * Planet.AU, 0, 22, grey_white, 5.9742 * 10 ** 26)
    jupyter.vel_y = 23.783 * 1000 
    planets = [sun, marcury, earth, mars, jupyter]
    clock = pygame.time.Clock()
    while running:
        clock.tick(60)
        window.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        window.blit(background, (0, 0))
        for i in planets:
            i.coordinate(planets)
            i.draw(window)
        pygame.display.update()
    pygame.quit()
main()