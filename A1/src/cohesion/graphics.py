from puzzle import BoardState
import search
import pygame

X_MARGIN = 120
Y_MARGIN = 80


def init() -> pygame.Surface:
    pygame.init()
    screen = pygame.display.set_mode((900, 800), pygame.RESIZABLE)
    # search.SHOW_SEARCH = True

    pygame.key.set_repeat(250, 50)
    print(pygame.key.get_repeat())

    return screen


def cell_size(board: BoardState, screen: pygame.Surface):
    return min((screen.get_width() - X_MARGIN * 2) // board.width, (screen.get_height() - Y_MARGIN * 2) // board.height)


def board_to_sprite(board: BoardState, screen: pygame.Surface):
    cs = cell_size(board, screen)
    surface = pygame.Surface(
        (board.width * cs, board.height * cs))

    surface.fill((0, 0, 0))
    for piece in board.pieces:
        for x, y in piece.positions:
            pygame.draw.rect(surface, piece.color.get_color_rgb(
            ), (x * cs, y * cs, cs, cs))
    for x in range(board.width):
        for y in range(board.height):
            pygame.draw.rect(surface, (255, 255, 255), (x *
                             cs, y * cs, cs, cs), 1)

    return surface


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

    s = board_to_sprite(board, screen)

    # draw the board at the center of the screen
    # screen.blit(s, (screen.get_width() // 2 - s.get_width() //
    #             2, screen.get_height()//2 - s.get_height() // 2))
    screen.blit(s, (X_MARGIN, Y_MARGIN))
    screen.blit(board_properties_text(board), (0, 0))


def draw_text(text: str, screen: pygame.Surface, dest):
    font = pygame.font.SysFont("Arial", 20)
    text = font.render(text, True, (255, 255, 255))
    screen.blit(text, dest)


def mouse_to_board(board: BoardState, mouse_pos, screen: pygame.Surface):
    cs = cell_size(board, screen)
    x, y = mouse_pos
    return (x - X_MARGIN) // cs, (y - Y_MARGIN) // cs


def board_to_screen(board: BoardState, x, y, screen: pygame.Surface):
    cs = cell_size(board, screen)
    return x * cs + X_MARGIN, y * cs + Y_MARGIN
