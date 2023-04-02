import heapq
import graphics
import pygame
from puzzle import BoardState, Piece


class TreeNode:
    def __init__(self, board: BoardState, parent=None):
        self.board = board
        self.parent = parent
        self._depth = parent.depth() + 1 if parent is not None else 0

    def depth(self):
        return self._depth


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


def dfs(board: BoardState, screen=None):
    stack = [TreeNode(board)]
    visited = set()

    while stack:
        current = stack.pop()
        visited.add(current.board)

        if screen is not None:
            if draw_search_debug(current, screen, visited):
                return None

        if current.board.is_win():
            return current

        for neighbour in current.board.children():
            if neighbour not in visited:
                visited.add(neighbour)
                stack.append(TreeNode(neighbour, current))

    return None


def pieces_heuristic(board: BoardState):
    diff = board.get_num_pieces() - board.get_num_colors()

    if diff < 0:
        raise ValueError(
            "Number of pieces cannot be less than number of colors")

    if diff == 0:
        return int(-1e9)

    return diff


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
        if piece != other and ((same_color and piece.color == other.color) or (not same_color and piece.color != other.color)):
            result += manhattan_distance_piece(piece, other)

    return result


def manhattan_distance_heuristic(same_color=True):
    def heuristic(board: BoardState):
        # manhattan distance of pieces of the same color
        result = 0
        for piece in board.pieces:
            result += manhattan_distance(board, piece, same_color)

        return result

    return heuristic


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


def multi_heuristic(heuristics: list[tuple[callable, callable]]):
    def heuristic(board: BoardState, depth: int):
        return sum([h(board) * w(depth) for h, w in heuristics])

    return heuristic


def greedy_search(board: BoardState, heuristic, screen=None):
    setattr(TreeNode, "__lt__", lambda self, other:
            heuristic(self.board, self.depth() - 1) < heuristic(other.board, self.depth() - 1))
    heap = [TreeNode(board)]
    visited = set()  # to not visit the same state twice

    while heap:
        node = heapq.heappop(heap)
        visited.add(node.board)

        if screen is not None:
            if draw_search_debug(node, screen, visited, heuristic):
                return None

        if node.board.is_win():
            return node

        for child in node.board.children_without_already_completed():
            if child not in visited:
                heapq.heappush(heap, TreeNode(child, node))

    return None


def a_star(board: BoardState, heuristic, depth_limit=None, weight=1, screen=None):
    setattr(TreeNode, "__lt__", lambda self, other: self.depth() +
            heuristic(self.board, self.depth()) * weight < other.depth() + heuristic(other.board, self.depth()) * weight)

    heap = [TreeNode(board)]
    visited = set()  # to not visit the same state twice

    while heap:
        node = heapq.heappop(heap)
        visited.add(node.board)

        if screen is not None:
            if draw_search_debug(node, screen, visited, heuristic):
                return None

        if node.board.is_win():
            return node

        for child in node.board.children_predicate(lambda b, p: b.should_move(p)):
            if child not in visited and (depth_limit is None or node.depth() + 1 < depth_limit):
                visited.add(child)
                heapq.heappush(heap, TreeNode(child, parent=node))

    return None


def beam_search(board: BoardState, heuristic, beam_width=3, depth_limit=None, weight=1, screen=None):
    setattr(TreeNode, "__lt__", lambda self, other: self.depth() +
            heuristic(self.board, self.depth()) * weight < other.depth() + heuristic(other.board, self.depth()) * weight)

    heap = [TreeNode(board)]
    visited = set()  # to not visit the same state twice

    while heap:
        node = heapq.heappop(heap)
        visited.add(node.board)

        if screen is not None:
            if draw_search_debug(node, screen, visited, heuristic):
                return None

        if node.board.is_win():
            return node

        for child in node.board.children_predicate(lambda b, p: b.should_move(p)):
            if child not in visited and (depth_limit is None or node.depth() + 1 < depth_limit):
                visited.add(child)
                heapq.heappush(heap, TreeNode(child, parent=node))

        if len(heap) > beam_width:
            heap = heap[:beam_width]

    return None


def draw_search_debug(node: TreeNode, screen: pygame.Surface, visited=None, heuristic=None) -> bool:
    for event in pygame.event.get():
        cancel = False
        if event.type == pygame.QUIT:
            cancel = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                cancel = True

        if cancel:
            graphics.draw_text("Cancelled", screen,
                               (screen.get_width() // 2 - 50, 20))
            return True

    graphics.draw_board(node.board, screen)
    graphics.draw_text("Depth: " + str(node.depth()),
                       screen, (screen.get_width() - 200, 0))

    if heuristic is not None:
        graphics.draw_text("Heuristic: " + str(heuristic(node.board, node.depth())),
                           screen, (screen.get_width() - 200, 20))

    if visited is not None:
        graphics.draw_text("Visited: " + str(len(visited)),
                           screen, (screen.get_width() - 200, 40))
    pygame.display.flip()

    return False
