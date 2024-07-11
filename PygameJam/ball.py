import pygame
from Physics import *

class Ball:
    def __init__(self, x, y, xvel, yvel, radius, holdtime, delay):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(xvel, yvel)
        self.radius = radius
        self.mass = 4*radius**3
        self.forces = []
        self.holdtime = holdtime
        self.delay = delay
        self.charge = 0
        self.cooldown = 0
        self.lineend = pygame.Vector2(0,0)
        self.canshoot = True
        self.slomo = False
        self.dead = False
        self.lastaction = [0, "initialize"]
        self.increase = 0
        self.multipliers = []
        self.multipliervalues = {"combo":      [4],
                                 "wallbounce": [1.5],
                                 "gravity turn":  [12],
                                 "slingshot":  [16]}
        
    def force(self, mousepos, limit):
        dif = self.pos - mousepos
        r = math.sqrt(dif.x**2 + dif.y**2)
        if r > limit:
            normal = dif.normalize()
            dif = pygame.Vector2(normal.x*limit, normal.y*limit)
        
        self.lastaction = [0, "shoot", dif * 0.07]
        return dif*0.07
    
    def scoremultiply(self, raw, multipliers):
        if len(multipliers) > 0:
            for multiplier in multipliers:
                val = self.multipliervalues[multiplier]
                final = raw * val[0]

            return final
        return raw
    
    def collisionscore(self, iv1, fv1, iv2, fv2, index, timer, multipliertime, basemultiplier):
        gainpoints = False
        self.multipliers = []
        
        if self.lastaction[1] == 'collision':
            if self.lastaction[0] >= timer or self.lastaction[3] != index:
                gainpoints = True
                if self.lastaction[0] <= multipliertime and self.lastaction[3] != index:
                    self.multipliers.append("combo")
                    
        elif self.lastaction[1] == 'wall' and self.lastaction[0] <= multipliertime:
            gainpoints = True
            self.multipliers.append("wallbounce")
            
        elif self.lastaction[1] == 'shoot':
            gainpoints = True
            
            prevmagnitude = math.sqrt(self.lastaction[2].x**2 + self.lastaction[2].y**2)
            if prevmagnitude >= 2:
                magnitude = math.sqrt(iv1.x**2 + iv1.y**2)
                prevangle = math.atan2(self.lastaction[2].y, self.lastaction[2].x)
                angle = math.atan2(iv1.y, iv1.x)
            
                dif = abs(angle - prevangle)
                if dif >= math.pi:
                    dif -= math.pi
                
                if dif >= math.pi/2:
                    if magnitude >= prevmagnitude + 3:
                        self.multipliers.append("slingshot")
                    else:
                        self.multipliers.append("gravity turn")
                    
        else:
            gainpoints = True
            
        if gainpoints:
            self.lastaction = [0, "collision", fv1, index]
                
            dif = iv2 - fv2
            leng = math.sqrt(dif.x**2 + dif.y**2)
            score = leng * basemultiplier
            multiplied = self.scoremultiply(score, self.multipliers)

            return math.ceil(multiplied)
        return 0
    
    def collide(self, initv2, finalv2, v1, index):
        self.increase = self.collisionscore(self.vel, v1, initv2, finalv2, index, 0.2, 2, 2)
            
        self.vel = v1

    def aim(self, speed, mousepos, mousestate, limit):
        if self.charge < 0:
            self.charge += speed/10
            if mousestate == 3:
                self.canshoot = True
           
        #0 = no mouse, 1 = click, 2 = hold, 3 = release

        elif self.charge < self.holdtime and self.charge >= 0:    
            if self.canshoot:
                if mousestate == 2:
                    self.slomo = True
                
                    dif = self.pos - mousepos
                    r = math.sqrt(dif.x**2 + dif.y**2)
                    if r > limit:
                        normal = dif.normalize()
                        dif = pygame.Vector2(normal.x*limit, normal.y*limit)
                    self.lineend = self.pos - dif
                
                    self.charge += speed
                
                elif mousestate == 3:
                    self.slomo = False
                
                    self.vel = self.force(mousepos, limit)
                    self.charge = -self.delay
                    
            elif mousestate == 3:
                self.canshoot = True
                
        elif self.charge >= self.holdtime:
            self.slomo = False

            self.vel = self.force(mousepos, limit)
            self.charge = -self.delay
            self.canshoot = False
            
    def update(self, mousepos, mousestate, speed, swidth, sheight):
        hold = False
        self.increase = 0
        
        self.lastaction[0] += speed/60

        newvel = ScreenBounce(self.pos, self.vel, self.radius, swidth, sheight)
        if newvel != self.vel:
            self.lastaction = [0, "wall", newvel]
            self.vel = newvel
        
        self.aim(speed, mousepos, mousestate, 300)

        sigmaforce = pygame.Vector2(0,0)
        finalforce = pygame.Vector2(0,0)
        for force in self.forces:
            sigmaforce.x += force.x
            sigmaforce.y += force.y
        
            finalforce = pygame.Vector2(sigmaforce.x/len(self.forces), sigmaforce.y/len(self.forces))
            
        self.forces = []
        
        self.vel += speed*finalforce/(self.mass)

        self.pos += self.vel * speed
        print(self.pos)
    
    def draw(self, screen, center, srotation, scalefactor):
        scaledpos = pygame.Vector2(self.pos.x * scalefactor.x, self.pos.y * scalefactor.y)
        finalpos = RotatePoint(center, scaledpos, srotation)
        pygame.draw.circle(screen, (150,150,200), finalpos, self.radius * scalefactor.x)
        if self.slomo:
            pygame.draw.line(screen, (150, 150, 200), finalpos, RotatePoint(center, pygame.Vector2(self.lineend.x * scalefactor.x, self.lineend.y * scalefactor.y), srotation), 2)