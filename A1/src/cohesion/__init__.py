from puzzle import BoardState, Color, Piece, Direction

class TreeNode:
    def __init__(self, board: BoardState, parent=None):
        self.board = board
        self.parent = parent

    def depth(self):
        if self.parent is None:
            return 0
        return self.parent.depth() + 1
# print the path from the root to the node

def print_path(node: TreeNode):
    if node is None:
        return

    print_path(node.parent)
    print("Depth: ", node.depth())
    print(node.board)

def main():

    board1 = BoardState(4, 4, set([
        Piece(Color.RED, set([(0, 0)])),
        #Piece(Color.RED, set([(3, 0)])),
        Piece(Color.RED, set([(1, 1), (2, 1),(2, 0)])),
        
        Piece(Color.BLUE, set([(0, 1)])),
        Piece(Color.BLUE, set([(3, 1)])),
        Piece(Color.BLUE, set([(1, 2), (2, 2)])),
        
        Piece(Color.YELLOW, set([(0, 3)])),
        Piece(Color.YELLOW, set([(3, 3)])),
    ]))

    board = BoardState.from_string(
    """
    R..R
    BRRB
    .BB.
    Y..Y
    """)

    print(board)
    
    print_path(bfs(board))


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