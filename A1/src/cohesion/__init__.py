from puzzle import BoardState, Color, Piece
import search
import time


def main():

    # R.R.
    # BRRB
    # .BB.
    # Y..Y
    board1 = BoardState(4, 4, set([
        Piece(Color.RED, set([(0, 0)])),
        # Piece(Color.RED, set([(3, 0)])),
        Piece(Color.RED, set([(1, 1), (2, 1), (2, 0)])),

        Piece(Color.BLUE, set([(0, 1)])),
        Piece(Color.BLUE, set([(3, 1)])),
        Piece(Color.BLUE, set([(1, 2), (2, 2)])),

        Piece(Color.YELLOW, set([(0, 3)])),
        Piece(Color.YELLOW, set([(3, 3)])),
    ]))

    board = BoardState.from_string(
        """
    R.RR.
    BRRB
    GBBBY
    Y..Y
    """
    )

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
    assert board != board2

    # print(board2)

    # search.print_path(search.bfs(board))

    # search.print_path(search.dfs(board2))

    # search.print_path(search.greedy_search(board2, search.heuristic))

    # search.print_path(search.a_star(board, search.heuristic))

    board = BoardState.generate_random(4, 4)
    print(board)

    compare_searches(board)

def compare_searches(board: BoardState):
    measure_search(lambda: search.bfs(board), "BFS")
    measure_search(lambda: search.dfs(board), "DFS")
    measure_search(lambda: search.greedy_search(board, search.heuristic), "Greedy")
    measure_search(lambda: search.a_star(board, search.heuristic), "A*")

def measure_search(search, name: str):
    start = time.time()
    node = search()
    print("{} took {} seconds".format(name, time.time() - start))
    print("Solution @ depth:", node.depth())
    print(node.board)
    print()

if __name__ == "__main__":
    main()
