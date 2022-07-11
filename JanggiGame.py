# Author: Alexander Kim
# Date: 3/11/2021
# Description:


class Piece:
    """
    Piece class contains information about each piece including player, position on board, name, and
    other piece specific rules such as palace confinement or movement direction. Inherited by other
    piece specific classes.
    """

    def __init__(self, player, position):
        """
        init method for generic piece - piece specific classes that inherit this one fill in more
        specific information
        :param player: True for blue, False for red
        :param position: position on the board as a string in algebraic notation, e.g. 'a1'
        """
        self._player = player
        self._position = position
        # name of piece
        self._name = ''
        # symbol to display on board
        self._symbol = 'p'
        # movement directions
        self._directions = None
        # number of spaces/ times the piece can move in one direction
        self._movement = 1
        # True if piece is confined to palace
        self._confined = False
        # True if piece can move along diagonals in palace
        self._palace_movement = True


    def __str__(self):
        """prints the name of the piece"""
        return self._name


    def get_name(self):
        """returns the name of the piece"""
        return self._name


    def get_player(self):
        """returns the player boolean"""
        return self._player


    def get_symbol(self):
        """
        returns the symbol of the piece to print on the board
        uppercase for blue, lowercase for red
        """
        if self._player:
            return self._symbol.upper()
        return self._symbol


    def get_space(self):
        """returns the position on the board in algebraic notation"""
        return self._position


    def get_coords(self):
        """returns the position on th board in column, row coordinates"""
        col = self._position[0]
        row = self._position[1:]
        return ord(col) - 97, int(row) - 1


    def set_space(self, new_position):
        """updates the position data member with a new space"""
        self._position = new_position


    def get_legal_moves(self):
        """returns information about the piece's legal movements"""
        return self._directions, self._movement, \
               self._confined, self._palace_movement


class General(Piece):
    """
    General class inherits Piece class methods and data members and
    contains piece specific information, such as symbol for display and
    legal moves.
    """

    def __init__(self, player, position):
        """
        init method uses inherited init
        """
        super().__init__(player, position)
        self._name = 'General'
        # k for king since general shares g with guard
        self._symbol = 'k'
        # can move any cardinal direction
        self._directions = (1, 0), (-1, 0), (0, -1), (0, 1)
        # confined to palace
        self._confined = True



class Guard(Piece):
    """
    Guard class inherits Piece class methods and data members and
    contains piece specific information, such as symbol for display and
    legal moves.
    """

    def __init__(self, player, position):
        """
        init method uses inherited init
        """
        super().__init__(player, position)
        self._name = 'Guard'
        self._symbol = 'g'
        # can move any cardinal direction
        self._directions = (1, 0), (-1, 0), (0, -1), (0, 1)
        # confined to palace
        self._confined = True




class Horse(Piece):
    """
    Horse class inherits Piece class methods and data members and
    contains piece specific information, such as symbol for display and
    legal moves.
    """

    def __init__(self, player, position):
        """
        init method uses inherited init
        """
        super().__init__(player, position)
        self._name = 'Horse'
        self._symbol = 'h'
        # the L shaped movements
        self._directions = (-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)
        # unaffected by diagonals in palace
        self._palace_movement = False




class Elephant(Piece):
    """
    Elephant class inherits Piece class methods and data members and
    contains piece specific information, such as symbol for display and
    legal moves.
    """

    def __init__(self, player, position):
        """
        init method uses inherited init
        """
        super().__init__(player, position)
        self._name = 'Elephant'
        self._symbol = 'e'
        # the large L shaped movement
        self._directions = (-3, -2), (-3, 2), (-2, -3), (-2, 3), (2, -3), (2, 3), (3, -2), (3, 2)
        # unaffected by diagonals in palace
        self._palace_movement = False



