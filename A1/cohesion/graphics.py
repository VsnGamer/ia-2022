from puzzle import BoardState
import search
import pygame

X_MARGIN = 120
Y_MARGIN = 80


def init() -> pygame.Surface:
    pygame.init()
    screen = pygame.display.set_mode((900, 800), pygame.RESIZABLE)

    pygame.key.set_repeat(250, 50)

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


def board_properties_text(board: BoardState, screen: pygame.Surface):

    # display the number of pieces and the number of colors
    font = pygame.font.SysFont("Arial", 20)
    text = font.render(
        f"Colors: {board.get_num_colors()}", True, (255, 255, 255))
    screen.blit(text, (0, 0))

    text = font.render(
        f"Pieces: {board.get_num_pieces()}", True, (255, 255, 255))
    screen.blit(text, (0, 20))

    percent_filled = board.num_piece_cells() / (board.width * board.height) * 100
    draw_text("Filled: {:.2f}%".format(percent_filled), screen, (0, 40))

    # Win: true/false, the boolean text should be red if false and green if true
    text = font.render(f"Win: {board.is_win()}", True,
                       (255, 0, 0) if not board.is_win() else (0, 255, 0))
    screen.blit(text, (0, 60))


def draw_board(board: BoardState, screen: pygame.Surface):
    screen.fill((0, 0, 0))

    s = board_to_sprite(board, screen)

    # draw the board at the center of the screen
    # screen.blit(s, (screen.get_width() // 2 - s.get_width() //
    #             2, screen.get_height()//2 - s.get_height() // 2))
    screen.blit(s, (X_MARGIN, Y_MARGIN))
    board_properties_text(board, screen)


def draw_path(path: list[search.TreeNode], screen: pygame.Surface, delay=250, heuristic=None):
    for node in path:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        draw_board(node.board, screen)
        text = pygame.font.SysFont("Arial", 20).render(
            f"Depth: {node.depth()}", True, (255, 255, 255))
        screen.blit(text, (screen.get_width() - 200, 0))

        text = pygame.font.SysFont("Arial", 20).render(
            f"Animating... ESC to skip", True, (255, 255, 255))
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 0))

        if heuristic is not None:
            draw_text("Heuristic: " + str(heuristic(node.board, node.depth())),
                      screen, (screen.get_width() - 200, 20))

        pygame.display.flip()
        pygame.time.wait(delay)


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


class Button:
    def __init__(self, text: str,  size: tuple[int, int]):
        super().__init__()
        self.text = text
        self.size = size
        self.pressed = False
        self.clicked = False

        self.rect = None

    def draw(self, screen: pygame.Surface, pos: tuple[int, int]):
        self.rect = pygame.Rect(pos, self.size)

        color = (255, 255, 255) if not self.pressed else (255, 0, 0)
        pygame.draw.rect(screen, color, self.rect, 1)
        text = pygame.font.SysFont("Arial", 20).render(
            self.text, True, (255, 255, 255)
        )
        screen.blit(text, (pos[0] + self.size[0] // 2 - text.get_width() //
                           2, pos[1] + self.size[1] // 2 - text.get_height() // 2))

    def handle_event(self, event: pygame.event.Event):
        if self.rect is None:
            return

        self.clicked = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos) and self.pressed:
                self.clicked = True
            self.pressed = False
        elif event.type == pygame.MOUSEMOTION:
            if not self.rect.collidepoint(event.pos):
                self.pressed = False
