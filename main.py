import pygame
from Game import Game
from Camera import Camera

width = 1080
height = 720

camera = Camera(width, height, 1)

pygame.init()
screen = pygame.display.set_mode([width, height])
running = True
game = Game(screen, camera)
mouse_coords = (None, None)
dragging = False

if __name__ == "__main__":
    while running:
        left_button = pygame.mouse.get_pressed(3)[0]
        if left_button:
            x, y = mouse_coords
            if x is None and y is None:
                mouse_coords = pygame.mouse.get_pos()
            else:
                current_x, current_y = pygame.mouse.get_pos()
                camera.move_x(current_x - x)
                camera.move_y(current_y - y)
                mouse_coords = pygame.mouse.get_pos()
                if (current_y - y) != 0 and (current_x - x) != 0:
                    dragging = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_EQUALS:
                    camera.zoom += .1
                if event.key == pygame.K_MINUS:
                    camera.zoom -= .1
                # if event.key == pygame.K_LEFT:
                #     camera.offset_x -= 50

                # this moves the camera with the different keys
                # if event.key == pygame.K_RIGHT:
                #     camera.offset_x += 50
                # if event.key == pygame.K_UP:
                #     camera.offset_y -= 50
                # if event.key == pygame.K_DOWN:
                #     camera.offset_y += 50
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_coords = (None, None)
                if not dragging:
                    game.handle_click(event, pygame.mouse.get_pos())
                dragging = False

        game.draw()
        pygame.display.flip()

    pygame.quit()
