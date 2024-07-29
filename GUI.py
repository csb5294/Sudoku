# TODO the reset button doesn't actually work

import pygame
import Engine

win = pygame.display.set_mode((750, 850))


class Button:

    def __init__(self, text, width, height, x, y):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = (x, y, width, height)

    def draw(self):
        pygame.draw.rect(win, (160, 160, 160), self.rect)
        font = pygame.font.SysFont("comicsans", 25)
        text = font.render(str(self.text), 1, (0, 0, 0))
        win.blit(text,
                 (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))


class Tile:

    def __init__(self, value, temp, is_selected, row, col, width):
        self.value = value
        self.temp = temp
        self.is_selected = is_selected
        self.row = row
        self.col = col
        self.width = width / 9

    def draw(self):

        x = self.width * self.col
        y = self.width * self.row

        if self.temp != 0 and self.value == 0:
            # pencil mark
            font = pygame.font.SysFont("comicsans", 20)
            text = font.render(str(self.temp), 1, (128, 128, 128))
            win.blit(text, (x + 7, y + 1))
        elif self.value != 0:
            # real mark
            font = pygame.font.SysFont("comicsans", 40)
            text = font.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (self.width / 2 - text.get_width() / 2), y + (self.width / 2 - text.get_height() / 2)))

        if self.is_selected:
            # outline
            pygame.draw.rect(win, (255, 0, 0), (x, y, self.width, self.width), 3)


