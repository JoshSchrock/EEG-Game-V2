import pygame

class Viewer:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.font = pygame.font.SysFont(None, 48)

    def update(self):
        self.screen.fill(pygame.color.Color('forestgreen'))
        pygame.draw.rect(self.screen, pygame.color.Color('grey'),
                         ((self.screen.get_width() / 4) - 150, 0, 300, self.screen.get_height()))
        pygame.draw.rect(self.screen, pygame.color.Color('yellow'),
                         ((self.screen.get_width() / 4) - 152, 0, 4, self.screen.get_height()))
        pygame.draw.rect(self.screen, pygame.color.Color('yellow'),
                         ((self.screen.get_width() / 4) - 52, 0, 4, self.screen.get_height()))
        pygame.draw.rect(self.screen, pygame.color.Color('yellow'),
                         ((self.screen.get_width() / 4) + 48, 0, 4, self.screen.get_height()))
        pygame.draw.rect(self.screen, pygame.color.Color('yellow'),
                         ((self.screen.get_width() / 4) + 148, 0, 4, self.screen.get_height()))
        pygame.draw.rect(self.screen, pygame.color.Color('grey'),
                         (((3* self.screen.get_width()) / 4) - 150, 0, 300, self.screen.get_height()))
        pygame.draw.rect(self.screen, pygame.color.Color('yellow'),
                         (((3* self.screen.get_width()) / 4) - 152, 0, 4, self.screen.get_height()))
        pygame.draw.rect(self.screen, pygame.color.Color('yellow'),
                         (((3* self.screen.get_width()) / 4) - 52, 0, 4, self.screen.get_height()))
        pygame.draw.rect(self.screen, pygame.color.Color('yellow'),
                         (((3* self.screen.get_width()) / 4) + 48, 0, 4, self.screen.get_height()))
        pygame.draw.rect(self.screen, pygame.color.Color('yellow'),
                         (((3* self.screen.get_width()) / 4) + 148, 0, 4, self.screen.get_height()))

        plyr1 = self.font.render('Player 1', True, pygame.color.Color('black'))
        self.screen.blit(plyr1, (50, 50))
        img = self.font.render(self.game.display, True, pygame.color.Color('black'))
        self.screen.blit(img, ((self.screen.get_width() / 2) - 100, 50))

        plyr2 = self.font.render('Player 2', True, pygame.color.Color('black'))
        self.screen.blit(plyr2, (self.screen.get_width() / 2 + 50, 50))
        img = self.font.render(self.game.display, True, pygame.color.Color('black'))
        self.screen.blit(img, (self.screen.get_width() - 100, 50))

        # draw pursuer
        self.game.draw(self.screen)


        # update display
        pygame.display.update()
