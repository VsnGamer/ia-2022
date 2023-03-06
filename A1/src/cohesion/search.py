from puzzle import BoardState

class TreeNode:
    def __init__(self, board: BoardState, parent=None):
        self.board = board
        self.parent = parent

    def depth(self):
        if self.parent is None:
            return 0
        return self.parent.depth() + 1

def print_path(node: TreeNode):
    if node is None:
        return

    print_path(node.parent)
    print("Depth: ", node.depth())
    print(node.board)


def bfs(board: BoardState):
    queue = [TreeNode(board)]

    while queue:
        current = queue.pop(0)

        if current.board.is_win():
            return current

        for neighbour in current.board.children():
            queue.append(TreeNode(neighbour, current))

    return None