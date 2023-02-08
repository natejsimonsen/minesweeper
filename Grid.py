import math
import random
import pygame
from Colors import Colors


class Grid:
    INERT = 0
    MINE = 1
    COVERED = 0
    UNCOVERED = 1

    def __init__(self, screen, camera, font):
        self.screen = screen
        self.rows = 14
        self.cols = 35
        self.square_size = 80
        self.font = pygame.font.SysFont(None, self.square_size * 3 // 4)
        self.mine_rate = .2
        self.num_current_mines = 0
        self.camera = camera
        self.width = self.cols * self.square_size * self.camera.zoom
        self.height = self.rows * self.square_size * self.camera.zoom
        self.camera.center_around_element(self.width, self.height)
        self.grid = self.generate_grid()
        self.flags = []
        self.mines = []
        self.debug = False
        self.end_of_game = False

    def generate_mines(self, clicked_row, clicked_col):
        total_tiles = self.rows * self.cols
        total_mines = math.floor(math.ceil(total_tiles // 5) * 5 * self.mine_rate)

        all_tiles = [(clicked_row, clicked_col)]
        for cell in self.get_surrounding_cells(clicked_row, clicked_col):
            all_tiles.append(cell)

        while self.num_current_mines != total_mines:
            random_row = random.randrange(0, self.rows)
            random_col = random.randrange(0, self.cols)

            if self.grid[random_row][random_col][1] != Grid.MINE and (random_row, random_col) not in all_tiles:
                self.grid[random_row][random_col][1] = Grid.MINE
                self.mines.append((random_row, random_col))
                self.num_current_mines += 1

    def generate_mine_map(self):
        for i, row in enumerate(self.grid):
            for j, col in enumerate(row):
                covered, tile_type, num_surrounding_mines = col
                if tile_type != Grid.MINE:
                    surrounding_cells = self.get_surrounding_cells(i, j)
                    num_mines = 0
                    for s_row, s_col in surrounding_cells:
                        covered, tile_type, num_surrounding_mines = self.grid[s_row][s_col]
                        if tile_type == Grid.MINE:
                            num_mines += 1
                    self.grid[i][j][2] = num_mines

    def get_surrounding_cells(self, row, col):
        surrounding_cells = []
        if row - 1 >= 0 and col - 1 >= 0:
            surrounding_cells.append((row - 1, col - 1))
        if row - 1 >= 0:
            surrounding_cells.append((row - 1, col))
        if row - 1 >= 0 and col + 1 < self.cols:
            surrounding_cells.append((row - 1, col + 1))
        if col - 1 >= 0:
            surrounding_cells.append((row, col - 1))
        if col + 1 < self.cols:
            surrounding_cells.append((row, col + 1))
        if row + 1 < self.rows and col - 1 >= 0:
            surrounding_cells.append((row + 1, col - 1))
        if row + 1 < self.rows:
            surrounding_cells.append((row + 1, col))
        if row + 1 < self.rows and col + 1 < self.cols:
            surrounding_cells.append((row + 1, col + 1))

        return surrounding_cells

    def generate_grid(self):
        grid = []
        for row in range(self.rows):
            grid.append([])
            for col in range(self.cols):
                grid[row].append([Grid.COVERED, Grid.INERT, 0])
        return grid

    def check_for_win(self):
        if sorted(self.flags) == sorted(self.mines):
            print("you win!")

    def handle_click(self, event, mouse_position):
        mouse_x, mouse_y = mouse_position
        row = int(abs((self.camera.offset_y - mouse_y) // (self.square_size * self.camera.zoom)) - 1)
        col = int(abs((self.camera.offset_x - mouse_x) // (self.square_size * self.camera.zoom)) - 1)

        if self.num_current_mines == 0:
            self.generate_mines(row, col)
            self.generate_mine_map()

        if event.button == 3:  # right click
            if (row, col) not in self.flags:
                self.flags.append((row, col))
                self.check_for_win()
            else:
                self.flags.remove((row, col))
        elif (row, col) not in self.flags:
            if self.grid[row][col][1] == Grid.MINE:
                print("You lose")
                self.end_of_game = True
                return
            self.grid[row][col][0] = Grid.UNCOVERED
            self.reveal_surrounding_cells(row, col)

    def reveal_surrounding_cells(self, row, col, zero_cells_to_remove=None):
        surrounding_cells = self.get_surrounding_cells(row, col)

        if not zero_cells_to_remove:
            zero_cells_to_remove = []

        for i, k in surrounding_cells:
            covered, tile_type, num_surrounding_mines = self.grid[i][k]
            # reveal cell
            if covered == Grid.COVERED and tile_type == Grid.INERT and num_surrounding_mines == 0:
                zero_cells_to_remove.append((i, k))

        if self.grid[row][col][2] == 0 and self.grid[row][col][1] == Grid.INERT:
            for i, k in surrounding_cells:
                self.grid[i][k][0] = Grid.UNCOVERED

        for i, k in zero_cells_to_remove:
            self.grid[i][k][0] = Grid.UNCOVERED
            zero_cells_to_remove.remove((i, k))
            for row, col in self.get_surrounding_cells(i, k):
                self.grid[row][col][0] = Grid.UNCOVERED
                self.reveal_surrounding_cells(row, col, zero_cells_to_remove)

    def draw_font(self, text, position):
        font = self.font.render(text, True, Colors.TEXT)
        self.screen.blit(font, position)

    def draw(self):
        for i, row in enumerate(self.grid):
            for j, col in enumerate(row):
                covered, tile_type, num_surrounding_mines = col
                square_color = Colors.ALT_SQUARE
                surrounding_mines_text = ""

                if covered == Grid.UNCOVERED and tile_type == Grid.INERT and num_surrounding_mines != 0:
                    surrounding_mines_text = str(num_surrounding_mines)

                if (i + j) % 2 == 0:
                    square_color = Colors.SQUARE

                if covered == Grid.UNCOVERED:
                    square_color = Colors.UNCOVERED_SQUARE
                    if (i + j) % 2 == 1:
                        square_color = Colors.UNCOVERED_SQUARE_ALT

                if (i, j) in self.flags:
                    square_color = Colors.FLAG

                if tile_type == Grid.MINE and self.end_of_game:
                    square_color = Colors.MINE

                rect = (
                    j * self.square_size * self.camera.zoom + self.camera.offset_x,
                    i * self.square_size * self.camera.zoom + self.camera.offset_y,
                    self.square_size * self.camera.zoom,
                    self.square_size * self.camera.zoom
                )
                pygame.draw.rect(self.screen, square_color, rect)
                text = self.font.render(surrounding_mines_text, True, Colors.TEXT)
                text_rect = text.get_rect(center=(
                rect[0] + self.square_size * self.camera.zoom // 2, rect[1] + self.square_size * self.camera.zoom // 2))
                self.screen.blit(text, text_rect)

                if self.debug:
                    self.draw_font(
                        f"{i}, {j}",
                        (
                            j * self.square_size + self.square_size // 4 + self.camera.offset_x,
                            i * self.square_size + self.square_size // 4 + self.camera.offset_y
                        )
                    )
