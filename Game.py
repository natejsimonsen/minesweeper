import pygame
from Colors import Colors
from Grid import Grid
from GameState import GameState
from MenuManager import MenuManager

pygame.init()


class Game:
    def __init__(self, screen, camera):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 38)
        self.camera = camera
        self.grid = Grid(self.screen, camera, self.font)
        self.menus = MenuManager(screen)
        self.state = GameState().state

    def restart(self):
        self.grid = Grid(self.screen, self.camera, self.font)
        self.menus = MenuManager(self.screen)
        self.state = GameState().state

    def handle_click(self, event, mouse_position):
        if self.state["lost"] or self.state['won']:
            self.restart()

        if self.state["playing"]:
            self.grid.handle_click(event, mouse_position)
            if self.grid.lost:
                self.state['lost'] = True
                self.state['playing'] = False
            if self.grid.won:
                self.state['won'] = True
                self.state['playing'] = False

        if self.state["start"]:
            self.state["start"] = False
            self.state["playing"] = True
            self.menus.current_element = self.grid

    def draw_font(self, text, position):
        font = self.font.render(text, True, Colors.TEXT)
        self.screen.blit(font, position)

    def draw(self):
        self.screen.fill(Colors.BG)
        self.menus.draw()
