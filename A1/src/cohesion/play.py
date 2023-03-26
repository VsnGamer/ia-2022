from puzzle import BoardState, shift
from graphics import draw_board, mouse_to_board, board_to_screen, cell_size
from puzzle import Direction
import pygame


class Game:
    def __init__(self, screen: pygame.Surface, board: BoardState = None):
        if board is None:
            board = BoardState.generate_random(10, 10, div=4)
        self.board = board
        self.selected_piece = None
        self.selected_position = None
        self.paused = False
        self.screen = screen

    def play(self):
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event)

                if event.type == pygame.MOUSEBUTTONUP:
                    self.handle_release(event)

                if event.type == pygame.MOUSEMOTION:
                    self.handle_motion(event)

                if event.type == pygame.KEYDOWN:
                    self.handle_key(event)

            draw_board(self.board, self.screen)
            self.draw_selected_piece_border()
            pygame.display.update()

            if self.paused:
                continue

            if self.board.is_win():
                self.handle_win()

            clock.tick(30)

    def handle_win(self):
        self.selected_piece = None
        self.selected_position = None
        self.paused = True
        # self.board = BoardState.generate_random(
        #     self.board.width, self.board.height, div=2)

    def draw_selected_piece_border(self):
        if self.selected_piece is None:
            return

        for x, y in self.selected_piece.positions:
            bx, by = board_to_screen(self.board, x, y, self.screen)
            cs = cell_size(self.board, self.screen)
            rect = pygame.Rect(bx - 1, by - 1, cs + 2, cs + 2)
            # magenta border
            pygame.draw.rect(self.screen, (255, 0, 255), rect, 2)

    def handle_click(self, event):
        if self.paused:
            self.board = BoardState.generate_random(
                self.board.width, self.board.height, div=4)
            self.paused = False
            return

        x, y = mouse_to_board(self.board, event.pos, self.screen)
        valid = self.board.is_valid_position(x, y)
        print(f"Board[{x}, {y}] (valid: {valid})")

        piece = self.board.get_piece(x, y)

        self.selected_piece = piece
        self.selected_position = (x, y)

        if piece is not None:
            print(f"Selected [{x}, {y}]")

    def mouse_direction(self, event):
        x, y = mouse_to_board(self.board, event.pos, self.screen)
        xi, yi = self.selected_position

        dx = x - xi
        dy = y - yi

        if dx == 0 and dy == 0:
            return None

        if abs(dx) > 0 and abs(dy) > 0:
            # can't move diagonally
            return None

        if abs(dx) > 1 or abs(dy) > 1:
            # can't move more than one cell
            return None

        if abs(dx) > abs(dy):
            if dx > 0:
                return Direction.RIGHT
            else:
                return Direction.LEFT
        else:
            if dy > 0:
                return Direction.DOWN
            else:
                return Direction.UP

    def handle_motion(self, event):
        if self.selected_piece is None or self.selected_position is None:
            return

        direction = self.mouse_direction(event)
        if direction is None:
            return

        new = self.board.move_piece(self.selected_piece, direction)
        if new is not None:
            self.board = new
            self.selected_position = shift(self.selected_position, direction)
            self.selected_piece = self.board.get_piece(*self.selected_position)

    def handle_release(self, event):
        if self.selected_piece is None or self.selected_position is None:
            return

        direction = self.mouse_direction(event)
        self.selected_piece = None
        self.selected_position = None
        if direction is None:
            return

        self.move_selected_piece(direction)

    def handle_key(self, event):
        if event.key == pygame.K_UP:
            self.move_selected_piece(Direction.UP)
        elif event.key == pygame.K_DOWN:
            self.move_selected_piece(Direction.DOWN)
        elif event.key == pygame.K_LEFT:
            self.move_selected_piece(Direction.LEFT)
        elif event.key == pygame.K_RIGHT:
            self.move_selected_piece(Direction.RIGHT)

    def move_selected_piece(self, direction: Direction):
        if self.selected_piece is None:
            return

        new = self.board.move_piece(self.selected_piece, direction)
        if new is not None:
            self.selected_piece = None
            self.selected_position = None
            self.board = new
