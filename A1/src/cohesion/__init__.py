from puzzle import BoardState, Color, Piece


class TreeNode:
    def __init__(self, board: BoardState, parent=None):
        self.board = board
        self.parent = parent

    def depth(self):
        if self.parent is None:
            return 0
        return self.parent.depth() + 1


def print_path(node: TreeNode):
    # print the path from the root to the node

    if node is None:
        return

    print_path(node.parent)
    print("Depth: ", node.depth())
    print(node.board)


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

    print_path(bfs(board2))


def bfs(board: BoardState):
    queue = [TreeNode(board)]

    while queue:
        current = queue.pop(0)

        if current.board.is_win():
            return current

        for neighbour in current.board.children():
            queue.append(TreeNode(neighbour, current))


if __name__ == "__main__":
    main()
