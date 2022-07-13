import math
from explosion import Explosion
import pygame

class Car:
    def __init__(self, color, player, velocity, initpos):
        self.color = color
        self.width = 100
        self.height = 100
        self.velocity = velocity
        self.car = pygame.image.load('car.png')
        self.car = pygame.transform.scale(self.car, (self.width, self.height))
        self.car.set_colorkey(pygame.color.Color('white'))
        self.choicestart = None
        self.explosion_group = pygame.sprite.Group()
        self.explosion_sound = pygame.mixer.Sound("Explosion.mp3")
        self.is_dead = False

        if player == 0:
            self.x = initpos[0]
            self.y = initpos[1] - 100
            self.direction = (0, -1)
        else:
            var = pygame.PixelArray(self.car)
            var.replace((242, 173, 18), pygame.color.Color('blue'))
            var.close()
            del var
            self.x = initpos[0]
            self.y = 100
            self.direction = (0, 1)

        cur_angle = math.pi/2
        angle = math.atan2(self.direction[1], self.direction[0])
        self.car = pygame.transform.rotate(self.car, math.degrees(angle + cur_angle))
        self.car_rect = self.car.get_rect(center=self.car.get_rect(center=(self.x, self.y)).center)

    def move(self):
        if not self.is_dead:
            self.x += self.velocity * self.direction[0]
            self.y += self.velocity * self.direction[1]
            self.car_rect = self.car.get_rect(center=self.car.get_rect(center=(self.x, self.y)).center)

    def make_choice(self, choice, collision):
        timeElapsed = (pygame.time.get_ticks() / 1000) - self.choicestart
        cur_angle = math.atan2(-self.direction[1], self.direction[0])
        omega = timeElapsed * 4
        if choice == 0:
            if omega <= 2*math.pi:
                difference = math.sin(omega)/50
                angle = cur_angle + difference
                self.direction = (math.cos(angle), -math.sin(angle))
                rotated_image = pygame.transform.rotate(self.car, math.degrees(difference))
                # self.car_rect = rotated_image.get_rect(center=self.car.get_rect(center=(self.x, self.y)).center)
                #self.car = rotated_image
        if choice == 2:
            if omega <= 2*math.pi:
                difference = -math.sin(omega)/50
                angle = cur_angle + difference
                self.direction = (math.cos(angle), -math.sin(angle))
                rotated_image = pygame.transform.rotate(self.car, math.degrees(difference))
                # self.car_rect = rotated_image.get_rect(center=self.car.get_rect(center=(self.x, self.y)).center)
                #self.car = rotated_image

        if collision and timeElapsed >= 0.8:
            self.explode()

    def explode(self):
        self.explosion_sound.play()
        self.is_dead = True
        self.explosion_group.add(Explosion(self.x, self.y))


    def draw(self, screen):
        self.explosion_group.draw(screen)
        self.explosion_group.update()
        if not self.is_dead:
            screen.blit(self.car, self.car_rect.topleft)
