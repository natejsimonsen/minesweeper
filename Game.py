import pygame
from Colors import Colors
from Grid import Grid

pygame.init()


class Game:
    def __init__(self, screen, camera):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 38)
        self.camera = camera
        self.grid = Grid(self.screen, camera, self.font)

    def handle_click(self, event, mouse_position):
        self.grid.handle_click(event, mouse_position)

    def draw_font(self, text, position):
        font = self.font.render(text, True, Colors.TEXT)
        self.screen.blit(font, position)

    def draw(self):
        self.screen.fill(Colors.BG)
        self.grid.draw()
        self.draw_font(f"Mines: {self.grid.num_current_mines}, Flags: {len(self.grid.flags)}", (20, 20))
