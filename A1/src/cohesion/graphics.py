from puzzle import BoardState
import pygame

SCREEN = pygame.display.set_mode((800, 600))

CELL_SIZE = 35


def board_to_sprite(board: BoardState):
    surface = pygame.Surface(
        (board.width * CELL_SIZE, board.height * CELL_SIZE))
    draw_board_surface(board, surface)
    return surface


def draw_board_surface(board: BoardState, surface: pygame.Surface):
    surface.fill((0, 0, 0))
    for piece in board.pieces:
        for x, y in piece.positions:
            pygame.draw.rect(surface, piece.color.get_color_rgb(
            ), (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    for x in range(board.width):
        for y in range(board.height):
            pygame.draw.rect(surface, (255, 255, 255), (x *
                             CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)


def board_properties_text(board: BoardState):
    surface = pygame.Surface((120, 60))

    # display the number of pieces and the number of colors
    font = pygame.font.SysFont("Arial", 20)
    text = font.render(
        f"Colors: {board.get_num_colors()}", True, (255, 255, 255))
    surface.blit(text, (0, 0))

    text = font.render(
        f"Pieces: {board.get_num_pieces()}", True, (255, 255, 255))
    surface.blit(text, (0, 20))

    # Win: true/false, the boolean text should be red if false and green if true
    text = font.render(f"Win: {board.is_win()}", True,
                       (255, 0, 0) if not board.is_win() else (0, 255, 0))
    surface.blit(text, (0, 40))

    return surface


def draw_board(board: BoardState, screen: pygame.Surface):
    pygame.event.pump()
    screen.fill((0, 0, 0))

    s = board_to_sprite(board)

    # draw the board at the center of the screen
    screen.blit(s, (screen.get_width() // 2 - s.get_width() //
                2, screen.get_height()//2 - s.get_height() // 2))
    screen.blit(board_properties_text(board), (0, 0))


def draw_text(text: str, screen: pygame.Surface, dest):
    font = pygame.font.SysFont("Arial", 20)
    text = font.render(text, True, (255, 255, 255))
    screen.blit(text, dest)
