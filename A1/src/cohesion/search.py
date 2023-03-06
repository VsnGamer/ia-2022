import heapq
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
    print("Heuristic: ", heuristic(node.board))
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


def dfs(board: BoardState):
    stack = [TreeNode(board)]
    visited = set()

    while stack:
        current = stack.pop()

        visited.add(current.board)

        if current.board.is_win():
            return current

        for neighbour in current.board.children():
            if neighbour not in visited:
                stack.append(TreeNode(neighbour, current))

    return None


def heuristic(board: BoardState):
    return board.get_num_pieces() - board.get_num_colors()


def greedy_search(board: BoardState, heuristic):
    setattr(TreeNode, "__lt__", lambda self, other: heuristic(
        self.board) < heuristic(other.board))
    heap = [TreeNode(board)]
    visited = set()  # to not visit the same state twice

    while heap:
        node = heapq.heappop(heap)
        visited.add(node.board)

        if node.board.is_win():
            return node

        for child in node.board.children():
            if child not in visited:
                heapq.heappush(heap, TreeNode(child, node))

    return None


def a_star(board: BoardState, heuristic):
    setattr(TreeNode, "__lt__", lambda self, other: (self.depth() +
            heuristic(self.board)) < (other.depth() + heuristic(other.board)))
    heap = [TreeNode(board)]
    visited = set()  # to not visit the same state twice

    while heap:
        node = heapq.heappop(heap)
        visited.add(node.board)

        if node.board.is_win():
            return node

        for child in node.board.children():
            if child not in visited:
                heapq.heappush(heap, TreeNode(child, node))

    return None
