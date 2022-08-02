import pygame
import random
import math
from button import Button
from event_handler import EventHandler
from image_handler import ImageHandler
from car import Car
import time
from player import Player


class Game:
    def __init__(self, eegInterfaces, frame_rate):
        self.frame_rate = frame_rate
        self.starttime = time.time()
        self.velocity = 1
        self.mode = 0
        self.player1 = Player(eegInterfaces[0], self.velocity, 0)
        self.player2 = Player(eegInterfaces[1], self.velocity, 1)
        self.p1choice = None
        self.p2choice = None

        self.settup()

    def settup(self):
        w, h = pygame.display.get_surface().get_size()
        self.player1.settup((w / 4, h))
        self.player2.settup(((3*w) / 4, h))
        print(self.player1.is_recording)
        print(self.player2.is_recording)

    def planning_time(self):
        self.display = str(round(time.time() - self.starttime, 1))

    def direction_selection(self):
        self.display = str(round(time.time() - self.starttime, 1))
        self.player1.update_slider()
        self.player2.update_slider()

    def simulate(self):
        self.player1.simulate(self.p1choice, self.p2choice)
        self.player2.simulate(self.p2choice, self.p1choice)

    def display(self, text):
        pass

    def run_one_cycle(self):
        self.player1.handle_events()
        self.player2.handle_events()

        if self.mode == 0:
            if time.time() - self.starttime >= 3:
                self.starttime = time.time()
                self.mode = 1
                self.player1.go_to_measure()
                self.player2.go_to_measure()
            else:
                self.planning_time()
        if self.mode == 1:
            if time.time() - self.starttime >= 5:
                self.starttime = time.time()
                self.mode = 2
                self.p1choice = self.player1.determine_direction()
                self.p2choice = self.player2.determine_direction()
                self.player1.go_to_sim(self.p1choice)
                self.player2.go_to_sim(self.p2choice)
            else:
                self.direction_selection()
        if self.mode == 2:
            if time.time() - self.starttime >= 5:
                self.starttime = time.time()
                self.mode = 0
                self.settup()
            else:
                self.simulate()


    def draw(self, screen, size):
        width, height = size
        self.player1.draw(screen, ((width/2) - 260, 150), (10, 150), (0, 250), ((width/2) - 10, 10))
        self.player2.draw(screen, (width - 260, 150), ((width / 2) + 10, 150), ((width / 2), 250), (width - 10, 10))






