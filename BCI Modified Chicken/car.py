import pygame

class Car:
    def __init__(self, color, player, velocity):
        self.color = color
        self.width = 50
        self.height = 50
        self.velocity = velocity
        self.car = pygame.image.load('car.png')
        self.car = pygame.transform.scale(self.car, (self.width, self.height))
        w, h = pygame.display.get_surface().get_size()

        if player == 0:
            self.x = w / 2
            self.y = h - 100
            self.direction = (0, 1)
        else:
            var = pygame.PixelArray(self.car)
            var.replace((242, 173, 18), pygame.color.Color('red'))
            var.close()
            self.x = w / 2
            self.y = 100
            self.direction = (0, -1)

    def move(self):
        self.x += self.velocity * self.direction[0]
        self.y += self.velocity * self.direction[1]

    def make_choice(self, choice):
        pass

    def draw(self, screen):
        self.car.set_colorkey(pygame.color.Color('white'))
        screen.blit(self.car, (self.x - (0.5 * self.width), self.y - (0.5 * self.height)))
