from enum import Enum
from typing import Callable, Optional
import random


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Color(Enum):
    # ANSI escape codes
    RED = 31
    GREEN = 32
    BLUE = 34
    YELLOW = 33

    def get_color_rgb(self):
        if self == Color.RED:
            return (255, 0, 0)
        elif self == Color.GREEN:
            return (0, 255, 0)
        elif self == Color.BLUE:
            return (0, 0, 255)
        elif self == Color.YELLOW:
            return (255, 255, 0)
        else:
            raise Exception("Invalid color")

    @staticmethod
    def parse_color(char: str) -> 'Color':
        # parse color from chars R G B Y

        if char == 'R':
            return Color.RED
        elif char == 'G':
            return Color.GREEN
        elif char == 'B':
            return Color.BLUE
        elif char == 'Y':
            return Color.YELLOW
        else:
            raise Exception("Invalid color char: {}".format(char))


def shift_pos(pos: tuple[int, int], direction: Direction, amount: int = 1) -> tuple[int, int]:
    x, y = pos
    if direction == Direction.UP:
        return (x, y - amount)
    elif direction == Direction.DOWN:
        return (x, y + amount)
    elif direction == Direction.LEFT:
        return (x - amount, y)
    elif direction == Direction.RIGHT:
        return (x + amount, y)
    else:
        raise Exception("Invalid direction")


class Piece:
    def __init__(self, color: Color, positions: set[(int, int)]):
        self.color = color
        self.positions = frozenset(positions)

    def __eq__(self, other):
        return self.color == other.color and self.positions == other.positions

    def __hash__(self):
        return hash((self.color, self.positions))

    def overlaps(self, other) -> bool:
        return len(self.positions & other.positions) > 0

    def get_neighbour_positions(self) -> set[(int, int)]:
        result = set([])
        for x, y in self.positions:
            for direction in Direction:
                pos = shift_pos((x, y), direction)
                if pos not in self.positions:
                    result.add(pos)
        return result

    # returns a new piece that is moved in the given direction, does not check if it stays on the board
    def move(self, direction: Direction) -> 'Piece':
        new_positions = set([])
        for x, y in self.positions:
            new_positions.add(shift_pos((x, y), direction))

        return Piece(self.color, new_positions)

    def uniformity2(self) -> float:
        min_x = min([x for x, y in self.positions])
        max_x = max([x for x, y in self.positions])
        min_y = min([y for x, y in self.positions])
        max_y = max([y for x, y in self.positions])

        width = abs(max_x - min_x) + 1
        height = abs(max_y - min_y) + 1

        largest_side = max(width, height)
        smallest_side = min(width, height)

        # if abs(largest_side - smallest_side) <= 1 and len(self.positions) >= largest_side * smallest_side:
        #     return 0

        if abs(largest_side - smallest_side) <= 1:
            if len(self.positions) >= largest_side * largest_side:
                return 0
            return largest_side * smallest_side - len(self.positions)

        return largest_side * largest_side - len(self.positions)


def merge_same_color_pieces(pieces: set[Piece]):
    # create a new set of pieces by merging pieces of the same color that are touching

    # visit each piece and merge it with any pieces that are connected to it
    visited = set([])
    pos_piece_map = build_pos_piece_map(pieces)
    pieces.clear()

    for piece in pos_piece_map.values():
        if piece in visited:
            continue

        # find all pieces that are connected to this piece
        connected_pieces = set([piece])
        to_visit = piece.get_neighbour_positions()
        while len(to_visit) > 0:
            x, y = to_visit.pop()
            connected_piece = pos_piece_map.get((x, y))
            if connected_piece is not None and connected_piece not in connected_pieces and connected_piece.color == piece.color:
                connected_pieces.add(connected_piece)
                to_visit |= connected_piece.get_neighbour_positions()

        # merge all connected pieces into one piece
        new_positions = set([])
        for connected_piece in connected_pieces:
            new_positions |= connected_piece.positions
            visited.add(connected_piece)
        pieces.add(Piece(piece.color, new_positions))

    return frozenset(pieces)


def any_overlaps(pieces: set[Piece]):
    for piece in pieces:
        for other in pieces:
            if piece != other and piece.overlaps(other):
                return True
    return False


def get_piece(x, y, pieces: set[Piece]) -> Optional[Piece]:
    result = [piece for piece in pieces if (x, y) in piece.positions]

    if len(result) == 0:
        return None

    if len(result) > 1:
        raise Exception("Multiple pieces at ({}, {})".format(x, y))

    return result[0]


def build_pos_piece_map(pieces: frozenset[Piece]) -> dict[(int, int), Piece]:
    result = {}
    for piece in pieces:
        for pos in piece.positions:
            if pos in result:
                raise Exception(
                    "Multiple pieces at ({}, {})".format(pos[0], pos[1]))
            result[pos] = piece
    return result


