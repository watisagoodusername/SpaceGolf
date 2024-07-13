import pygame
import math
from Physics import *

class Body:
    def __init__(self, index, x, y, xvel, yvel, radius, state, constant, mass = None):
        self.index = index
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(xvel, yvel)
        self.radius = radius
        if mass is None:
            self.mass = 2*radius**3
        else:
            self.mass = mass
        self.state = state
        self.constant = constant
        self.forces = []
        self.heat = 0
        self.timesincehit = 0
        self.dead = False
        self.timealive = 0
        self.heatmultiplier = 0

    def clicked(self, mousepos, mousestate):
        dif = mousepos - self.pos
        rt = math.sqrt(dif.x**2 + dif.y**2)

        if CircleCollide(rt, self.radius, 0):
            if mousestate == 1:
                return True
        return False

    def bounce(self, otherobject, dif):
        contactangle = math.atan2(dif.x, dif.y)
        v1 = self.vel
        v2 = otherobject.vel
        m1 = self.mass
        m2 = otherobject.mass
        return CircleBounce(contactangle, v1, v2, m1, m2, 0.999)
        
    def gravforce(self, difference, m1, m2):
        direction = pygame.Vector2(difference).normalize()
        r = math.sqrt(difference[0]**2 + difference[1]**2)
        force = self.constant*m1*m2/r**2
        
        return(pygame.Vector2(force*direction.x, force*direction.y))
    
    def consume(self, other):
        consumedmass = other.mass * 2
        radiuschange = (other.radius/2)**1/3
        self.mass += consumedmass

    def interact(self, item, isball):
        if self.heatmultiplier < 199:    
            self.heatmultiplier = 2**(0.04*self.timealive)
        else:
            self.heatmultiplier = 199
                
        dif = self.pos - item.pos
        rt = math.sqrt(dif.x**2 + dif.y**2)  
            
        if CircleCollide(rt, self.radius, item.radius):
            if self.state == 1:
                return (item)

            if self.timesincehit >= 0.5:
                self.heat += self.heatmultiplier
                self.timesincehit = 0
                    
            if not isball:
                if item.state == 1:
                    return(self)
                if item.timesincehit >= 0.5:
                    item.heat += item.heatmultiplier
                    item.timesincehit = 0

            clip = self.radius + item.radius - rt
            if clip >= 3:
                
                ratio = self.radius/item.radius

                d1 = ratio*clip/2
                d2 = clip/ratio*2
                
                self.pos += dif.normalize() * d2
                item.pos -= dif.normalize() * d1

            finalvels = self.bounce(item, dif)
                
            if isball:
                item.collide(self.vel, finalvels[0], finalvels[1], self.index)
            else:
                item.vel = finalvels[1]
                    
            self.vel = finalvels[0]
                
        else:
            force = self.gravforce(dif, self.mass, item.mass)
            
            self.forces.append(force * -1)
            item.forces.append(force)
        
    def force(self, bodies, swidth, sheight, ball = None):
        force = pygame.Vector2(0,0)
        iterations = 0
        
        self.vel = ScreenBounce(self.pos, self.vel, self.radius, swidth, sheight)

        if ball is not None:
            if self.interact(ball, True) == ball:
                ball.dead = True

        for i in range(self.index + 1, len(bodies)):
            toberemoved = self.interact(bodies[i], False)
            if toberemoved:
                toberemoved.dead = True
                if toberemoved == self:
                    bodies[i].consume(toberemoved)
                else:
                    self.consume(toberemoved)

    def physics(self, speed):
        self.timealive += speed/ 60

        self.timesincehit += speed/60
        
        if self.heat > 0 and self.timesincehit > 1:
            self.heat -= speed / 5

        sigmaforce = pygame.Vector2(0,0)
        finalforce = pygame.Vector2(0,0)
        for force in self.forces:
            sigmaforce.x += force.x
            sigmaforce.y += force.y
        
            finalforce = pygame.Vector2(sigmaforce.x/len(self.forces), sigmaforce.y/len(self.forces))
            
        self.forces = []
        
        self.vel += speed*finalforce/(self.mass)

        self.pos += self.vel * speed
        
        if self.heat >= 200:
            if self.mass >= 54000:
                self.state = 1
                self.heat = 0
                self.radius = 1
                return True
        return False
    
    def draw(self, screen, center, srotation, scalefactor):
        scaledpos = pygame.Vector2(self.pos.x * scalefactor.x, self.pos.y * scalefactor.y)
        finalpos = RotatePoint(center, scaledpos, srotation)
        
        if self.state == 0:
            xr = self.radius * scalefactor.x
            yr = self.radius * scalefactor.y
            rect = pygame.Rect(finalpos.x - xr, finalpos.y - yr, xr * 2, yr * 2)
            if self.heat <= 200:
                pygame.draw.ellipse(screen, (50 + self.heat,50,50), rect)
            else:
                pygame.draw.ellipse(screen, (255,50,50), rect)
        else:
            xr1 = 15*scalefactor.x
            yr1 = 15*scalefactor.y
            xr2 = 10*scalefactor.x
            yr2 = 10*scalefactor.y
            rect1 = pygame.Rect(finalpos.x - xr1, finalpos.y - yr1, xr1 * 2, yr1 * 2)
            rect2 = pygame.Rect(finalpos.x - xr2, finalpos.y - yr2, xr2 * 2, yr2 * 2)
            pygame.draw.circle(screen, (200, 200 - self.heat, 200 - self.heat), finalpos, 15*scalefactor.x)
            pygame.draw.circle(screen, (5, 5, 5), finalpos, 10*scalefactor.x)
            pygame.draw.ellipse(screen, (200, 200 - self.heat, 200 - self.heat), rect1)
            pygame.draw.ellipse(screen, (5, 5, 5), rect2)