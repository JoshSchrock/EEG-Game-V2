import pygame

class Slider:
    def __init__(self):
        self.pos = 1

    def update(self, pos):
        self.pos = pos

    def reset(self):
        self.pos = 1

    def draw(self, screen, pos):
        x, y = pos
        pygame.draw.rect(screen, pygame.color.Color('black'), (x, y, 250, 10))
        pygame.draw.rect(screen, pygame.color.Color('black'), (x, y - 20, 10, 30))
        pygame.draw.rect(screen, pygame.color.Color('black'), (x + 10 + 84, y - 20, 4, 30))
        pygame.draw.rect(screen, pygame.color.Color('black'), (x + 10 + 142, y - 20, 4, 30))
        pygame.draw.rect(screen, pygame.color.Color('black'), (x + 240, y - 20, 10, 30))
        pygame.draw.polygon(screen, pygame.color.Color('red'),
                            [(x + 10 + (self.pos * 115), y),
                             (x + (self.pos * 115), y - 20),
                             (x + 20 + (self.pos * 115), y - 20)])