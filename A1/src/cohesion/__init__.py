from puzzle import BoardState
from graphics import draw_board, SCREEN
import search
import time
import pygame

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
                
         
def main():

    pygame.init()


    # board = hard_1
    # print(board)
    # compare_searches(board)
    # return

    while True:
        # board = hard_3
        board = BoardState.generate_random(20, 10, div=4)
        print(board)

        draw_board(board, SCREEN)
        pygame.display.flip()

        # node = measure_search(lambda: search.bfs(board), "BFS")
        # node = measure_search(lambda: search.greedy_search(board, search.pieces_and_distance_heuristic), "Greedy")
        # node = measure_search(lambda: search.a_star(
        #     board, search.pieces_and_distance_heuristic), "A* (Pieces + Distance)")
        node = measure_search(lambda: search.greedy_search(
            board, search.pieces_and_distance_heuristic(.1)), "Greedy (Pieces + Distance)")

        if node is None:
            print("No solution found")
            continue

        path = search.get_path(node)

        for node in path:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            draw_board(node.board, SCREEN)
            # draw depth text
            text = pygame.font.SysFont("Arial", 20).render(
                f"Depth: {node.depth()}", True, (255, 255, 255))
            SCREEN.blit(text, (0, 60))
            pygame.display.flip()

            pygame.time.wait(10)
        pygame.time.wait(1000)


def compare_searches(board: BoardState):
    measure_search(lambda: search.bfs(board), "BFS")
    measure_search(lambda: search.dfs(board), "DFS")
    measure_search(lambda: search.greedy_search(board, search.pieces_heuristic), "Greedy")
    measure_search(lambda: search.a_star(board, search.pieces_heuristic), "A* (Pieces)")
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
