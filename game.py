import pygame
import math
import random

from ball import Ball
from body import Body
from sounds import Music
from Physics import RotatePoint
from UI import button

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h

        #self.SCREEN_WIDTH = 1440
        #self.SCREEN_HEIGHT = 720
        self.scalefactor = pygame.Vector2(self.SCREEN_WIDTH / 1920, self.SCREEN_HEIGHT / 1080)

        self.SCREEN_CENTER = pygame.Vector2(self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/2)
        
        self.G = 0.15

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption('Space')

        self.scorfont = pygame.font.SysFont('Ariel', 40)
        
        with open("sounds/number.txt", "r") as f:
            try:
                self.totalscore = int(f.read())
            except:
                self.totalscore = 0

        self.scoresurfaces = []
        self.scorelife = 2
        
        self.highestheat = 0
        self.isblackhole = 0

        self.mousestate = 0

        self.music = Music()
        self.music.startsounds()

        self.buttoncolour = (15, 15, 20)

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

    def menu(self):
        page = 0
        
        menusystem = [[960, 540, 0, 0.084375, 100, 0],
                     [500, 540, 0, -25, 30, 0]]
        
        playtext = self.displaytext('PLAY', size = 70)
        optionstext = self.displaytext('OPTIONS', size = 30)
        quittext = self.displaytext('(ESC to quit)', size = 25)

        apology = self.displaytext('Sorry, nothing here yet.', size = 55)
        nowindow = self.displaytext("you're stuck with fullscreen.", size = 45)
        
        apologypos = pygame.Vector2(500, 500)
        nowindowpos = pygame.Vector2(520, 550)
        apologyvel = pygame.Vector2(79, 30)
        nowindowvel = pygame.Vector2(80, 40)
        
        options = button(self.screen, 10, 10, 180, 100, self.buttoncolour)

        planets = []

        for i in range(0, len(menusystem)):
            self.construct(menusystem, i, planets)
            
        planets[1].mass = 6750
        
        esc = False

        game = True
        while game:
            self.screen.fill((0,0,0))
            dt = self.clock.tick()/1000
            dt = min(dt, 0.2)

            self.music.play(dt, 0, 0)

            if self.mousestate == 3:
                self.mousestate = 0
            elif self.mousestate == 1:
                self.mousestate = 2
            #0 = no mouse, 1 = click, 2 = hold, 3 = release

            for event in pygame.event.get():
            
                if event.type == pygame.QUIT:
                    game = False
            
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mousestate = 1
            
                if event.type == pygame.MOUSEBUTTONUP:
                    self.mousestate = 3
            
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        esc = True
                    if event.key == pygame.K_SPACE:
                        self.rungame(0)
                        
            mouse = pygame.mouse.get_pos()
            scaledmouse = pygame.Vector2(mouse[0] / self.scalefactor.x, mouse[1] / self.scalefactor.y)

            if page == 0:
                if esc:
                    game = False

                for item in planets:
                    item.force(planets, self.SCREEN_WIDTH/self.scalefactor.x, self.SCREEN_HEIGHT/self.scalefactor.y)
                
                for item in planets:
                    item.physics(dt*20)
                    item.draw(self.screen, self.SCREEN_CENTER, 0, self.scalefactor)
                          
                if planets[0].clicked(scaledmouse, self.mousestate):
                    self.rungame(0)
                    
                if planets[1].clicked(scaledmouse, self.mousestate):
                    self.rungame(1)
                        
                if options.update(self.mousestate, scaledmouse):
                    page = 1
                    
                totalscoretext = self.displaytext('TOTAL SCORE: ' + str(self.totalscore), size = 30)

                self.screen.blit(playtext, (planets[0].pos.x*self.scalefactor.x - playtext.get_width()/2, planets[0].pos.y*self.scalefactor.y - playtext.get_height()/2))
                self.screen.blit(optionstext, (50*self.scalefactor.x, 50*self.scalefactor.y))
                self.screen.blit(quittext, (10*self.scalefactor.x, 1080*self.scalefactor.y - quittext.get_height()))
                self.screen.blit(totalscoretext, (1870*self.scalefactor.x - totalscoretext.get_width(), 50*self.scalefactor.y))

            elif page == 1:
                if esc:
                    page = 0
                    esc = False
                   
                apologypos += pygame.Vector2(apologyvel.x * dt, apologyvel.y*dt)
                nowindowpos += pygame.Vector2(nowindowvel.x * dt, nowindowvel.y*dt)
                
                if apologypos.x >= self.SCREEN_WIDTH - apology.get_width():
                    apologyvel = pygame.Vector2(abs(apologyvel.x) * -1, apologyvel.y)
                if apologypos.x <= 0:
                    apologyvel = pygame.Vector2(abs(apologyvel.x), apologyvel.y)
                if apologypos.y >= self.SCREEN_HEIGHT - apology.get_height():
                    apologyvel = pygame.Vector2(apologyvel.x, abs(apologyvel.y) * -1)
                if apologypos.y <= 0:
                    apologyvel = pygame.Vector2(apologyvel.x, abs(apologyvel.y))
                    
                if nowindowpos.x >= self.SCREEN_WIDTH - nowindow.get_width():
                    nowindowvel = pygame.Vector2(abs(nowindowvel.x) * -1, nowindowvel.y)
                if nowindowpos.x <= 0:
                    nowindowvel = pygame.Vector2(abs(nowindowvel.x), nowindowvel.y)
                if nowindowpos.y >= self.SCREEN_HEIGHT - nowindow.get_height():
                    nowindowvel = pygame.Vector2(nowindowvel.x, abs(nowindowvel.y) * -1)
                if nowindowpos.y <= 0:
                    nowindowvel = pygame.Vector2(nowindowvel.x, abs(nowindowvel.y))

                self.screen.blit(apology, (apologypos.x * self.scalefactor.x, apologypos.y * self.scalefactor.y))
                self.screen.blit(nowindow, (nowindowpos.x*self.scalefactor.x, nowindowpos.y*self.scalefactor.y))

            pygame.display.update()
            

    def rungame(self, system):
        self.soundstate = 1
        
        self.highestheat = 0
        self.isblackhole = 0
        
        self.gameover = False

        system1 = [[960, 540, 0, 0, 50, 0],
                   [650, 540, 0, -4, 15, 0],
                   [1270, 540, 0, 4, 15, 0],
                   [960, 850, -4, 0, 15, 0],
                   [960, 230, 4, 0, 15, 0],
                   [100, 540, 0, -5, 15, 0],
                   [1820, 540, 0, 5, 15, 0]
           
        ]#v1 = -v2*r2^3/r1^3
        system2 = [[960, 540, 0, 0, 50, 0],
                   [650, 540, 0, -4, 5, 0],
                   [1270, 540, 0, 4, 5, 0],
                   [960, 850, -4, 0, 5, 0],
                   [960, 230, 4, 0, 5, 0],
                   [100, 540, 0, -5, 5, 0],
                   [1820, 540, 0, 5, 5, 0]
        ]

        player = Ball(200, 700, 0, 0, 10, 6, 4)
        planets = []

        if system == 0:
            for i in range(0, len(system1)):
                self.construct(system1, i, planets)
        else:
            for i in range(0, len(system2)):
                self.construct(system2, i, planets)
            
        mainmenutext = self.displaytext('MAIN MENU', size = 30)
        resumetext = self.displaytext('RESUME', size = 30)
        pausedtext = self.displaytext('PAUSED', size = 100)
        gameovertext = self.displaytext('GAME OVER', size = 100)

        mainmenu = button(self.screen, 660, 480, 180, 100, self.buttoncolour)
        resume = button(self.screen, 1050, 480, 180, 100, self.buttoncolour)
        mainmenu2 = button(self.screen, 865, 480, 180, 100, self.buttoncolour)

        speedfactor = 1
        speedchange = 1

        score = 0

        srotation = 0
        ispaused = False

        scoreupdated = False

        esc = False

        game = True
        while game:
            dt = self.clock.tick()/1000
            dt = min(dt, 0.2)

            if self.mousestate == 3:
                self.mousestate = 0
            elif self.mousestate == 1:
                self.mousestate = 2
            #0 = no mouse, 1 = click, 2 = hold, 3 = release

            mouse = pygame.mouse.get_pos()
            rotatedmouse = RotatePoint(self.SCREEN_CENTER, mouse, -srotation)
            scaledmouse = pygame.Vector2(rotatedmouse[0] / self.scalefactor.x, rotatedmouse[1] / self.scalefactor.y)

            for event in pygame.event.get():
            
                if event.type == pygame.QUIT:
                    self.exit()
            
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mousestate = 1
            
                if event.type == pygame.MOUSEBUTTONUP:
                    self.mousestate = 3
            
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        esc = True

                    if event.key == pygame.K_LEFT:
                        srotation -= 1
                    if event.key == pygame.K_RIGHT:
                        srotation += 1

            if not ispaused:
                self.screen.fill((0,0,0))
            
                self.music.play(dt, self.soundstate, self.highestheat)

                for item in planets:
                    item.force(planets, self.SCREEN_WIDTH/self.scalefactor.x, self.SCREEN_HEIGHT/self.scalefactor.y, player)
            
                if player.increase > 0:
                    self.scoresurfaces.append([self.displaytext(player.increase), (player.pos.x * self.scalefactor.x, (player.pos.y - 20) * self.scalefactor.x ), self.scorelife])
                    for multiplier in player.multipliers:
                        self.scoresurfaces.append([self.displaytext(multiplier), (player.pos.x * self.scalefactor.x, (player.pos.y - 40) * self.scalefactor.x), self.scorelife])
                    
                    score += player.increase
                    
                if self.gameover:
                    player.update(scaledmouse, 0, speedfactor, self.SCREEN_WIDTH/self.scalefactor.x, self.SCREEN_HEIGHT/self.scalefactor.y)
                else:
                    player.update(scaledmouse, self.mousestate, speedfactor, self.SCREEN_WIDTH/self.scalefactor.x, self.SCREEN_HEIGHT/self.scalefactor.y)

                if player.slomo:
                    speedfactor = 0.1*dt*60*speedchange
                else:
                    speedfactor = 1*dt*60*speedchange
        
                player.draw(self.screen, self.SCREEN_CENTER, srotation, self.scalefactor)
        
                if len(planets) == 1:
                    if planets[0].state == 1:
                        self.gameover = True

                heatvals = []
                for item in planets:
                    if item.dead:
                        planets.remove(item)
                    else:
                        if item.physics(speedfactor):
                            if self.soundstate == 1:
                                self.soundstate = 2
                        if item.heat >= 200:
                            planets.remove(item)
                        item.draw(self.screen, self.SCREEN_CENTER, srotation, self.scalefactor)
                    heatvals.append(item.heat)
                
                self.highestheat = max(heatvals)
                
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
                        
                if self.gameover:
                    
                    if scoreupdated == False:
                        with open("sounds/number.txt", "r") as f:
                            try:
                                self.totalscore = int(f.read())
                            except:
                                self.totalscore = 0
                            
                        self.totalscore += score
                        
                        print(self.totalscore, type(self.totalscore))
                        
                        with open("sounds/number.txt", "w") as f:
                            f.write(str(self.totalscore))
                        scoreupdated = True

                    if esc == True:
                        game = False

                    if mainmenu2.update(self.mousestate, scaledmouse):
                        game = False
                        
                    self.screen.blit(mainmenutext, (900*self.scalefactor.x, 520*self.scalefactor.y))
                    self.screen.blit(gameovertext, (750*self.scalefactor.x, 350*self.scalefactor.y))

                    if speedchange > 0:
                        speedchange -= 0.1 * dt
                    else:
                        speedchange = 0

                elif esc == True:
                    ispaused = True
                    esc = False
                
            else:
                self.music.play(dt, 0, 0)
                
                if esc == True:
                    ispaused = False
                    esc = False

                if mainmenu.update(self.mousestate, scaledmouse):
                    game = False
                    
                if resume.update(self.mousestate, scaledmouse):
                    ispaused = False
                    player.canshoot = False
                    

                self.screen.blit(mainmenutext, (700*self.scalefactor.x, 520*self.scalefactor.y))
                self.screen.blit(resumetext, (1100*self.scalefactor.x, 520*self.scalefactor.y))
                self.screen.blit(pausedtext, (805*self.scalefactor.x, 350*self.scalefactor.y))

            pygame.display.update()
            
    def exit(self):
        pygame.quit()