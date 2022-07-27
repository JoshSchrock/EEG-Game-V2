import pygame

class Lives:
    def __init__(self, lives, color, width, height):
        self.lives = lives
        self.width = width
        self.car = pygame.image.load('car.png')
        self.car = pygame.transform.scale(self.car, (self.width, height))
        self.car.set_colorkey(pygame.color.Color('white'))
        var = pygame.PixelArray(self.car)
        var.replace((242, 173, 18), color)

    def die(self):
        self.lives -= 1

    def draw(self, screen, coords):
        x, y = coords
        for i in range(self.lives):
            screen.blit(self.car, (x + (i*self.width), y))