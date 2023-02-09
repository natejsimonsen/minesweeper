import pygame
from Colors import Colors


class MenuManager:
    def __init__(self, screen):
        self.current_element = StartMenu(screen)

    def draw(self):
        self.current_element.draw()


class StartMenu:
    def __init__(self, screen):
        self.font = pygame.font.SysFont("Arial", 30, Colors.TEXT)
        self.screen = screen
        self.width, self.height = pygame.display.get_surface().get_size()

    def draw_font(self, text):
        font = self.font.render(text, True, Colors.TEXT)

        font_rect = font.get_rect(center=(self.width / 2, self.height / 2))
        self.screen.blit(font, font_rect)

    def draw(self):
        self.draw_font("Click to start the game")
