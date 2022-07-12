import pygame
import random
import math
from button import Button
from event_handler import EventHandler
from image_handler import ImageHandler
from car import Car
import time


class Game:
    def __init__(self, eegInterfaces, frame_rate):
        self.eegInterfaces = eegInterfaces
        self.frame_rate = frame_rate
        self.starttime = time.time()
        self.velocity = 1
        self.mode = 0

        self.settup()

    def settup(self):
        self.player = Car(pygame.color.Color('blue'), 0, self.velocity)
        self.enemy = Car(pygame.color.Color('red'), 1, self.velocity)

    def planning_time(self):
        self.display = str(time.time() - self.starttime)

    def direction_selection(self):
        self.display = str(time.time() - self.starttime)

    def simulate(self):
        w, h = pygame.display.get_surface().get_size()
        if self.player.y <= h / 2 + 100 or self.enemy.y >= h / 2 - 100:
            if not self.player.choicestart:
                self.player.choicestart = pygame.time.get_ticks() / 1000
                self.enemy.choicestart = pygame.time.get_ticks() / 1000
            self.player.make_choice(0)
            self.enemy.make_choice(0)
        self.player.move()
        self.enemy.move()

    def display(self, text):
        pass

    def run_one_cycle(self):
        events = EventHandler(self)
        if self.mode == 0:
            if time.time() - self.starttime >= 1:
                self.starttime = time.time()
                self.mode = 1
            else:
                self.planning_time()
        if self.mode == 1:
            if time.time() - self.starttime >= 1:
                self.starttime = time.time()
                self.mode = 2
            else:
                self.direction_selection()
        if self.mode == 2:
            if time.time() - self.starttime >= 5:
                self.starttime = time.time()
                self.mode = 0
                self.settup()
            else:
                self.simulate()





