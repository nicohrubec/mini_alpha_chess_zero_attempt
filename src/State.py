import numpy as np

white_pieces = {'P': 1, 'B': 2, 'N': 3, 'R': 4, 'Q': 5, 'K': 6}
black_pieces = {'p': 1, 'b': 2, 'n': 3, 'r': 4, 'q': 5, 'k': 6}
board_shape = (8, 8)


class State:

    def __init__(self, board):
        self.board = board
        self.move_count = 0
        self.player = 0  # white begins
        self.state = self.get_board_representation()

    def update_game(self, board):
        self.board = board
        self.move_count += 1
        self.player = 1 if self.player == 0 else 0
        self.state = self.get_board_representation()

    def get_board_representation(self):  # get board representation
        # 8 = position player + position opponent + color + n moves + castling rights queen and kingside each
        state = np.zeros((8, 8, 8))
        white_board = np.zeros(board_shape)  # current player
        black_board = np.zeros(board_shape)  # opposing player

        for i in range(64):
            piece = str(self.board.piece_at(i))
            col = i % 8
            row = int(i/8)

            if piece in white_pieces:
                white_board[row, col] = white_pieces[piece]
            elif piece in black_pieces:
                black_board[row, col] = black_pieces[piece]
            else:  # No piece here
                pass

        if self.move_count % 2 == 0:  # white playing
            state[0] = white_board  # current player piece positions
            state[1] = black_board  # opposing player piece positions
            state[2] = np.zeros(board_shape)  # color of current player
            # set castling rights
            state[3] = np.full(board_shape, self.board.has_kingside_castling_rights(color=0))
            state[4] = np.full(board_shape, self.board.has_queenside_castling_rights(color=0))
            state[5] = np.full(board_shape, self.board.has_kingside_castling_rights(color=1))
            state[6] = np.full(board_shape, self.board.has_queenside_castling_rights(color=1))
        else:  # black playing
            state[0] = np.fliplr(np.flipud(black_board))
            state[1] = np.fliplr(np.flipud(white_board))
            state[2] = np.ones(board_shape)
            state[3] = np.full(board_shape, self.board.has_kingside_castling_rights(color=1))
            state[4] = np.full(board_shape, self.board.has_queenside_castling_rights(color=1))
            state[5] = np.full(board_shape, self.board.has_kingside_castling_rights(color=0))
            state[6] = np.full(board_shape, self.board.has_queenside_castling_rights(color=0))

        state[7] = np.full(board_shape, self.move_count)  # how many moves

        return state

    def get_status(self):
        print(self.board)
        print("Currently {} moves have been played.".format(self.move_count))
        print("Player {} is next.".format(self.player))
