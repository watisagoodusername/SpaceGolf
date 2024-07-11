import math
import pygame
import random

SCREEN_WIDTH = 1000
SCREEN_HEIGHT =  1000

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pygame.time.Clock()

class Object:
    def __init__(self, x, y, xvel, yvel, radius):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(xvel, yvel)
        self.radius = radius
        self.mass = 4*radius**3
   
    def colliding(self, dif, r2):
        rt = math.sqrt(dif.x**2 + dif.y**2)    
        if rt <= self.radius + r2:
            return True
        return False
        
    def draw(self):
        pygame.draw.circle(screen, (50,50,50), self.pos, self.radius)
        
    def update(self):
        self.pos += self.vel
        self.draw()

    def bounce(self, contactangle, v1, v2, m1, m2):
        rv1 = v1.rotate_rad(contactangle)
        rv2 = v2.rotate_rad(contactangle)
        
        v1y = ((m1-m2)/(m1+m2))*rv1.y + ((2*m2)/(m1+m2))*rv2.y
        v2y = ((2*m1)/(m1+m2))*rv1.y + ((m2-m1)/(m1+m2))*rv2.y
        
        frv1 = pygame.Vector2(rv1.x, v1y)
        frv2 = pygame.Vector2(rv2.x, v2y)
        
        fv1 = frv1.rotate_rad(-contactangle)
        fv2 = frv2.rotate_rad(-contactangle)
        
        return(fv1, fv2)
        
    def physics(self, interaction):
        dif = self.pos - interaction.pos
        if self.colliding(dif, interaction.radius):
            
            contactangle = math.atan2(dif.x, dif.y)
            v1 = self.vel
            v2 = interaction.vel
            m1 = self.mass
            m2 = interaction.mass
            finalvels = self.bounce(contactangle, v1, v2, m1, m2)
            self.vel = finalvels[0]
            interaction.vel = finalvels[1]

obstacle = Object(500,500, 0,0, 50)
projectile = Object(250,200, 5,5, 50)

game = True
while game:
    clock.tick(60)
    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
            
    projectile.physics(obstacle)
    obstacle.update()
    projectile.update()

    pygame.display.update()
    
pygame.quit()