class Chariot(Piece):
    """
    Chariot class inherits Piece class methods and data members and
    contains piece specific information, such as symbol for display and
    legal moves.
    """

    def __init__(self, player, position):
        """
        init method uses inherited init
        """
        super().__init__(player, position)
        self._name = 'Chariot'
        # r for rook since chariot shares c with cannon
        self._symbol = 'r'
        # can move any cardinal direction
        self._directions = (1, 0), (-1, 0), (0, -1), (0, 1)
        # can move any number of spaces
        self._movement = -1



class Cannon(Piece):
    """
    Cannon class inherits Piece class methods and data members and
    contains piece specific information, such as symbol for display and
    legal moves.
    """

    def __init__(self, player, position):
        """
        init method uses inherited init
        """
        super().__init__(player, position)
        self._name = 'Cannon'
        self._symbol = 'c'
        # can move any cardinal direction
        self._directions = (1, 0), (-1, 0), (0, -1), (0, 1)
        # can move any number of spaces
        self._movement = -1



class Soldier(Piece):
    """
    Soldier class inherits Piece class methods and data members and
    contains piece specific information, such as symbol for display and
    legal moves.
    """

    def __init__(self, player, position):
        """
        init method uses inherited init
        """
        super().__init__(player, position)
        self._name = 'Soldier'
        self._symbol = 's'
        # movement direction is dependent on player
        if self._player:
            self._directions = (-1, 0), (1, 0), (0, -1)
        else:
            self._directions = (-1, 0), (1, 0), (0, 1)


