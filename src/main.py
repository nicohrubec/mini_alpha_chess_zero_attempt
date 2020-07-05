import chess
from State import State

if __name__ == '__main__':
    board = chess.Board()

    game = State(board)

    move = next(iter(board.legal_moves))

    board.push(move)
    game.update_game(board)

    move = next(iter(board.legal_moves))
    board.push(move)
    game.update_game(board)