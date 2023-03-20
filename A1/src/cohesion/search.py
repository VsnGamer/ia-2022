import heapq
import graphics
import pygame
from puzzle import BoardState, Piece

SHOW_SEARCH = True


class TreeNode:
    def __init__(self, board: BoardState, parent=None):
        self.board = board
        self.parent = parent

    def depth(self):
        depth = 0
        node = self
        while node is not None:
            depth += 1
            node = node.parent

        return depth


def get_path(node: TreeNode) -> list[TreeNode]:
    # from root to node
    path = []
    while node is not None:
        path.append(node)
        node = node.parent

    return path[::-1]


def print_path(node: TreeNode):
    if node is None:
        return

    print_path(node.parent)
    print("Depth: ", node.depth())
    print("Heuristic: ", pieces_heuristic(node.board))
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

        if SHOW_SEARCH:
            draw_search_debug(current, visited)

        if current.board.is_win():
            return current

        for neighbour in current.board.children():
            if neighbour not in visited:
                visited.add(neighbour)
                stack.append(TreeNode(neighbour, current))

    return None


def pieces_heuristic(board: BoardState):
    return board.get_num_pieces() - board.get_num_colors()


def manhattan_distance_piece(piece, other):
    distance = None

    # get the smallest distance between the two pieces
    for x, y in piece.positions:
        for other_x, other_y in other.positions:
            if distance is None:
                distance = abs(x - other_x) + abs(y - other_y) - 1
            else:
                distance = min(distance, abs(x - other_x) +
                               abs(y - other_y) - 1)

    return distance if distance is not None else 0


def manhattan_distance(board: BoardState, piece: Piece, same_color: bool):
    result = 0
    for other in board.pieces:
        if piece != other and (same_color and piece.color == other.color or not same_color and piece.color != other.color):
            result += manhattan_distance_piece(piece, other)

    return result


def manhattan_distance_heuristic(board: BoardState, same_color=True):
    # manhattan distance of pieces of the same color
    result = 0
    for piece in board.pieces:
        result += manhattan_distance(board, piece, same_color)

    return result


def touching_pieces(board: BoardState):
    # number of pieces that are touching each other (different color)
    result = 0
    for piece in board.pieces:
        for other in board.pieces:
            if piece != other and piece.color != other.color:
                for x, y in piece.positions:
                    for other_x, other_y in other.positions:
                        if abs(x - other_x) + abs(y - other_y) <= 2:
                            result += 1

    return result


def piece_uniformity_heuristic(board: BoardState):
    return sum([piece.uniformity2() for piece in board.pieces])


def multi_heuristic(heuristics):
    def heuristic(board: BoardState):
        return sum([h(board) * w for h, w in heuristics])

    return heuristic


def greedy_search(board: BoardState, heuristic):
    setattr(TreeNode, "__lt__", lambda self, other: heuristic(
        self.board) < heuristic(other.board))
    heap = [TreeNode(board)]
    visited = set()  # to not visit the same state twice

    while heap:
        node = heapq.heappop(heap)
        visited.add(node.board)

        if SHOW_SEARCH:
            draw_search_debug(node, visited, heuristic)

        if node.board.is_win():
            return node

        for child in node.board.children():
            if child not in visited:
                heapq.heappush(heap, TreeNode(child, node))

    return None


def a_star(board: BoardState, heuristic, depth_limit=None, weight=1):
    setattr(TreeNode, "__lt__", lambda self, other: self.depth() +
            heuristic(self.board) * weight < other.depth() + heuristic(other.board) * weight)

    heap = [TreeNode(board)]
    visited = set()  # to not visit the same state twice

    while heap:
        node = heapq.heappop(heap)
        visited.add(node.board)

        if SHOW_SEARCH:
            draw_search_debug(node, visited, heuristic)

        if node.board.is_win():
            return node

        for child in node.board.children_without_already_completed():
            if child not in visited and (depth_limit is None or node.depth() + 1 < depth_limit):
                visited.add(child)
                heapq.heappush(heap, TreeNode(child, parent=node))

    return None


def draw_search_debug(node: TreeNode, visited=None, heuristic=None):
    graphics.draw_board(node.board, graphics.SCREEN)
    graphics.draw_text("Depth: " + str(node.depth()),
                       graphics.SCREEN, (graphics.SCREEN.get_width() - 200, 0))

    if heuristic is not None:
        graphics.draw_text("Heuristic: " + str(heuristic(node.board)),
                           graphics.SCREEN, (graphics.SCREEN.get_width() - 200, 20))

    if visited is not None:
        graphics.draw_text("Visited: " + str(len(visited)),
                           graphics.SCREEN, (graphics.SCREEN.get_width() - 200, 40))
    pygame.display.flip()
