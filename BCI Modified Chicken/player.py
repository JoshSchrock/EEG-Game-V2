from car import Car
import pygame
from event_handler import EventHandler
from scoreboard import Scoreboard
from slider import Slider
from lives import Lives
import random

class Player:
    def __init__(self, eegInterface, velocity, control):
        self.eegInterface = eegInterface
        self.eventhandler = EventHandler(self, control)
        self.velocity = velocity
        self.list_of_inputs = []
        self.scoreboard = Scoreboard()
        self.score_to_add = None
        self.direction = None
        self.slider = Slider()
        self.lives = Lives(3, pygame.color.Color('blue'), 100, 100)
        self.sub_life = False
        self.random = None

    def settup(self, initpos):
        self.player = Car(pygame.color.Color('blue'), 0, self.velocity, initpos)
        self.enemy = Car(pygame.color.Color('red'), 1, self.velocity, initpos)
        self.slider.reset()
        if self.score_to_add:
            self.scoreboard.score += self.score_to_add
        if self.direction:
            self.scoreboard.moves.append(self.direction)
        if self.sub_life:
            self.lives.lives -= 1
            if self.lives.lives == 0:
                self.lives = Lives(3, pygame.color.Color('blue'), 100, 100)
                self.scoreboard.score = 0
        if self.eegInterface:
            self.eegInterface.add_control_marker(1)
            self.eegInterface.add_control_marker(self.scoreboard.score + 100)
            self.eegInterface.add_control_marker(self.lives.lives + 20)

    def go_to_measure(self):
        self.random = random.randint(0, 6) / 3
        self.list_of_inputs = []
        if self.eegInterface:
            self.eegInterface.add_control_marker(2)

    def go_to_sim(self):
        if self.eegInterface:
            self.eegInterface.add_control_marker(3)

    def simulate(self, urchoice, thrchoice):
        w, h = pygame.display.get_surface().get_size()
        if urchoice == 1:
            self.direction = 'Center'
        elif urchoice == 0:
            self.direction = 'Left'
        else:
            self.direction = 'Right'

        if (urchoice + thrchoice) / 2 == 1:
            collision = True
            self.score_to_add = -25
            self.sub_life = True
        else:
            collision = False
            self.sub_life = False
            if urchoice == 1:
                self.score_to_add = 5
            else:
                self.score_to_add = 1

        if self.player.y <= h / 2 + 100 or self.enemy.y >= h / 2 - 100:
            if not self.player.choicestart:
                self.player.choicestart = pygame.time.get_ticks() / 1000
                self.enemy.choicestart = pygame.time.get_ticks() / 1000
            self.player.make_choice(urchoice, collision)
            self.enemy.make_choice(thrchoice, collision)

        self.player.move()
        self.enemy.move()

    def determine_direction(self):
        if len(self.list_of_inputs) > 0:
            avg = sum(self.list_of_inputs) / len(self.list_of_inputs)
            if 0 <= avg < 0.75:
                self.list_of_inputs = []
                return 0
            elif 0.75 <= avg < 1.25:
                self.list_of_inputs = []
                return 1
            else:
                self.list_of_inputs = []
                return 2
        else:
            return 1

    def handle_events(self):
        self.eventhandler.get_and_handle_events()

    def update_slider(self):
        if len(self.list_of_inputs) > 0:
            avg = sum(self.list_of_inputs) / len(self.list_of_inputs)
            self.slider.update(avg)

    def draw(self, screen, scoreboard, slider, lives):
        self.player.draw(screen)
        self.enemy.draw(screen)
        self.slider.draw(screen, slider)
        self.scoreboard.draw(screen, scoreboard)
        self.lives.draw(screen, lives)

