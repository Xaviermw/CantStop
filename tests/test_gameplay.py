import random
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from Components.board_elements import Board
from Components.game import Turn
from Components.player import Player


def test_column_advance_completes_and_sets_winner():
	board = Board(num_players=2)
	column = board.columns[0]
	steps = column.spaces
	completed = column.advance(player_ref=1, steps=steps)

	assert completed is True
	assert column.completed is True
	assert column.winner == 1
	assert column.player_scores[1] == steps


def test_player_registers_three_wins_for_victory():
	player = Player(num_players=2, player_ref=0)
	player.register_column_win(2)
	player.register_column_win(3)
	player.register_column_win(4)

	assert player.columns_won == 3
	assert player.is_winner is True


def test_balanced_player_stops_on_column_finish():
	board = Board(num_players=2)
	player = Player(num_players=2, player_ref=0, strategy="balanced")
	column_value = board.columns[0].value
	board.columns[0].player_scores[0] = board.columns[0].spaces - 1
	turn_progress = {column_value: 1}

	assert player.decide_stop(board, turn_progress, turn_cols=[column_value]) is True


def test_turn_filter_combo_respects_max_columns():
	board = Board(num_players=2)
	players = [Player(num_players=2, player_ref=0), Player(num_players=2, player_ref=1)]
	turn = Turn(players, board, player_ref=0, round_logging=False, roll_delay=0)
	turn.turn_cols = [3, 4, 5]

	assert turn.filter_combo([6, 7]) == []


def test_random_player_chooses_valid_option():
	random.seed(10)
	board = Board(num_players=2)
	player = Player(num_players=2, player_ref=0, strategy="random")
	options = [[3, 4], 5]

	selection = player.choose_option(options, board, turn_progress={})

	assert selection in options