class Board:
    """
    Board class contains information about the board, including contents of each space on the board
    and default setup of the game. Contains methods to set up a game with a given layout, move
    pieces, validate spaces, find pieces of a given player or on a given space, print the board
    for visual inspection, etc.
    """

    def __init__(self, setup=None):
        """
        init method creates a list of lists representing the board and calls method to set up
        pieces in a given layout or the default starting layout
        :param setup: optional, used to set up a board with the given setup, mostly used for testing
        """

        # column labels for algebraic notation
        self._col_labels = 'abcdefghi'
        # board is represented as 9 lists (representing columns)
        # with 10 elements each (representing columns)
        self._spaces = []
        for col in range(0, 9):
            new_col = [None] * 10
            self._spaces.append(new_col)
        # uses the default Janggi setup if no setup is given
        if setup is None:
            setup = ['rehg gehr',
                     '    k    ',
                     ' c     c ',
                     's s s s s',
                     '         ',
                     '         ',
                     'S S S S S',
                     ' C     C ',
                     '    K    ',
                     'REHG GEHR']
        self._setup = setup
        self.setup_game(self._setup)


    def setup_game(self, setup):
        """
        sets up a game with the given board layout
        :param setup: a list containing ten strings, each 9 characters long - each character
                      represents a piece or an empty space and characters used for pieces are the
                      same as the symbols returned by the piece's get_symbol method
        """
        for i, col in enumerate(setup):
            for j, space in enumerate(col):
                if space.isupper():
                    player = True
                else:
                    player = False
                space_num = self._col_labels[j] + str(i + 1)

                # create piece depending on symbol in string
                if space.lower() == 'k':
                    new_piece = General(player, space_num)
                elif space.lower() == 'g':
                    new_piece = Guard(player, space_num)
                elif space.lower() == 'h':
                    new_piece = Horse(player, space_num)
                elif space.lower() == 'e':
                    new_piece = Elephant(player, space_num)
                elif space.lower() == 'r':
                    new_piece = Chariot(player, space_num)
                elif space.lower() == 'c':
                    new_piece = Cannon(player, space_num)
                elif space.lower() == 's':
                    new_piece = Soldier(player, space_num)
                else:
                    new_piece = None

                self.place_piece(new_piece, space_num)



    def place_piece(self, piece, space_num):
        """
        place a given piece on a given space
        :param piece: some object that inherited the Piece class
        :param space_num: a string representing a space in algebraic notation, e.g. 'a1'
        """
        col, row = self.space_to_coord(space_num)
        self._spaces[col][row] = piece


    def move_piece(self, piece, new_space):
        """
        move a given piece to a given space and remove the piece from its previous space
        :param piece: some object that inherited the Piece class
        :param new_space: a string representing a space in algebraic notation, e.g. 'a1'
        """
        old_space = piece.get_space()
        piece.set_space(new_space)
        self.place_piece(None, old_space)
        self.place_piece(piece, new_space)


    def is_valid_space(self, space_num):
        """
        returns true if the given space is on the board
        :param space_num: a string representing a space in algebraic notation, e.g. 'a1'
        :return: True if the space is on the board, False otherwise
        """
        if len(space_num) < 2 or len(space_num) > 3:
            return False
        if not space_num.isalnum():
            return False
        if not space_num[0].isalpha():
            return False
        if space_num[0].lower() not in self._col_labels:
            return False
        if not space_num[1:].isnumeric():
            return False
        if int(space_num[1:]) < 1 or int(space_num[1:]) > 10:
            return False
        return True


    @staticmethod
    def space_to_coord(space_num):
        """
        converts a string representing a space to coordinates in column, row format
        :param space_num: a string representing a space in algebraic notation, e.g. 'a1'
        :return: a tuple containing the column and row of the space in self._spaces
        """
        col = space_num[0]
        row = space_num[1:]
        return ord(col) - 97, int(row) - 1


    def coord_to_space(self, col, row):
        """
        converts coordinates in column, row format to a string representing of the space
        :param col: index of the column
        :param row: index of the row
        :return: a string representing the space in algebraic notation
        """
        return self._col_labels[col] + str(row + 1)


    def board_to_strings(self):
        """
        creates a list representing the board state, either for printing or backup for reverting
        :return: array of ten strings, each with nine characters, that represents the board state
        """
        board_strings = []
        for i in range(0, 10):
            new_col = []
            for j in range(0, 9):
                if self._spaces[j][i] is None:
                    new_col += ' '
                else:
                    new_col += self._spaces[j][i].get_symbol()
            board_strings.append(new_col)
        return board_strings


    def board_to_print(self):
        """
        creates an output to pass to __str__ for board visualization
        :return: a string containing board lines and piece positions
        """
        print_string = '1  '
        board_strings = self.board_to_strings()
        for i, row in enumerate(board_strings):
            for j, piece in enumerate(row):
                print_string += piece
                if j != 8:
                    print_string += ' - '
                elif i != 9:
                    print_string += '\n'
                    if i == 0 or i == 7:
                        print_string += '   |   |   |   | \ | / |   |   |   ' \
                                        '|\n' + str(i + 2) + '  '
                    elif i == 1 or i == 8:
                        print_string += '   |   |   |   | / | \ |   |   |   ' \
                                        '|\n' + str(i + 2) + ' '
                        if i == 1:
                            print_string += ' '
                    else:
                        print_string += '   |   |   |   |   |   |   |   |   ' \
                                        '|\n' + str(i + 2) + '  '
        print_string += '\n   a   b   c   d   e   f   g   h   i\n'
        return print_string


    def __str__(self):
        """prints the board in its current state"""
        return self.board_to_print()


    def get_player_pieces(self, player):
        """
        gets list of pieces for a given player
        :param player: True for blue, False for red
        :return: list of Piece objects
        """
        pieces = []
        for col in self._spaces:
            for space in col:
                if space is not None and space.get_player() == player:
                    pieces.append(space)
        return pieces


    def get_player_general(self, player):
        """
        returns the general of a given player
        :param player: True for blue, False for red
        :return: the player's General object
        """
        col = [3, 4, 5]
        if player:
            row = [7, 8, 9]
        else:
            row = [0, 1, 2]
        for c in col:
            for r in row:
                space = self.get_piece_on(c, r)
                if space is not None and space.get_name() == 'General':
                    return space


    def get_piece_on(self, space_or_col, row=None):
        """
        returns the piece on a given space
        :param space_or_col: either the column index of the piece or the space in algebraic notation
        :param row: optional, if the first parameter was the column index, then the row index
        :return: the Piece object on the space or None
        """
        if row is not None:
            space_or_col = self.coord_to_space(space_or_col, row)
        if not self.is_valid_space(space_or_col):
            return None
        col, row = self.space_to_coord(space_or_col)
        return self._spaces[col][row]


