import pygame

class Music():
    def __init__(self):
        self.maintheme = pygame.mixer.Sound("sounds/maintheme.wav") 
        self.drums1 = pygame.mixer.Sound("sounds/drums1.wav")
        self.drums2 = pygame.mixer.Sound("sounds/drums2.wav")
        self.final = pygame.mixer.Sound("sounds/chaos.wav")
        self.intro = pygame.mixer.Sound("sounds/intro.wav")
        self.timer = 0
        
        self.mainthemevol = 0
        self.drums1vol = 0
        self.drums2vol = 0
        self.finalvol = 0
        self.introvol = 0.6
        
        self.prevstate = 0
        self.introgoing = False

    def gradual(self, current, target, speed):
        if current < target - speed:
            current += speed
        elif current > target + speed:
            current -= speed
        else:
            current = target
            
        return current

    def startsounds(self):
        pygame.mixer.Sound.play(self.maintheme) 
        pygame.mixer.Sound.play(self.drums1) 
        pygame.mixer.Sound.play(self.drums2)
        pygame.mixer.Sound.play(self.final)
        
    def stopmusic(self):
        pygame.mixer.Sound.stop(self.maintheme) 
        pygame.mixer.Sound.stop(self.drums1) 
        pygame.mixer.Sound.stop(self.drums2)
        pygame.mixer.Sound.stop(self.final)
        
    def setvolumes(self, maintheme, drums1, drums2, final, intro):
        pygame.mixer.Sound.set_volume(self.maintheme, maintheme)
        pygame.mixer.Sound.set_volume(self.drums1, drums1)
        pygame.mixer.Sound.set_volume(self.drums2, drums2)
        pygame.mixer.Sound.set_volume(self.final, final)
        pygame.mixer.Sound.set_volume(self.intro, intro)
        
    def volumes(self, maintheme, drums1, drums2, final, gradualspeed):
        self.mainthemevol = self.gradual(self.mainthemevol, maintheme, gradualspeed)
        self.drums1vol = self.gradual(self.drums1vol, drums1, gradualspeed)
        self.drums2vol = self.gradual(self.drums2vol, drums2, gradualspeed)
        self.finalvol = self.gradual(self.finalvol, final, gradualspeed)
        
        pygame.mixer.Sound.set_volume(self.maintheme, self.mainthemevol)
        pygame.mixer.Sound.set_volume(self.drums1, self.drums1vol)
        pygame.mixer.Sound.set_volume(self.drums2, self.drums2vol)
        pygame.mixer.Sound.set_volume(self.final, self.finalvol)

    def play(self, dt, gamestate, heat):
        self.timer += dt

        if gamestate >= 0:
            if gamestate == 0:
                self.volumes(0.6, 0, 0, 0, 0.002)
            elif gamestate == 1:
                if heat <= 100:
                    self.volumes(0.6, 0.4, heat/150, 0, 0.002)
                else:
                    volumemulitplier = 1 - (heat - 100)/75
                    self.volumes(0.6 * volumemulitplier, 0.4 * volumemulitplier, heat/150, 0, 0.0005)
            elif gamestate == 2:
                if self.prevstate == 1:
                    self.timer = 0
                    self.setvolumes(0,0,0,0, 0.5)
                    self.stopmusic()
                    pygame.mixer.Sound.play(self.intro)
                    self.introgoing = True
                    
                if self.introgoing:
                    if self.timer >= 2:
                        self.introgoing = False
                        self.timer = 0
                        self.setvolumes(0.6,0.6,0.3,0.6, 0.5)
                        self.startsounds()
                else:
                    self.volumes(0.6, 0.6, 0.4, 0.6, 0.002)
                
            if self.timer >= 32:
                self.timer = 0
                self.startsounds()
                
        self.prevstate = gamestate
        
          
