import pygame

class Scoreboard:
    def __init__(self):
       self.score = 0
       self.moves = []
       self.font1 = pygame.font.SysFont(None, 48)
       self.font2 = pygame.font.SysFont(None, 26)

    def draw(self, screen, coords):
        x, y = coords
        pygame.draw.rect(screen, pygame.color.Color('white'), (x, y, 250, 400), width=5)
        score = self.font1.render(f'Score: {str(self.score)}', True, pygame.color.Color('black'))
        screen.blit(score, (x + 25, y + 25))
        moves = self.font1.render('Moves: ', True, pygame.color.Color('black'))
        screen.blit(moves, (x + 25, y + 75))
        for i in range(len(self.moves)):
            move = self.font2.render(self.moves[i], True, pygame.color.Color('black'))
            screen.blit(move, (x + 25 + (75 * (i // 14)), y + 110 + (20 * i) - (280 * (i // 14))))