class JanggiGame:
    """
    JanggiGame class contains the encompassing information about a game. Contains the board, keeps
    track of whose turn it is, and the game state. Also contains information about the diagonal
    lines inside each palace for piece movement. Contains methods for piece movement, move
    verification, check verification, game printing, etc.
    """

    def __init__(self, setup=None):
        """
        init method creates the board, sets player turn to blue, sets game state to unfinished, and
        creates dictionary of palace diagonals
        :param setup: optional, used to set up a game with a different start than usual, mostly
                      for testing
        """
        self._board = Board(setup)
        self._palace_connections = {'d1': ['e2'],
                                    'f1': ['e2'],
                                    'e2': ['d1', 'f1', 'd3', 'f3'],
                                    'd3': ['e2'],
                                    'f3': ['e2'],
                                    'd8': ['e9'],
                                    'f8': ['e9'],
                                    'e9': ['d8', 'f8', 'd10', 'f10'],
                                    'd10': ['e9'],
                                    'f10': ['e9']}
        # True for blue, False for red
        self._turn = True
        self._game_state = 'UNFINISHED'


    def get_game_state(self):
        """returns game state"""
        return self._game_state


    def get_turn(self):
        return self._turn


    def __str__(self):
        """gets a string of the board using the Board method"""
        return str(self._board)


    def is_valid_space(self, space_num):
        """determines if the given space is valid using the Board method"""
        return self._board.is_valid_space(space_num)


    def space_to_coord(self, space_num):
        """converts from algebraic notation to coordinates using the Board method"""
        return self._board.space_to_coord(space_num)


    def coord_to_space(self, col, row):
        """converts from coordinates to algebraic notation using the Board method"""
        return self._board.coord_to_space(col, row)


    def get_piece_on(self, space_or_col, row=None):
        """gets the piece on a given space using the Board method"""
        return self._board.get_piece_on(space_or_col, row)


    def setup(self, setup):
        """sets up a game with the given setup using the Board method"""
        self._board.setup_game(setup)


    @staticmethod
    def on_board(col, row):
        """returns True if the indices given represent a space on the board"""
        if 0 <= col < 9 and 0 <= row < 10:
            return True
        return False


    @staticmethod
    def in_palace(col, row):
        """returns True if the indices given represent a space in either palace"""
        if str(col) in '345' and str(row) in '012789':
            return True
        return False


    def get_general(self, player):
        """gets the general of a given player using the Board method"""
        return self._board.get_player_general(player)


    def get_pieces(self, player):
        """gets the pieces of a given player using the Board method"""
        return self._board.get_player_pieces(player)


    def cannon_moves(self, piece):
        """
        method specifically for cannon movement since it is unique
        :param piece: the Cannon object
        :return: a list of spaces in algebraic notation that the cannon can go
        """

        # get location and movement information
        piece_x, piece_y = piece.get_coords()
        direct, moves, confined, pal_move = piece.get_legal_moves()
        possible_spaces = []

        # iterates through each of the possible movement directions
        for x, y in direct:

            # adds current position and movement to get space for prospective movement
            pos_x = piece_x + x
            pos_y = piece_y + y

            # number of times the cannon has jumped another piece
            jumps = 0

            # while the prospective space is on the board and the cannon has jumped less than twice
            while self.on_board(pos_x, pos_y) and jumps < 2:

                # get piece on space of prospective movement
                space = self.get_piece_on(pos_x, pos_y)

                if space is not None:
                    # cannot jump cannons, so do not look further
                    if space.get_name() == 'Cannon':
                        jumps = 99
                    else:
                        jumps += 1

                    # if this is the second piece encountered and it is an opponent piece, it
                    # can be taken
                    if jumps == 2 and space.get_player() != piece.get_player():
                        possible_spaces.append(self.coord_to_space(pos_x, pos_y))

                # add empty spaces after the first jump to possible spaces to move
                elif jumps == 1:
                    possible_spaces.append(self.coord_to_space(pos_x, pos_y))

                # look to the next space in the same direction
                pos_x += x
                pos_y += y

        # look for diagonal movement if cannon is on the corner of a palace
        if piece.get_space() in self._palace_connections:
            if piece_y == 0 or piece_y == 2:
                possible_spaces += self.cannon_diagonals(piece, 'e2')
            elif piece_y == 7 or piece_y == 9:
                possible_spaces += self.cannon_diagonals(piece, 'e2')

        return possible_spaces


    def cannon_diagonals(self, piece, palace_center):
        """
        method specifically for cannon movement in palaces
        :param piece: the Cannon object
        :param palace_center: the center of the palace the cannon is in
        :return: list containing spaces the cannon can move to diagonally
        """

        # cannon can only move diagonally if there is a piece in the center of the palace
        center_piece = self.get_piece_on(palace_center)

        if center_piece and center_piece.get_name() != 'Cannon':
            piece_x, piece_y = piece.get_coords()
            center_x, center_y = center_piece.get_coords()

            x = center_x - piece_x
            y = center_y - piece_y

            # get the space in the palace opposite of the cannon
            pos_x = center_x + x
            pos_y = center_y + y

            space = self.get_piece_on(pos_x, pos_y)

            # check the corner opposite of the cannon is valid for movement
            if space is None:
                return [self.coord_to_space(pos_x, pos_y)]
            elif space.get_player() != piece.get_player():
                if space.get_name() != 'Cannon':
                    return [self.coord_to_space(pos_x, pos_y)]

        return []


    def elephorse_blocked(self, movement, coords):
        """
        check if the path of an elephant or horse is blocked
        :param movement: tuple containing the column and row movement of the piece
        :param coords: tuple containing coordinates of the piece
        :return: True if movement is blocked, False otherwise
        """
        x, y = movement
        piece_x, piece_y = coords

        while x != 0 and y != 0:
            # check the spaces incrementally closer to the starting position
            if x > 0:
                x -= 1
            else:
                x += 1
            if y > 0:
                y -= 1
            else:
                y += 1

            pos_x = piece_x + x
            pos_y = piece_y + y

            if self.get_piece_on(pos_x, pos_y) is not None:
                return True
        return False


    def find_possible_moves(self, piece):
        """
        find the possible moves of a given piece based on positions of other pieces - does not
        take into account putting own king into check
        :param piece: the Piece object for movement
        :return: list containing spaces of possible movement in algebraic notation
        """

        # cannon movement is unique, so use different method
        if piece.get_name() == 'Cannon':
            return self.cannon_moves(piece)

        # get location and movement information
        piece_x, piece_y = piece.get_coords()
        direct, moves, confined, pal_move = piece.get_legal_moves()
        possible_spaces = []

        # iterate through each of the possible movement directions
        for x, y in direct:
            movement = 0
            pos_x = piece_x + x
            pos_y = piece_y + y
            blocked = False

            # check spaces in a direction while the piece has not moved too far, the space is on
            # the board, and the space is not blocked
            while movement != moves and self.on_board(pos_x, pos_y) and not blocked:

                # get the piece (if any) that is on the prospective space
                space = self.get_piece_on(pos_x, pos_y)

                # go no further if the space is blocked by own piece
                if space is not None and space.get_player() == piece.get_player():
                    blocked = True

                # if confined to palace, make sure the space is in the palace before adding it
                # to list of possible movements
                elif confined:
                    if self.in_palace(pos_x, pos_y):
                        possible_spaces.append(self.coord_to_space(pos_x, pos_y))

                # add space to list if unblocked or occupied by enemy piece - additional blocking
                # check for horse and elephant pieces
                else:
                    if space is not None:
                        blocked = True
                    if piece.get_name() == 'Elephant' or piece.get_name() == 'Horse':
                        if not self.elephorse_blocked((x, y), (piece_x, piece_y)):
                            possible_spaces.append(self.coord_to_space(pos_x, pos_y))
                    else:
                        possible_spaces.append(self.coord_to_space(pos_x, pos_y))

                # look to next space in same direction and increment movement counter
                pos_x += x
                pos_y += y
                movement += 1

        # logic for movement in palace along diagonals
        if pal_move:
            space_num = self.coord_to_space(piece_x, piece_y)

            # if the space is in the dictionary of palace movement, diagonal movement is
            # potentially available
            if space_num in self._palace_connections:

                # combine movement vectors to ensure movement is in legal direction
                # (mostly for soldier pieces)
                for x1, y1 in direct[0:2]:
                    for x2, y2 in direct[2:]:

                        # same logic as non-palace movement for the most part
                        movement = 0
                        pos_x = piece_x + x1 + x2
                        pos_y = piece_y + y1 + y2
                        blocked = False

                        while movement != moves and self.in_palace(pos_x, pos_y) and not blocked:
                            space = self.get_piece_on(pos_x, pos_y)

                            if space is not None and space.get_player() == piece.get_player():
                                blocked = True
                            elif self.in_palace(pos_x, pos_y):
                                if space is not None:
                                    blocked = True
                                possible_spaces.append(self.coord_to_space(pos_x, pos_y))

                            pos_x += x1 + x2
                            pos_y += y1 + y2
                            movement += 1

        return possible_spaces


    def spaces_under_attack(self, pieces):
        """
        finds all spaces that are being attacked
        :param pieces: list of Piece objects
        :return: list of spaces in algebraic notation that the pieces can be moved to
        """
        moves = []
        for piece in pieces:
            moves += self.find_possible_moves(piece)

        return moves


    @staticmethod
    def player(player):
        """returns 'blue' for True, 'red' for False"""
        if player:
            return 'blue'
        return 'red'


    def is_in_check(self, player_color):
        """
        determines if the specified player is in check
        :param player_color: a string containing the player color
        :return: True if the player is in check, false otherwise
        """

        if player_color.lower() == 'blue':
            player = True
        elif player_color.lower() == 'red':
            player = False
        else:
            return False

        # get a list of the opponent pieces and the player general
        opponent_pieces = self.get_pieces(not player)
        general = self.get_general(player)

        # get a list of moves the opponent can make
        opponent_moves = self.spaces_under_attack(opponent_pieces)

        # if the space the general is on is in the list of opponent moves, the general is in check
        if general.get_space() in opponent_moves:
            return True
        return False


    def check_for_mate(self, player):
        """
        determines if the specified player has been checkmated
        :param player: True for blue, False for red
        :return: True if the player is in checkmate, False otherwise
        """

        # convert boolean to player color string for is_in_check
        player_color = self.player(player)

        # if the player is not in check in the first place, they are not in checkmate
        if not self.is_in_check(player_color):
            return False

        # calls methods to see if checkmate can be avoided by moving the general
        # or by moving a friendly piece to block the check
        not_mate = self.check_for_mate_avoid(player) or self.check_for_mate_defense(player)
        return not not_mate



    def check_for_mate_avoid(self, player):
        """
        determines if the general can be moved to avoid being in check
        :param player: True for blue, False for red
        :return: True if the player can move the general to get it out of check
        """

        # get the player general and a list of its moves
        general = self.get_general(player)
        gen_moves = self.find_possible_moves(general)

        # get a list of opponent moves
        opponent_moves = self.spaces_under_attack(self.get_pieces(not player))

        # if there is a space the general can move to that is not under attack by an opponent piece
        # return True
        if [move for move in gen_moves if move not in opponent_moves]:
            return True

        return False


    def check_for_mate_defense(self, player):
        """
        determines if a friendly piece can be moved to block the king from check or take the
        attacking piece
        :param player: True for blue, False for red
        :return: True if the player can uncheck their king by moving a different piece
        """

        # get player color string for is_in_check
        player_color = self.player(player)

        # save the game to backup to allow moving pieces around for experimentation
        save_game = self._board.board_to_strings()

        friendly_pieces = self.get_pieces(player)

        # iterate through friendly pieces to see if check can be blocked
        for piece in friendly_pieces:
            friendly_moves = self.find_possible_moves(piece)
            for move in friendly_moves:
                self._board.move_piece(piece, move)

                # see if general is in check after making move and return True if not
                if not self.is_in_check(player_color):

                    # revert game back
                    self._board.setup_game(save_game)
                    return True

            # revert game back
            self._board.setup_game(save_game)

        return False


    def make_move(self, space_from, space_to):
        """
        tries to move a piece from one space to another
        :param space_from: a string representing a space in algebraic notation
        :param space_to: a string representing a space in algebraic notation
        :return: True if the movement was successful, False otherwise
        """


        #print('Trying to move from '+space_from+' to '+space_to)
        # if the game is finished, do not do anything
        if self.get_game_state() != 'UNFINISHED':
            return False

        # if the spaces are the same, the player skips their turn and movement succeeds
        if space_from == space_to:
            self._turn = not self._turn
            return True

        # if either given spaces are not valid, movement fails
        if not self.is_valid_space(space_from) or not self.is_valid_space(space_to):
            #print('space is not on the board')
            return False

        # if there is no piece or the piece is owned by the opponent, movement fails
        to_be_moved = self.get_piece_on(space_from)
        if to_be_moved is None or to_be_moved.get_player() != self._turn:
            #print('piece does not exist or owned by opponent')
            return False

        # get spaces the piece can move - if the destination space is not in the list of
        # valid movements, movement fails
        move_list = self.find_possible_moves(to_be_moved)
        if space_to not in move_list:
            #print('destination is not in valid moveset')
            return False

        # save the game in case the movement is actually not valid and make the move
        save_game = self._board.board_to_strings()
        self._board.move_piece(to_be_moved, space_to)

        # determine if the move put the player's own general in check - if not, switch whose
        # turn it is and check for checkmate
        if not self.is_in_check(self.player(self._turn)):
            #print('valid move')
            #print(self._board)
            self._turn = not self._turn

            # if checkmate, update game state
            if self.check_for_mate(self._turn):
                if not self._turn:
                    self._game_state = 'BLUE_WON'
                else:
                    self._game_state = 'RED_WON'

            return True

        # if movement put own king in check, revert game to previous state and movement fails.
        self._board.setup_game(save_game)
        #print('move resulted in self-check')
        return False


    def board_to_strings(self):
        return self._board.board_to_strings()


    def setup_game(self, setup):
        self._board.setup_game(setup)


    def place_piece(self, piece, space_num):
        self._board.place_piece(piece, space_num)


    def switch_turn(self):
        self._turn = not self._turn


