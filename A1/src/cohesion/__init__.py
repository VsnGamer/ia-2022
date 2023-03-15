from puzzle import BoardState
from graphics import draw_board, SCREEN
import search
import time
import pygame
import play


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


def main():
    pygame.init()
    play.start()

def solve_demo():
    while True:
        solve(BoardState.generate_random(10, 10, div=5))

def solve(board: BoardState):
    print(board)

    draw_board(board, SCREEN)
    pygame.display.flip()

    # node = measure_search(lambda: search.bfs(board), "BFS")
    # node = measure_search(lambda: search.greedy_search(board,  search.pieces_and_distance_heuristic), "Greedy")
    # node = measure_search(lambda: search.a_star(
    #     board, search.pieces_and_distance_heuristic), "A* (Pieces + Distance)")

    manhattan_weight = 1
    touching_weight = .5
    heuristic = search.pieces_and_distance_heuristic(manhattan_weight)
    a_star_weight = 1.8
    node = measure_search(lambda: search.dfs(board), "DFS")

    if node is None:
        print("No solution found")
        return

    # draw_path(search.get_path(node), heuristic=heuristic)
    pygame.time.wait(3000)


def draw_path(path: list[search.TreeNode], delay=250, heuristic=None):
    for node in path:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        draw_board(node.board, SCREEN)
        # draw depth text
        text = pygame.font.SysFont("Arial", 20).render(
            f"Depth: {node.depth()}", True, (255, 255, 255))
        SCREEN.blit(text, (0, 60))

        if heuristic is not None:
            text = pygame.font.SysFont("Arial", 20).render(
                f"Heuristic: {heuristic(node.board)}", True, (255, 255, 255))
            SCREEN.blit(text, (0, 80))

        pygame.display.flip()
        pygame.time.wait(delay)


def compare_searches(board: BoardState):
    measure_search(lambda: search.bfs(board), "BFS")
    measure_search(lambda: search.dfs(board), "DFS")
    measure_search(lambda: search.greedy_search(
        board, search.pieces_heuristic), "Greedy")
    measure_search(lambda: search.a_star(
        board, search.pieces_heuristic), "A* (Pieces)")
    measure_search(lambda: search.a_star(
        board, search.pieces_and_distance_heuristic), "A* (Pieces + Distance)")
    measure_search(lambda: search.a_star(board, search.pieces_and_distance_heuristic,
                   weight=1.03), "Weighted A* (Pieces + Distance) (1.03x)")


def measure_search(search, name: str):
    start = time.time()
    node = search()
    print("{} took {} seconds".format(name, time.time() - start))
    print("Solution @ depth:", node.depth())
    print(node.board)
    print()

    return node


if __name__ == "__main__":
    main()