class GUI:

    def __init__(self):
        pygame.init()
        self.start_time = pygame.time.get_ticks()
        self.ticks = self.start_time

        self.board = [[3, 0, 6, 5, 0, 8, 4, 0, 0],
                      [5, 2, 0, 0, 0, 0, 0, 0, 0],
                      [0, 8, 7, 0, 0, 0, 0, 3, 1],
                      [0, 0, 3, 0, 1, 0, 0, 8, 0],
                      [9, 0, 0, 8, 6, 3, 0, 0, 5],
                      [0, 5, 0, 0, 9, 0, 6, 0, 0],
                      [1, 3, 0, 0, 0, 0, 2, 5, 0],
                      [0, 0, 0, 0, 0, 0, 0, 7, 4],
                      [0, 0, 5, 2, 0, 6, 3, 0, 0]]

        self.board_height = 750
        self.board_width = 750
        self.strikes = 0
        self.running = True
        self.tiles = [[Tile(0, 0, False, 0, 0, 0) for a in range(9)] for b in range(9)]
        self.refresh_tiles()
        self.solve_button = Button("Solve", 125, 50, 50, 780)
        self.reset_button = Button("Reset", 125, 50, 200, 780)
        self.refresh()
        pygame.display.flip()

    def refresh_tiles(self):
        for i in range(9):
            for j in range(9):
                self.tiles[i][j] = Tile(self.board[i][j], 0, False, i, j, self.board_width)

    def reset_board(self):
        self.board = [[3, 0, 6, 5, 0, 8, 4, 0, 0],
                      [5, 2, 0, 0, 0, 0, 0, 0, 0],
                      [0, 8, 7, 0, 0, 0, 0, 3, 1],
                      [0, 0, 3, 0, 1, 0, 0, 8, 0],
                      [9, 0, 0, 8, 6, 3, 0, 0, 5],
                      [0, 5, 0, 0, 9, 0, 6, 0, 0],
                      [1, 3, 0, 0, 0, 0, 2, 5, 0],
                      [0, 0, 0, 0, 0, 0, 0, 7, 4],
                      [0, 0, 5, 2, 0, 6, 3, 0, 0]]

    def draw(self):
        # gridlines
        gap = win.get_width() / 9
        for i in range(10):
            if i % 3 == 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, (0, 0, 0), (0, i * gap), (self.board_width, i * gap), thick)
            pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.board_height), thick)

        self.draw_tiles()

    def handle_click(self, pos):
        x, y = pos
        if y < self.board_height:
            x = int((x / self.board_width) * 9)
            y = int((y / self.board_height) * 9)
            for i in range(9):
                for j in range(9):
                    if i != y or j != x:
                        self.tiles[i][j].is_selected = False
            self.tiles[y][x].is_selected = not self.tiles[y][x].is_selected
        if self.solve_button.y < y < self.solve_button.y + self.solve_button.height and self.solve_button.x < x < self.solve_button.x + self.solve_button.width:
            Engine.board = self.board
            Engine.solve_board(Engine.board)
            self.board = Engine.board
            self.refresh_tiles()
            self.refresh()
        if self.reset_button.y < y < self.reset_button.y + self.reset_button.height and self.reset_button.x < x < self.reset_button.x + self.reset_button.width:
            self.reset_board()
            self.strikes = 0
            self.refresh_tiles()
            self.start_time = pygame.time.get_ticks()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(pygame.mouse.get_pos())
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.insert_temp(1)
                    if event.key == pygame.K_2:
                        self.insert_temp(2)
                    if event.key == pygame.K_3:
                        self.insert_temp(3)
                    if event.key == pygame.K_4:
                        self.insert_temp(4)
                    if event.key == pygame.K_5:
                        self.insert_temp(5)
                    if event.key == pygame.K_6:
                        self.insert_temp(6)
                    if event.key == pygame.K_7:
                        self.insert_temp(7)
                    if event.key == pygame.K_8:
                        self.insert_temp(8)
                    if event.key == pygame.K_9:
                        self.insert_temp(9)
                    if event.key == pygame.K_BACKSPACE:
                        self.insert_temp(0)
                    if event.key == pygame.K_RETURN:
                        self.confirm_temp()
            self.refresh()
            self.draw_timer()
            self.draw_mistakes()
            pygame.display.flip()

    def draw_timer(self):
        self.ticks = pygame.time.get_ticks() - self.start_time
        seconds = int(self.ticks / 1000 % 60)
        minutes = int(self.ticks / 60000 % 24)
        out = '{minutes:02d}:{seconds:02d}'.format(minutes=minutes, seconds=seconds)
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(out, 1, (0, 0, 0))
        win.blit(text, (win.get_width() - 140, self.board_height + 20))

    def draw_mistakes(self):
        color = (160, 160, 160)
        font = pygame.font.SysFont("comicsans", 30)
        if self.strikes > 0:
            color = (255, 0, 0)
        text = font.render("X", 1, color)
        win.blit(text, (win.get_width() - 250, self.board_height + 28))
        color = (160, 160, 160)

        if self.strikes > 1:
            color = (255, 0, 0)
        text = font.render("X", 1, color)
        win.blit(text, (win.get_width() - 220, self.board_height + 28))
        color = (160, 160, 160)

        if self.strikes > 2:
            color = (255, 0, 0)
        text = font.render("X", 1, color)
        win.blit(text, (win.get_width() - 190, self.board_height + 28))

    def draw_tiles(self):
        for i in range(9):
            for j in range(9):
                self.tiles[i][j].draw()

    def refresh(self):
        win.fill("white")
        self.draw()
        self.solve_button.draw()
        self.reset_button.draw()
        self.draw_mistakes()

    def insert_temp(self, num):
        x, y = self.get_selected_tile()
        if x < 0 or y < 0:
            return
        if self.tiles[x][y].value != 0:
            return

        self.tiles[x][y].temp = num
        # self.board[x][y] = num
        self.refresh()

    def confirm_temp(self):

        x, y = self.get_selected_tile()
        if x < 0 or y < 0:
            return
        if self.tiles[x][y].value != 0:
            return
        if self.tiles[x][y].temp == 0:
            return

        guess = self.tiles[x][y].temp

        if Engine.is_valid_guess(Engine.board, guess, x, y):

            Engine.board[x][y] = guess
            if Engine.solve_board(Engine.board):
                self.tiles[x][y].value = self.tiles[x][y].temp
                self.board[x][y] = guess
                Engine.board = self.board
                return

        Engine.board = self.board
        print("invalid guess")
        self.insert_temp(0)
        self.strikes += 1

    def print_tiles(self):
        for i in range(9):
            for j in range(9):
                print(self.tiles[i][j].value, end='')
            print()

    def get_selected_tile(self):
        for i in range(9):
            for j in range(9):
                if self.tiles[i][j].is_selected:
                    return i, j
        return -1, -1


if __name__ == "__main__":
    gui = GUI()
    gui.run()