def main():
    """
    g = JanggiGame(['         ',
                    '    k    ',
                    '     c  e',
                    '         ',
                    '         ',
                    '     s   ',
                    '         ',
                    '  r      ',
                    '  s K    ',
                    '        r'])
    print(g)
    print(g.is_in_check('blue'))
    print(g.make_move('1','1'))
    g.make_move('i3', 'g6')
    print(g)
    print(g.is_in_check('blue'))
    print(g.get_game_state())
    """
    g1 = JanggiGame()
    g1.make_move('e9', 'f10')
    """
    game = JanggiGame()
    print(game)
    print(game.make_move('c1', 'e3'))  # should be False because it's not Red's turn
    print(game.make_move('a7','b7')) #should return True
    print(game.is_in_check('blue'))  # should return False
    print(game.make_move('a4', 'a5'))  # should return True
    print(game.get_game_state())  # should return UNFINISHED
    print(game.make_move('b7', 'b6'))  # should return True
    print(game.make_move('b3', 'b6'))  # should return False because it's an invalid move
    print(game.make_move('a1', 'a4'))  # should return True
    print(game.make_move('c7', 'd7'))  # should return True
    print(game.make_move('a4', 'a4'))  # this will pass the Red's turn and return True
    print(game)
    """
if __name__ == '__main__':
    main()

