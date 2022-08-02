import pygame
from game import Game
from viewer import Viewer
from eeg_interface import EEGInterface
import os


def main():
    pygame.init()
    pygame.display.set_caption("Modified Chicken")  # title on top of game window

    screen1 = pygame.display.set_mode((1800, 900), pygame.RESIZABLE)  # DONE: Choose your own size
    clock = pygame.time.Clock()
    frame_rate = 120  # game and display rate

    #  client connection to cortex
    your_app_client_id = 'BN6wnwY8b9ZKYAQmTUCJLHBx0UVQ1VE52QN4I9Ha'
    your_app_client_secret = 'WSdbaAxrMqkNvqRvMYW8ZsLXWNuNb3XJGk4cnxXebQb3A43bl7L21AEvr7aiQqOepIo01K74ixfDSKPb1QBhUPPX9EOewegV4kYZCJceDiGBZFfAKrSN5MIpTQroOhg6'
    your_app_license = 'd5b584b8-883e-421f-8bf5-cbe4bcb0ac72'


    #  recording settings
    export_folder = 'Test'
    record_export_folder = f'{os.getcwd()}\\EEGExports\\{export_folder}' # your place to export, you should have write
    # permission, example on desktop
    record_export_format = 'EDF'
    record_export_version = 'V2'

    #  headset and profile settings
    headset_1 = 'EPOCFLEX-F0000172'
    headset_2 = 'EPOCFLEX-F000015B'
    profile_name_1 = "Josh Schrock"
    profile_name_2 = "Patrick"

    eegInterface1 = EEGInterface(your_app_client_id, your_app_client_secret, your_app_license, record_export_folder,
                                 record_export_format, record_export_version, headset_1, profile_name_1)
    eegInterface2 = EEGInterface(your_app_client_id, your_app_client_secret, your_app_license, record_export_folder,
                                 record_export_format, record_export_version, headset_2, profile_name_2)

    game = Game([eegInterface1, eegInterface2], frame_rate)  # Methods of game operation
    viewer = Viewer(screen1, game)  # display the game

    while True:
        clock.tick(frame_rate)
        game.run_one_cycle()
        viewer.update()

if __name__ == "__main__":
    main()

