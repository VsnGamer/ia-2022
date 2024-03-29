import os
from typing import Optional
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

easy_big_1 = BoardState.from_string("""
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

hard_big_4 = BoardState.from_string("""
G   GR   R
YGYBR BB .
BYRG YG  G
R Y   G R.
GR BG RBYY
B R  B RYB
.G BY  BRG
. GRRB RR.
.GYY R  B.
.G  YRBG Y
""")


def main():
    screen = graphics.init()

    logo = pygame.image.load(os.path.join(
        os.path.dirname(__file__), "..", "logo.webp")
    )
    
    play_btn = graphics.Button("Play",  (200, 50))
    solve_btn = graphics.Button("Solve", (200, 50))

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                return

            [btn.handle_event(event) for btn in [play_btn, solve_btn]]

            if play_btn.clicked:
                start_play(screen)
                continue

            if solve_btn.clicked:
                solve_demo(screen)
                continue

            screen.fill((0, 0, 0))

            screen.blit(logo, (screen.get_width() //
                        2 - logo.get_width() // 2, 50))
            text = pygame.font.SysFont("Arial", 50).render(
                "Cohesion", True, (255, 255, 255))
            screen.blit(text, (screen.get_width() //
                               2 - text.get_width() // 2, 300))

            play_btn.draw(screen, (screen.get_width() //
                          2 - play_btn.size[0] // 2, 400))
            solve_btn.draw(screen, (screen.get_width() //
                           2 - solve_btn.size[0] // 2, 500))
            pygame.display.flip()

        clock.tick(30)

    # start_play()
    # solve_demo()
    # compare_searches(medium_big)


def start_play(screen: pygame.Surface, board: BoardState = None):

    game = play.Game(screen, board)
    game.play()


def solve_demo(screen: pygame.Surface):
    while True:
        board = BoardState.generate_random(10, 10, 2)
        if solve(board, screen):
            break


def solve(board: BoardState, screen: pygame.Surface) -> bool:
    print(board)

    graphics.draw_board(board, screen)
    pygame.display.flip()

    heuristic = search.multi_heuristic([
        (search.pieces_heuristic, lambda _: 100),
        (search.manhattan_distance_heuristic(), lambda _: 1),
        (search.manhattan_distance_heuristic(same_color=False), lambda _: -.2),
        (search.piece_uniformity_heuristic, lambda _: 15),
        # (search.touching_pieces, lambda _: .5),
    ])

    res = measure_search(
        lambda: search.a_star(board, heuristic, weight=1.8, screen=screen),
        "Weighted A*(x1.8) (Pieces(x100) + Distance(x1) + Repel(x-.2) + Uniformity(x20))",
    )

    if res is None:
        print("No solution found")
    else:
        node, time = res
        graphics.draw_path(search.get_path(node), screen, time, heuristic=heuristic)
    pygame.display.flip()

    # wait for click to continue or backspace/esc to go back
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
                    return True

        pygame.time.wait(100)


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


def measure_search(search, name: str) -> Optional[tuple[search.TreeNode, float]]:
    start = time.time()

    node = search()
    if node is None:
        return None
    
    duration = time.time() - start

    print("{} took {:.3f} seconds".format(name, duration))
    print("Solution @ depth:", node.depth())
    print(node.board)
    print()

    return node, duration


if __name__ == "__main__":
    main()
