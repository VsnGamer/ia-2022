from puzzle import BoardState
from graphics import draw_board, SCREEN

class Game:
    def __init__(self, board: BoardState = None):
        if board is None:
            board = BoardState.generate_random(10, 10, div=5)
        self.board = board

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            draw_board(self.board, SCREEN)
            pygame.display.flip()

            time.sleep(0.1)

            self.board = self.board.children()[0]
