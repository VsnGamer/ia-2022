from puzzle import BoardState
import graphics
import search
import time
import pygame
import play

easy_1 = BoardState.from_string("""
    .B.
    RGR
    .B.
""")

medium_1 = BoardState.from_string("""
    ....
    GBYB
    BB.G
    .R..
""")

hard_1 = BoardState.from_string("""
        BB.G
        RRR.
        RRRB
        .GB.
""")

hard_2 = BoardState.from_string("""
        ..YY
        BGRY
        G.G.
        RGB.
""")

hard_3 = BoardState.from_string("""
        GB.B
        .R..
        .RR.
        BRBG
""")

hard_big_1 = BoardState.from_string("""
RR  R        Y     .
.  Y            R  .
.   G Y B  R G Y   .
.   G           R R.
.Y             GR  .
.                 YY
.     B   B     R  Y
R      RY  R  B R  .
.          R G     .
.   RBB   Y        .
""")

hard_big_2 = BoardState.from_string("""
B GG  RYRB
R     RBY 
GG YGY    
GBR G     
 RY   G  B
   BBR    
GYY  YBY B
RGRBGG    
 RYR  RR  
B      G R
""")

medium_big = BoardState.from_string("""
RR  R              .
.  Y            R  .
.   G Y    R G Y   .
.   G           R R.
.Y             G   .
.                 YY
.     B            Y
R      R   R  B R  .
.          R G     .
.   RB    Y        .
""")

hard_big_3 = BoardState.from_string("""
BGR   Y R.
BRY     GG
R    G Y .
G   BGRB B
. Y YYYB .
. YR  R  R
.  YR YGYG
.G Y  R  B
.B Y GYG .
Y RYGGB Y.
""")

def main():
    # start_play()
    solve_demo()
    # compare_searches(medium_big)


def start_play(board: BoardState = None):
    screen = graphics.init()

    game = play.Game(screen, board)
    game.play()


def solve_demo():
    screen = graphics.init()

    while True:
        # solve(BoardState.generate_random(10, 10, div=1.2), screen)
        solve(hard_big_3, screen)


def solve(board: BoardState, screen: pygame.Surface):
    print(board)

    graphics.draw_board(board, screen)
    pygame.display.flip()

    heuristic = search.multi_heuristic([
        (search.pieces_heuristic, lambda _: 100),
        (search.manhattan_distance_heuristic(), lambda _: 1),
        (search.manhattan_distance_heuristic(same_color=False), lambda _: -.55),
        (search.piece_uniformity_heuristic, lambda _: 20),
        # (search.touching_pieces, lambda _: 1),
    ])
    node = measure_search(lambda: search.a_star(
        board, heuristic, weight=1.5,screen=screen), "A* (Pieces(100), Distance(1), Uniformity(10))")

    if node is None:
        print("No solution found")
        return

    # draw_path(search.get_path(node), heuristic=heuristic)

    # wait for click
    while True:
        graphics.draw_board(node.board, screen)
        search.draw_search_debug(node, screen, heuristic=heuristic)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONDOWN:
                return


def draw_path(path: list[search.TreeNode], delay=250, heuristic=None):
    for node in path:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        graphics.draw_board(node.board, graphics.SCREEN)
        # draw depth text
        text = pygame.font.SysFont("Arial", 20).render(
            f"Depth: {node.depth()}", True, (255, 255, 255))
        graphics.SCREEN.blit(text, (0, 60))

        if heuristic is not None:
            graphics.draw_text("Heuristic: " + str(heuristic(node.board)),
                               graphics.SCREEN, (graphics.SCREEN.get_width() - 200, 20))

        pygame.display.flip()
        pygame.time.wait(delay)


def compare_searches(board: BoardState):
    # graphics.draw_text("Comparing Searches...", graphics.SCREEN, (0, 0))
    # pygame.display.flip()

    print("Comparing Board:")
    print(board)

    # measure_search(lambda: search.bfs(board), "BFS")
    # measure_search(lambda: search.dfs(board), "DFS")
    # measure_search(lambda: search.greedy_search(
    # board, search.pieces_heuristic), "Greedy")
    # measure_search(lambda: search.a_star(
    #     board, search.pieces_heuristic), "A* (Pieces)")

    measure_search(lambda: search.a_star(
        board,
        search.multi_heuristic([
            (search.pieces_heuristic, 1),
            (search.manhattan_distance_heuristic, 1)
        ])
    ), "A* (Pieces(x1) + Distance(x1))")

    measure_search(lambda: search.a_star(
        board,
        search.multi_heuristic([
            (search.pieces_heuristic, 1),
            (search.manhattan_distance_heuristic, 1)
        ]),
        weight=1.5
    ), "Weighted A* (1.5x) (Pieces(x1) + Distance(x1)) ")


def measure_search(search, name: str):
    start = time.time()
    node = search()
    print("{} took {:.3f} seconds".format(name, time.time() - start))
    print("Solution @ depth:", node.depth())
    print(node.board)
    print()

    return node


if __name__ == "__main__":
    main()
