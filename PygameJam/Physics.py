import pygame
import math

def RotatePoint(center, pos, angle):
    dif = pos - center
    change = dif.rotate(angle)
    return change + center

def CircleCollide(rt, r1, r2):  
        if rt < r1 + r2:
            return True
        return False

def CircleBounce(contactangle, v1, v2, m1, m2, damp):
        rv1 = v1.rotate_rad(contactangle)
        rv2 = v2.rotate_rad(contactangle)
        
        v1y = ((m1-m2)/(m1+m2))*rv1.y + ((2*m2)/(m1+m2))*rv2.y
        v2y = ((2*m1)/(m1+m2))*rv1.y + ((m2-m1)/(m1+m2))*rv2.y
        
        frv1 = pygame.Vector2(rv1.x, v1y)
        frv2 = pygame.Vector2(rv2.x, v2y)
        
        fv1 = frv1.rotate_rad(-contactangle) * damp
        fv2 = frv2.rotate_rad(-contactangle) * damp
        
        return(fv1, fv2)

def ScreenBounce(pos, vel, radius, swidth, sheight):
    finalvel = vel

    if pos.x >= swidth-radius:
        finalvel = pygame.Vector2(abs(vel.x)*-0.95, vel.y)
    if pos.x <= radius:
        finalvel = pygame.Vector2(abs(vel.x)*0.95, vel.y)
    if pos.y >= sheight-radius:
        finalvel = pygame.Vector2(vel.x, abs(vel.y)*-0.95)
    if pos.y <= radius:
        finalvel = pygame.Vector2(vel.x, abs(vel.y)*0.95)
        
    return finalvel