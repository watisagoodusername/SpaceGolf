import pygame

class button():
    def __init__(self, screen, x, y, width, height, colour):
        self.pos = pygame.Vector2(x,y)
        self.colour  = colour
        self.rect = pygame.Rect(x,y,width,height)
        self.screen = screen
        
    def update(self, mousestate, mousepos):
        pygame.draw.rect(self.screen, self.colour, self.rect)
        padding = pygame.Vector2(5, 5)

        if self.rect.collidepoint(mousepos):
            if mousestate == 1:
                return True
                
        return False
    