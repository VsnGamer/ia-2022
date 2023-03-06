from puzzle import BoardState, Color, Piece
import search

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

    #print(board2)

    search.print_path(search.bfs(board2))


if __name__ == "__main__":
    main()
