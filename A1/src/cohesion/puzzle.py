from enum import Enum

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3
    YELLOW = 4

# parse color from chars R G B Y
def parse_color(char: str):
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

def get_position_in_direction(x, y, direction: Direction):
    if direction == Direction.UP:
        return (x, y - 1)
    elif direction == Direction.DOWN:
        return (x, y + 1)
    elif direction == Direction.LEFT:
        return (x - 1, y)
    elif direction == Direction.RIGHT:
        return (x + 1, y)
    else:
        raise Exception("Invalid direction")

class Piece:
    def __init__(self, color: Color, positions: set[(int, int)]):
        self.color = color
        self.positions = positions

    def overlaps(self, other):
        return len(self.positions & other.positions) > 0
    
    def get_neighbour_positions(self):
        result = set([])
        for x, y in self.positions:
            for direction in Direction:
                pos = get_position_in_direction(x, y, direction)
                if pos not in self.positions:
                    result.add(pos)
        return result
    
    def is_touching(self, other):
        return len(self.get_neighbour_positions() & other.positions) > 0

    def should_merge(self, other):
        return self.color == other.color and self.is_touching(other)

# create a new set of pieces by merging pieces that are touching
def merge_same_color_pieces(pieces: set[Piece]):
    # visit each piece and merge it with any pieces that are connected to it
    new_pieces_merged = set([])
    visited = set([])
    for piece in pieces:
        if piece in visited:
            continue

        # find all pieces that are connected to this piece
        connected_pieces = set([piece])
        to_visit = piece.get_neighbour_positions()
        while len(to_visit) > 0:
            x, y = to_visit.pop()
            connected_piece = get_piece(x, y, pieces)
            if connected_piece is not None and connected_piece not in connected_pieces and connected_piece.color == piece.color:
                connected_pieces.add(connected_piece)
                to_visit |= connected_piece.get_neighbour_positions()
        
        # merge all connected pieces into one piece
        new_positions = set([])
        for connected_piece in connected_pieces:
            new_positions |= connected_piece.positions
            visited.add(connected_piece)
        new_pieces_merged.add(Piece(piece.color, new_positions))
    
    return new_pieces_merged

def any_overlaps(pieces: set[Piece]):
    for piece in pieces:
        for other in pieces:
            if piece != other and piece.overlaps(other):
                return True
    return False

def get_piece(x, y, pieces: set[Piece]):
    result = [piece for piece in pieces if (x, y) in piece.positions]

    if len(result) == 0:
        return None
    
    if len(result) > 1:
        raise Exception("Multiple pieces at ({}, {})".format(x, y))
        
    return result[0]

# Cohesion puzzle board state 
class BoardState:

    # helper function to create a board state from a string
    @staticmethod
    def from_string(string):
        lines = string.splitlines()
        # remove empty lines
        lines = [line.strip() for line in lines if line.strip()]
        width = len(lines[0])
        height = len(lines)
        pieces = set([])
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char != '.':
                    color = parse_color(char)
                    piece = Piece(color, set([(x, y)]))
                    pieces.add(piece)



        board = BoardState(width, height, pieces)
        # merge pieces that are connected
        board.pieces = merge_same_color_pieces(board.pieces)
        return board


    def __init__(self, width, height, pieces: set[Piece]):
        self.width = width
        self.height = height
        self.pieces = pieces

        if not self.is_valid():
            raise Exception("Invalid board state")

    def get_piece(self, x, y):
        return get_piece(x, y, self.pieces)
    
    def get_colors(self):
        return set([piece.color for piece in self.pieces])

    def get_num_colors(self):
        return len(self.get_colors())

    def get_num_pieces(self):
        return len(self.pieces)

    def is_win(self):
        return self.get_num_pieces() == self.get_num_colors()

    def move_piece(self, piece, direction: Direction):
        new_piece_positions = set([])

        for x, y in piece.positions:
            new_x, new_y = get_position_in_direction(x, y, direction)
            if not self.is_valid_position(new_x, new_y):
                return None
            new_piece_positions.add((new_x, new_y))

        new_piece = Piece(piece.color, new_piece_positions)
        new_pieces = self.pieces - set([piece]) | set([new_piece])
        if any_overlaps(new_pieces):
            return None

        
     

        new_state = BoardState(self.width, self.height, merge_same_color_pieces(new_pieces))
        if not new_state.is_valid():
            return None
        
        return new_state
    
    

    def children(self):
        result = []
        for piece in self.pieces:
            for direction in Direction:
                new_state = self.move_piece(piece, direction)
                if new_state is not None:
                    result.append(new_state)
        return result

    def is_valid_position(self, x, y):
        return x >= 0 and x < self.width and y >= 0 and y < self.height

    def is_valid(self):
        for piece in self.pieces:
            for x, y in piece.positions:
                if not self.is_valid_position(x, y):
                    return False
        
        # check for overlapping pieces
        for y in range(self.height):
            for x in range(self.width):
                if len([piece for piece in self.pieces if (x, y) in piece.positions]) > 1:
                    return False

        # check for pieces that should be connected but aren't
      

        return True

    def __str__(self):
        result = ""
        for y in range(self.height):
            result += "|"
            for x in range(self.width):
                piece = self.get_piece(x, y)
                if piece is None:
                    result += " "
                else:
                    result += piece.color.name[0]
            result += "|\n"

        result += str(self.get_num_colors()) + " colors, " + str(self.get_num_pieces()) + " pieces\n"
        result += "Win: " + str(self.is_win()) + "\n"
        return result

