from puzzle import BoardState
from graphics import board_to_sprite, board_properties_text, draw_board
import search
import time
import pygame


def main():

    pygame.init()

    screen = pygame.display.set_mode((800, 600))

    board2 = BoardState.from_string("""
        R...
        BR.B
        ..R.
    """)

    board2_copy = BoardState.from_string("""
        R...
        BR.B
        ..R.
    """)

    assert board2 == board2_copy

    while True:
        board = BoardState.generate_random(7, 9)
        print(board)
        draw_board(board, screen)
        pygame.display.flip()

        node = measure_search(lambda: search.a_star(
            board, search.pieces_and_distance_heuristic), "A*")

        if node is None:
            print("No solution found")
            continue

        path = search.get_path(node)

        for node in path:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            draw_board(node.board, screen)
              # draw depth text
            text = pygame.font.SysFont("Arial", 20).render(
                f"Depth: {node.depth()}", True, (255, 255, 255))
            screen.blit(text, (0, 60))
            pygame.display.flip()

            pygame.time.wait(100)
        pygame.time.wait(2000)

    # print(board2)

    # search.print_path(search.bfs(board))

    # search.print_path(search.dfs(board2))

    # search.print_path(search.greedy_search(board2, search.heuristic))

    # search.print_path(search.a_star(board, search.heuristic))

    # board = BoardState.generate_random(4, 4)
    # print(board)

    # compare_searches(board)


def compare_searches(board: BoardState):
    measure_search(lambda: search.bfs(board), "BFS")
    measure_search(lambda: search.dfs(board), "DFS")
    measure_search(lambda: search.greedy_search(
        board, search.pieces_heuristic), "Greedy")
    measure_search(lambda: search.a_star(board, search.pieces_heuristic), "A*")


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
