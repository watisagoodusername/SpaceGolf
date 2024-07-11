import pygame
import math
import random

from pygame.version import PygameVersion
from ball import Ball
from body import Body
from Physics import RotatePoint

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h

        #self.SCREEN_WIDTH = 1440
       # self.SCREEN_HEIGHT = 720
        self.scalefactor = pygame.Vector2(self.SCREEN_WIDTH / 1920, self.SCREEN_HEIGHT / 1080)

        self.SCREEN_CENTER = pygame.Vector2(self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/2)
        
        self.G = 0.15

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption('Space')

        self.scorfont = pygame.font.SysFont('Ariel', 40)
        self.scoresurfaces = []
        self.scorelife = 2

        self.clock = pygame.time.Clock()
       
    def construct(self, system, i, listout):
        listout.append(Body(i, system[i][0], system[i][1], system[i][2], system[i][3], system[i][4], system[i][5], self.G))
        
    def displaytext(self, text, font=None, size=None):
        
        text = str(text)
        
        if font is not None:
            surface = font.render(text, False, (255,255,255))
            
        elif size is not None:
            font = pygame.font.SysFont('Ariel', size)
            surface = font.render(text, False, (255,255,255))
            
        else:
            font = pygame.font.SysFont('Ariel', 30)
            surface = font.render(text, False, (255,255,255))
            
        return surface

    def run(self):
        planetamount = 7

        system1 = [[self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2, 0, 0.064, 50, 0],
                   [650, self.SCREEN_HEIGHT // 2, 0, -5, 15, 0],
                   [self.SCREEN_WIDTH - 659, self.SCREEN_HEIGHT // 2, 0, 5, 15, 0],
                   [self.SCREEN_WIDTH - 652, self.SCREEN_HEIGHT // 2, 0, 5, 15, 0],
                   [self.SCREEN_WIDTH - 651, self.SCREEN_HEIGHT // 2, 0, 5, 15, 0],
                   [self.SCREEN_WIDTH - 653, self.SCREEN_HEIGHT // 2, 0, 5, 15, 0],
                   [self.SCREEN_WIDTH - 655, self.SCREEN_HEIGHT // 2, 0, 5, 15, 0]
           
        ]#v1 = -v2*r2^3/r1^3

        player = Ball(200, 700, 0, 0, 10, 6, 4)
        planets = []

        for i in range(0, planetamount):
            self.construct(system1, i, planets)

        speedfactor = 1

        score = 0

        mousestate = 0
        srotation = 0

        game = True
        while game:
            dt = self.clock.tick()/1000
            self.screen.fill((0,0,0))
    
            if mousestate == 3:
                mousestate = 0
            elif mousestate == 1:
                mousestate = 2
            #0 = no mouse, 1 = click, 2 = hold, 3 = release

            for event in pygame.event.get():
            
                if event.type == pygame.QUIT:
                    game = False
            
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousestate = 2
            
                if event.type == pygame.MOUSEBUTTONUP:
                    mousestate = 3
            
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game = False

                    if event.key == pygame.K_LEFT:
                        srotation -= 1
                    if event.key == pygame.K_RIGHT:
                        srotation += 1
    
            mouse = pygame.mouse.get_pos()
            rotatedmouse = RotatePoint(self.SCREEN_CENTER, mouse, -srotation)
            scaledmouse = pygame.Vector2(rotatedmouse[0] / self.scalefactor.x, rotatedmouse[1] / self.scalefactor.y)

            for item in planets:
                item.force(planets, player, self.SCREEN_WIDTH/self.scalefactor.x, self.SCREEN_HEIGHT/self.scalefactor.y)
            
            if player.increase > 0:
                self.scoresurfaces.append([self.displaytext(player.increase), (player.pos.x * self.scalefactor.x, (player.pos.y - 20) * self.scalefactor.x ), self.scorelife])
                for multiplier in player.multipliers:
                    self.scoresurfaces.append([self.displaytext(multiplier), (player.pos.x * self.scalefactor.x, (player.pos.y - 40) * self.scalefactor.x), self.scorelife])
                    
                score += player.increase
            player.update(scaledmouse, mousestate, speedfactor, self.SCREEN_WIDTH/self.scalefactor.x, self.SCREEN_HEIGHT/self.scalefactor.y)

            if player.slomo:
                speedfactor = 0.1*dt*60
            else:
                speedfactor = 1*dt*60
        
            player.draw(self.screen, self.SCREEN_CENTER, srotation, self.scalefactor)
        
            for item in planets:
                if item.dead:
                    planets.remove(item)
                else:
                    item.physics(speedfactor)
                    if item.heat >= 200:
                        planets.remove(item)
                    item.draw(self.screen, self.SCREEN_CENTER, srotation, self.scalefactor)
                
            self.screen.blit(self.displaytext(score, self.scorfont), (5, 5))
            
            
            for img in self.scoresurfaces:
                if img[2] > self.scorelife / 2:
                    self.screen.blit(img[0], img[1])
                    img[2] -= dt
                elif img[2]> 0:
                    img[0].set_alpha(img[2]*255/(self.scorelife / 2))
                    self.screen.blit(img[0], img[1])
                    img[2] -= dt
                else:
                    self.scoresurfaces.remove(img)

            pygame.display.update()
            
    def exit(self):
        pygame.quit()