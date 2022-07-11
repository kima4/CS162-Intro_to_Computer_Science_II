from JanggiGame import JanggiGame
from JanggiGame import Piece


class Move(Piece):
    def __init__(self, player, position):
        """
        init method uses inherited init
        """
        super().__init__(player, position)
        self._name = 'Possible Move'
        self._symbol = 'x'


class UI:

    def __init__(self):
        setup = self.get_setup()
        self._game = JanggiGame(setup)


    @staticmethod
    def get_setup():
        while True:
            print('Enter the back line setup for each side by using a string representing the piece layout.\n'
                  'r = chariot, h = horse, e = elephant, g = guard,   = no piece\n')
            print('The input should look something like: rehg gher\n'
                  'Capitalization does not matter.\n')
            red = input('Red\'s back line setup from Blue\'s perspective: ')
            blue = input('Blue\'s back line setup from Blue\'s perspective: ')
            red = red.lower()
            blue = blue.upper()

            if not len(red) == 9 or not len(blue) == 9:
                print('ERROR: String length must be exactly 9 characters.')
            elif not (red.startswith('r') and red.endswith('r')) or not (blue.startswith('R') and blue.endswith('R')):
                print('ERROR: Back line must start and end with chariots (r).\n')
            elif red[3:6] != 'g g' or blue[3:6] != 'G G':
                print('ERROR: Middle pieces must be a guard, no piece, and then a guard (g g).\n')
            elif 'h' not in red[1:3] or 'h' not in red[6:8] or 'H' not in blue[1:3] or 'H' not in blue[6:8]:
                print('ERROR: There must be exactly one horse on each side of the general for each player (h).\n')
            elif 'e' not in red[1:3] or 'e' not in red[6:8] or 'E' not in blue[1:3] or 'E' not in blue[6:8]:
                print('ERROR: There must be exactly one elephant on each side of the general for each player (e).\n')
            else:
                setup = [red]
                middle = ['    k    ',
                          ' c     c ',
                          's s s s s',
                          '         ',
                          '         ',
                          'S S S S S',
                          ' C     C ',
                          '    K    ']
                setup += middle
                setup += [blue]
                return setup


    def play_game(self):

        while self._game.get_game_state() == 'UNFINISHED':
            move_piece = self.prompt_for_piece()
            if not move_piece:
                print('The desired piece does not exist.')
            else:
                valid_moves = self.find_valid_moves(move_piece)
                if not valid_moves:
                    print('The piece cannot be moved.')
                else:
                    print('Valid moves are: ' + ', '.join(valid_moves))

                    saved_game = self._game.board_to_strings()
                    mock_game = JanggiGame(saved_game)

                    for move in valid_moves:
                        mock_game.place_piece(Move(self._game.get_turn(), move), move)

                    print(mock_game)

                    destination = self.prompt_for_move(move_piece, valid_moves)

                    if destination:
                        self._game.make_move(move_piece.get_space(), destination)



        print(self._game.get_game_state())


    def prompt_for_piece(self):
        print(self._game)
        to_be_moved = input('Where is the piece that you would like to move?: ')
        return self._game.get_piece_on(to_be_moved)


    @staticmethod
    def prompt_for_move(piece, valid_moves):
        while True:
            destination = input('Where would you like to move the piece?\nEnter \'q\' to choose a different piece: ')
            if destination == 'q':
                return
            if destination in valid_moves or destination == piece.get_space():
                return destination
            print('Invalid destination.')





    def find_valid_moves(self, piece):
        saved_game = self._game.board_to_strings()

        possible_moves = self._game.find_possible_moves(piece)

        valid_moves = []

        for move in possible_moves:
            game_copy = JanggiGame(saved_game)

            if game_copy.get_turn() != self._game.get_turn():
                game_copy.switch_turn()

            if game_copy.make_move(piece.get_space(), move):
                valid_moves.append(move)

        return valid_moves


def main():
    ui = UI()
    ui.play_game()


if __name__ == '__main__':
    main()