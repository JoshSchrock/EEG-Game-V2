import pygame

class Viewer:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.font = pygame.font.SysFont(None, 48)

    def update(self):
        width, height = self.screen.get_size()
        self.screen.fill(pygame.color.Color('forestgreen'))
        pygame.draw.rect(self.screen, pygame.color.Color('grey'),
                         ((width / 4) - 150, 0, 300, height))
        pygame.draw.rect(self.screen, pygame.color.Color('yellow'),
                         ((width / 4) - 152, 0, 4, height))
        pygame.draw.rect(self.screen, pygame.color.Color('yellow'),
                         ((width / 4) - 52, 0, 4, height))
        pygame.draw.rect(self.screen, pygame.color.Color('yellow'),
                         ((width / 4) + 48, 0, 4, height))
        pygame.draw.rect(self.screen, pygame.color.Color('yellow'),
                         ((width / 4) + 148, 0, 4, height))
        pygame.draw.rect(self.screen, pygame.color.Color('grey'),
                         (((3 * width) / 4) - 150, 0, 300, height))
        pygame.draw.rect(self.screen, pygame.color.Color('yellow'),
                         (((3 * width) / 4) - 152, 0, 4, height))
        pygame.draw.rect(self.screen, pygame.color.Color('yellow'),
                         (((3 * width) / 4) - 52, 0, 4, height))
        pygame.draw.rect(self.screen, pygame.color.Color('yellow'),
                         (((3 * width) / 4) + 48, 0, 4, height))
        pygame.draw.rect(self.screen, pygame.color.Color('yellow'),
                         (((3 * width) / 4) + 148, 0, 4, height))

        plyr1 = self.font.render('Player 1', True, pygame.color.Color('black'))
        self.screen.blit(plyr1, (50, 50))
        img = self.font.render(self.game.display, True, pygame.color.Color('black'))
        self.screen.blit(img, ((width / 2) - 100, 50))
        img = self.font.render(self.game.warning_display, True, pygame.color.Color('red'))
        self.screen.blit(img, ((width / 4) - img.get_width()/2, height/2))

        plyr2 = self.font.render('Player 2', True, pygame.color.Color('black'))
        self.screen.blit(plyr2, (width / 2 + 50, 50))
        img = self.font.render(self.game.display, True, pygame.color.Color('black'))
        self.screen.blit(img, (width - 100, 50))
        img = self.font.render(self.game.warning_display, True, pygame.color.Color('red'))
        self.screen.blit(img, (3*(width / 4) - img.get_width()/2, height / 2))

        # draw game
        self.game.draw(self.screen, (width, height))


        # update display
        pygame.display.update()
