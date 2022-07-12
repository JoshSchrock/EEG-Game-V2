import math

import pygame

class Car:
    def __init__(self, color, player, velocity):
        self.color = color
        self.width = 100
        self.height = 100
        self.velocity = velocity
        self.car = pygame.image.load('car.png')
        self.car = pygame.transform.scale(self.car, (self.width, self.height))
        # self.car.set_colorkey(pygame.color.Color('white'))
        w, h = pygame.display.get_surface().get_size()
        self.choicestart = None

        if player == 0:
            self.x = w / 2
            self.y = h - 100
            self.direction = (0, -1)
        else:
            var = pygame.PixelArray(self.car)
            var.replace((242, 173, 18), pygame.color.Color('blue'))
            var.close()
            del var
            self.x = w / 2
            self.y = 100
            self.direction = (0, 1)

        cur_angle = math.pi/2
        angle = math.atan2(self.direction[1], self.direction[0])
        self.car = pygame.transform.rotate(self.car, math.degrees(angle + cur_angle))
        self.car_rect = self.car.get_rect(center=self.car.get_rect(center=(self.x, self.y)).center)

    def move(self):
        self.x += self.velocity * self.direction[0]
        self.y += self.velocity * self.direction[1]
        self.car_rect = self.car.get_rect(center=self.car.get_rect(center=(self.x, self.y)).center)

    def make_choice(self, choice):
        timeElapsed = (pygame.time.get_ticks() / 1000) - self.choicestart
        cur_angle = math.atan2(-self.direction[1], self.direction[0])
        omega = timeElapsed * 4
        if choice == 0:
            if omega <= 2*math.pi:
                difference = -math.sin(omega)/50
                angle = cur_angle + difference
                self.direction = (math.cos(angle), -math.sin(angle))
                rotated_image = pygame.transform.rotate(self.car, math.degrees(difference))
                self.car_rect = rotated_image.get_rect(center=self.car.get_rect(center=(self.x, self.y)).center)
                self.car = rotated_image


    def draw(self, screen):
        screen.blit(self.car, self.car_rect.topleft)
