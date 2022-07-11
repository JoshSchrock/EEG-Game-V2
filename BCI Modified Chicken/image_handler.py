import pygame

class ImageHandler:
    def __init__(self, image, location, size):
        self.image = pygame.image.load(image)
        self.location = location
        self.image = pygame.transform.scale(self.image, size)

    def draw(self, screen):
        screen.blit(self.image, self.location)
