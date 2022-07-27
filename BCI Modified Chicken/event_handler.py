import pygame
import sys

class EventHandler:
    def __init__(self, player):
        self.player = player
        self.last_marker = None

    def get_and_handle_events(self):
        self.ManualController()
        self.EEGController()


    # manual controls to pursue - implemented for testing purposes
    def ManualController(self):
        events = pygame.event.get()
        self.exit_if_time_to_quit(events)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_LEFT]:
            self.player.list_of_inputs.append(0)
        if pressed_keys[pygame.K_DOWN]:
            self.player.list_of_inputs.append(1)
        if pressed_keys[pygame.K_RIGHT]:
            self.player.list_of_inputs.append(2)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F5:
                    self.player.eegInterface.createRecording()
                if event.key == pygame.K_F6:
                    self.player.eegInterface.endRecording()



    # controls given to pursuer
    def EEGController(self):
        if self.player.eegInterface.streamLineData():
            action = self.player.eegInterface.streamLineData()[0]
            power = self.player.eegInterface.streamLineData()[1]
            # left
            if action == "left":
                self.player.list_of_inputs.append(0)
                if self.last_marker != 'left':
                    self.player.eegInterface.add_control_marker(10)
                    self.last_marker = 'left'
            # right
            if action == "right":
                self.player.list_of_inputs.append(2)
                if self.last_marker != 'right':
                    self.player.eegInterface.add_control_marker(12)
                    self.last_marker = 'right'
            if action == 'neutral':
                self.player.list_of_inputs.append(1)
                if self.last_marker != 'neutral':
                    self.player.eegInterface.end_control_marker(11)
                    self.last_marker = 'neutral'


    @staticmethod
    def exit_if_time_to_quit(events):
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()

    @staticmethod
    def key_was_pressed_on_this_cycle(key, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == key:
                return True
        return False