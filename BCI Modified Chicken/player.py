from car import Car
import pygame
from event_handler import EventHandler
from scoreboard import Scoreboard
from slider import Slider
from lives import Lives
import random
import time
import numpy as np

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
        self.is_recording = False
        self.record = None

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
        if self.is_recording:
            self.record = np.concatenate((self.record, np.array([[time.time(), 1, -1]])), axis=0)
        if self.eegInterface is not None:
            self.eegInterface.add_control_marker(1)
            time.sleep(0.1)
            self.eegInterface.add_control_marker(self.scoreboard.score + 100)
            time.sleep(0.1)
            self.eegInterface.add_control_marker(self.lives.lives + 20)
            time.sleep(0.1)

    def go_to_measure(self):
        self.random = random.randint(0, 6) / 3
        self.list_of_inputs = []
        if self.is_recording:
            self.record = np.concatenate((self.record, np.array([[time.time(), 2, -1]])), axis=0)
        if self.eegInterface is not None:
            self.eegInterface.add_control_marker(2)
            time.sleep(0.1)

    def go_to_sim(self, choice):
        if self.is_recording:
            self.record = np.concatenate((self.record, np.array([[time.time(), 3, choice]])), axis=0)
        if self.eegInterface is not None:
            self.eegInterface.add_control_marker(3)
            time.sleep(0.1)

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
            self.score_to_add = -10
            self.sub_life = True
        else:
            collision = False
            self.sub_life = False
            if urchoice == 1:
                self.score_to_add = 5
            elif thrchoice == 1:
                self.score_to_add = 0
            else:
                self.score_to_add = 3

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

    def begin_recording(self):
        self.eegInterface.createRecording()
        self.record = np.array([[time.time(), -1, -1]])
        self.is_recording = True

    def end_Recording(self):
        self.eegInterface.endRecording()
        self.record = np.concatenate((self.record, np.array([[time.time(), -1, -1]])), axis=0)
        file = f'{self.eegInterface.record_export_folder}\\EEG-Game_{self.eegInterface.profile_name}_{self.eegInterface.headset_id}_{time.time()}_actions'
        print(self.record)
        np.save(file, self.record)
        self.is_recording = False

    def draw(self, screen, scoreboard, slider, lives, record):
        self.player.draw(screen)
        self.enemy.draw(screen)
        self.slider.draw(screen, slider)
        self.scoreboard.draw(screen, scoreboard)
        self.lives.draw(screen, lives)
        if self.is_recording:
            pygame.draw.circle(screen, pygame.color.Color('red'), record, 5)