class BoardState:
    # Cohesion puzzle board state

    # helper function to create a board state from a string
    @staticmethod
    def from_string(string):
        lines = string.splitlines()
        lines = [line.strip() for line in lines if line.strip()]
        width = len(lines[0])
        height = len(lines)
        pieces = set([])
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char != '.' and char != ' ':
                    color = Color.parse_color(char)
                    piece = Piece(color, set([(x, y)]))
                    pieces.add(piece)

        return BoardState(width, height, merge_same_color_pieces(pieces))

    @staticmethod
    def generate_random(width, height, div=2):
        pieces = set([])

        # lets fill about 1/2 of the board with pieces
        for _ in range(int(width * height / div)):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)

            # if there is already a piece at this position, skip it
            if get_piece(x, y, pieces) is not None:
                continue

            color = random.choice(list(Color))
            piece = Piece(color, set([(x, y)]))
            pieces.add(piece)

        return BoardState(width, height, merge_same_color_pieces(pieces))

    def __init__(self, width: int, height: int, pieces: frozenset[Piece], check_valid=True):
        self.width = width
        self.height = height
        self.pieces = pieces

        # this should speed up get_piece
        self.pos_piece_map = build_pos_piece_map(self.pieces)

        if check_valid and not self.is_valid():
            raise Exception("Invalid board state")

        self.num_colors = len(self.get_colors())

    def get_piece(self, x, y) -> Optional[Piece]:
        return self.pos_piece_map.get((x, y), None)

    def get_colors(self):
        return set([piece.color for piece in self.pieces])

    def get_num_colors(self):
        return self.num_colors

    def get_num_pieces(self):
        return len(self.pieces)

    def get_num_pieces_predicate(self, predicate):
        return len([piece for piece in self.pieces if predicate(piece)])

    def get_num_pieces_of_color(self, color):
        return self.get_num_pieces_predicate(lambda piece: piece.color == color)

    # def get_color_counts(self):
    #     return {color: self.get_num_pieces_of_color(color) for color in self.get_colors()}

    def num_piece_cells(self) -> int:
        return sum([len(piece.positions) for piece in self.pieces])

    def is_win(self) -> bool:
        return self.get_num_pieces() == self.get_num_colors()

    def is_piece_in_bounds(self, piece: Piece) -> bool:
        return all([self.is_pos_in_bounds(x, y) for x, y in piece.positions])

    def move_piece(self, piece: Piece, direction: Direction) -> Optional['BoardState']:
        new_piece = piece.move(direction)
        if not self.is_piece_in_bounds(new_piece):
            return None

        new_pieces = set(self.pieces) - set([piece]) | set([new_piece])
        if any_overlaps(new_pieces):
            return None

        return BoardState(self.width, self.height, merge_same_color_pieces(new_pieces), check_valid=False)

    def piece_all_moves(self, piece: Piece) -> list['BoardState']:
        result = []
        for direction in Direction:
            new_state = self.move_piece(piece, direction)
            if new_state is not None:
                result.append(new_state)
        return result

    def children_predicate(self, predicate: Callable[['BoardState', Piece], bool] = lambda _: True):
        result = []
        for piece in self.pieces:
            if predicate(self, piece):
                result.extend(self.piece_all_moves(piece))
        return result

    def should_move(self, piece: Piece):
        return self.get_num_pieces_of_color(piece.color) > 1 or self.is_piece_touching_another(piece)

    def num_stuck_pieces(self):
        return len([piece for piece in self.pieces if len(self.piece_all_moves(piece)) == 0])

    def is_piece_touching_another(self, piece: Piece) -> bool:
        for x, y in piece.positions:
            for direction in Direction:
                other = self.get_piece(*shift_pos((x, y), direction))
                if other is not None and other != piece:
                    return True
        return False

    def is_pos_in_bounds(self, x, y):
        return x >= 0 and x < self.width and y >= 0 and y < self.height

    def is_valid(self):
        for piece in self.pieces:
            for x, y in piece.positions:
                if not self.is_pos_in_bounds(x, y):
                    print("Invalid position: ({}, {})".format(x, y))
                    return False

        # check for overlapping pieces
        for y in range(self.height):
            for x in range(self.width):
                if len([piece for piece in self.pieces if (x, y) in piece.positions]) > 1:
                    print("Overlapping pieces at ({}, {})".format(x, y))
                    return False

        # check for pieces that should be connected but aren't
        for piece in self.pieces:
            for x, y in piece.positions:
                for direction in Direction:
                    pos = shift_pos((x, y), direction)
                    other_piece = self.get_piece(*pos)
                    if pos not in piece.positions and other_piece is not None and other_piece.color == piece.color:
                        print("Pieces not connected at ({}, {})".format(x, y))
                        return False

        return True

    def __str__(self):
        result = "-" * (self.width) + "\n"
        for y in range(self.height):
            for x in range(self.width):
                piece = self.get_piece(x, y)
                if piece is None:
                    result += " "
                else:
                    # colored text
                    result += "\033[{};1m{}\033[0m".format(
                        piece.color.value, piece.color.name[0])

            result += "\n"
        result += "-" * (self.width) + "\n"

        result += str(self.get_num_colors()) + " colors, " + \
            str(self.get_num_pieces()) + " pieces, " + \
            str(self.num_piece_cells()) + " cells"

        percent_filled = self.num_piece_cells() / (self.width * self.height) * 100
        result += " ({:.2f}%)\n".format(percent_filled)
        result += "Win: " + str(self.is_win()) + "\n"
        return result

    def __eq__(self, other):
        return self.pieces == other.pieces

    def __hash__(self):
        return hash(self.pieces)

# tests


def test_equal():
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
