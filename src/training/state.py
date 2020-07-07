import numpy as np

from utils import onehot_board

white_pieces = {'P': 1, 'B': 2, 'N': 3, 'R': 4, 'Q': 5, 'K': 6}
black_pieces = {'p': 1, 'b': 2, 'n': 3, 'r': 4, 'q': 5, 'k': 6}
board_shape = (8, 8)


class State:

    def __init__(self, board):
        self.board = board
        self.move_count = 0
        self.player = 0  # white begins
        self.state = self.get_board_representation()

    def make_move(self, move):
        self.move_count += 1
        self.board.push(move)
        self.player = 1 if self.player == 0 else 0
        self.state = self.get_board_representation()

    def undo_last_move(self):
        self.move_count -= 1
        self.board.pop()
        self.player = 1 if self.player == 0 else 0
        self.state = self.get_board_representation()

    def get_board_representation(self):  # get board representation
        # 8 = position player + position opponent + color + n moves + castling rights queen and kingside each
        state = np.zeros((18, 8, 8))
        white_board = np.zeros(board_shape, dtype=np.int)  # current player
        black_board = np.zeros(board_shape, dtype=np.int)  # opposing player

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
            state[0] = np.zeros(board_shape)  # color of current player

            # set castling rights
            state[1] = np.full(board_shape, self.board.has_kingside_castling_rights(color=0))
            state[2] = np.full(board_shape, self.board.has_queenside_castling_rights(color=0))
            state[3] = np.full(board_shape, self.board.has_kingside_castling_rights(color=1))
            state[4] = np.full(board_shape, self.board.has_queenside_castling_rights(color=1))

            # put together piece encodings for both players
            # shape (6, 8, 8) per player --> one plane per piece
            white_board = onehot_board(white_board)
            black_board = onehot_board(black_board)
            board_encode = np.concatenate((white_board, black_board), axis=0)

        else:  # black playing
            # encoding the same as for white just switch the constants and align the board so that it faces black
            state[0] = np.ones(board_shape)
            state[1] = np.full(board_shape, self.board.has_kingside_castling_rights(color=1))
            state[2] = np.full(board_shape, self.board.has_queenside_castling_rights(color=1))
            state[3] = np.full(board_shape, self.board.has_kingside_castling_rights(color=0))
            state[4] = np.full(board_shape, self.board.has_queenside_castling_rights(color=0))

            black_board = onehot_board(np.fliplr(np.flipud(black_board)))
            white_board = onehot_board(np.fliplr(np.flipud(white_board)))
            board_encode = np.concatenate((black_board, white_board), axis=0)

        state[5] = np.full(board_shape, self.move_count)  # how many moves
        state[6:] = board_encode

        return state

    def get_status(self):
        print(self.board)
        print("Currently {} moves have been played.".format(self.move_count))
        print("Player {} is next.".format(self.player))

    def get_num_moves(self):
        return self.move_count

    def is_game_ended(self):
        return self.board.is_checkmate()

    def get_legal_moves(self):
        return self.board.legal_moves

    def get_state(self):
        return self.state

    def get_player(self):
        return self.player
