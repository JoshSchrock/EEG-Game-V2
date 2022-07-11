import pygame
import sys

class EventHandler:
    def __init__(self, game):
        self.game = game
        self.last_marker = None

    def get_and_handle_events(self):
        self.ManualController()
        self.EEGController()


    # manual controls to pursue - implemented for testing purposes
    def ManualController(self):
        events = pygame.event.get()
        self.exit_if_time_to_quit(events)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_LEFT] and self.game.pursuePos[0] > self.game.velocity:
            self.game.pursuePos[0] -= self.game.velocity
        if pressed_keys[pygame.K_RIGHT] and self.game.pursuePos[0] < 1000 - self.game.width - self.game.velocity:
            self.game.pursuePos[0] += self.game.velocity
        if pressed_keys[pygame.K_UP] and self.game.pursuePos[1] > self.game.velocity:
            self.game.pursuePos[1] -= self.game.velocity
        if pressed_keys[pygame.K_DOWN] and self.game.pursuePos[1] < 1000 - self.game.height - self.game.velocity:
            self.game.pursuePos[1] += self.game.velocity

        mousex, mousey = pygame.mouse.get_pos()
        if self.game.close_button.isOver((mousex, mousey)):
            self.game.close_button.outline = 20
        else:
            self.game.close_button.outline = 0

        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and self.game.close_button.isOver((mousex, mousey)):
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F5:
                    for eeg in self.game.eegInterfaces:
                        eeg.createRecording()
                if event.key == pygame.K_F6:
                    for eeg in self.game.eegInterfaces:
                        eeg.endRecording()



    # controls given to pursuer
    def EEGController(self):
        cumHorDir = 0
        cumVerDir = 0
        for eeg in self.game.eegInterfaces:
            action = eeg.streamLineData()[0]
            power = eeg.streamLineData()[1]
            # left
            if action == "left" and self.game.pursuePos[0] > self.game.velocity:
                cumHorDir -= power
                if self.last_marker != 'left':
                    eeg.add_control_marker(2)
                    self.last_marker = 'left'
            # right
            if action == "right" and self.game.pursuePos[0] < 1000 - self.game.width - self.game.velocity:
                cumHorDir += power
                if self.last_marker != 'right':
                    eeg.add_control_marker(3)
                    self.last_marker = 'right'
            # up
            if action == "lift" and self.game.pursuePos[1] > self.game.velocity:
                cumVerDir -= power
                if self.last_marker != 'lift':
                    eeg.add_control_marker(4)
                    self.last_marker = 'lift'
            # down
            if action == "drop" and self.game.pursuePos[1] < 1000 - self.game.height - self.game.velocity:
                cumVerDir += power
                if self.last_marker != 'drop':
                    eeg.add_control_marker(5)
                    self.last_marker = 'drop'
            if action == 'neutral':
                if self.last_marker != 'neutral':
                    eeg.end_control_marker()
                    self.last_marker = 'neutral'

        self.game.pursuePos[0] += (cumHorDir / len(self.game.eegInterfaces)) * self.game.velocity
        self.game.pursuePos[1] += (cumVerDir / len(self.game.eegInterfaces)) * self.game.velocity


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