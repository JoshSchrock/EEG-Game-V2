import pygame

class Viewer:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.font = pygame.font.SysFont(None, 48)

    def update(self):
        self.screen.fill(pygame.color.Color('forestgreen'))
        pygame.draw.rect(self.screen, pygame.color.Color('grey'),
                         ((self.screen.get_width() / 2) - 300, 0, 600, self.screen.get_height()))
        pygame.draw.rect(self.screen, pygame.color.Color('yellow'),
                         ((self.screen.get_width() / 2) - 305, 0, 10, self.screen.get_height()))
        pygame.draw.rect(self.screen, pygame.color.Color('yellow'),
                         ((self.screen.get_width() / 2) - 105, 0, 10, self.screen.get_height()))
        pygame.draw.rect(self.screen, pygame.color.Color('yellow'),
                         ((self.screen.get_width() / 2) + 95, 0, 10, self.screen.get_height()))
        pygame.draw.rect(self.screen, pygame.color.Color('yellow'),
                         ((self.screen.get_width() / 2) + 295, 0, 10, self.screen.get_height()))
        # draw pursuer
        self.game.player.draw(self.screen)
        self.game.enemy.draw(self.screen)

        img = self.font.render(self.game.display, True, pygame.color.Color('red'))
        self.screen.blit(img, (self.screen.get_width()/2, self.screen.get_height()/2))



        # update display
        pygame.display.update()
