import torch
import numpy as np
from copy import deepcopy

from training.Player import Player


def play_n_self_play_games(game, n_games=100, max_game_length=100, n_playouts=10):
    # init best player here and let it play against itself
    # --> either randomly initialized or load in an already trained model
    # init in class
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    curr_best_player = Player(device=device)  # load in already trained net?

    for i in range(n_games):
        player = deepcopy(curr_best_player)
        play_self_play_game(game, player, max_game_length, n_playouts)

    # train neural net --> pick some randomly shuffled batches from the generated samples
    # let new nn play against old nn
    # if num wins exceeds certain threshold we set the current best player to the new nn
    # repeat this infinitely


def play_self_play_game(game, player, max_game_length=100, n_playouts=10):

    while not game.is_game_ended() and game.get_num_moves() < max_game_length:
        move_value_dict = get_move_values(game, player, n_playouts)  # returns list of values for each move
        move = pick_move(move_value_dict)
        game.make_move(move)


def get_move_values(game, player, n_playouts):
    move_values = {}

    for move in game.get_legal_moves():
        # monte carlo value for move determined by mean over n rollouts starting from new state after picking the move
        game.make_move(move)
        move_values[str(move)] = np.mean([do_playout(game, player) for i in range(0, n_playouts)])
        # get back to actual state
        game.undo_last_move()

    print(move_values)

    return move_values


def do_playout(game, player):
    if game.is_game_ended():
        player.log(game.get_state(), -1)  # current player lost --> value -1
        return 1

    heuristic_move_values = {}

    for move in game.get_legal_moves():
        game.make_move(move)
        # get approximated value for new state
        heuristic_move_values[str(move)] = get_heuristic_state_value(game, player)
        game.undo_last_move()

    # play on
    move = pick_move(heuristic_move_values)
    game.make_move(move)
    value = -do_playout(game, player)
    game.undo_last_move()

    # add state value pair to training samples
    player.log([game.get_state(), value])

    return value  # return the playout value


def get_heuristic_state_value(game, player):
    state = game.get_state()
    heuristic_value = player.predict(state)

    return heuristic_value


# logic for how to pick the move during self play
# for now just pick action with highest value
def pick_move(value_dict):
    return max(value_dict, key=value_dict.get)
