from .board_elements import Board, Column
from .player import Player
from .dice import DiceRoll
import copy

class CantStop:

	round_logging = False
	is_over = False

	def __init__(self, num_players, round_logging, strategies=None):
		self.round_logging = round_logging
		self.num_players = num_players
		self.rounds_played = 0
		self.strategies = strategies or ["balanced"] * num_players

	def run_game(self):

		# Initialize Board and Players 
		board = Board(self.num_players)
		players = []
		for i in range(self.num_players):
			strategy = self.strategies[i] if i < len(self.strategies) else "balanced"
			players.append(Player(self.num_players, i, strategy=strategy))

		turn_increment = 0
		while self.is_over == False:
			player_ref = turn_increment % self.num_players
			new_turn = Turn(players, board, player_ref, self.round_logging)
			winner = new_turn.run_turn()
			if winner is not None:
				self.is_over = True
				break
			turn_increment += 1
			self.rounds_played += 1
		return players, board

class Turn:

	max_columns_in_turn = 3

	def __init__(self, players, board, player_ref, round_logging):
		self.players = players
		self.board = board
		self.turn_cols = []
		self.turn_progress = {}
		self.turn_over = False
		self.player_ref = player_ref
		self.round_logging = round_logging

	def run_turn(self):
		while (self.turn_over == False):
			options = self.roll_sequence()
			if not options:
				if self.round_logging:
					print("No Valid Choice - Progress Lost")
				self.turn_over = True
			else:
				player = self.players[self.player_ref]
				selection = player.choose_option(options, self.board, self.turn_progress)
				if self.round_logging:
					print(selection)
				self.update_turn(selection)
				if player.decide_stop(self.board, self.turn_progress, self.turn_cols):
					self.bank_progress()
					if player.is_winner:
						return player.player_ref
					self.turn_over = True
		return None

	def update_turn(self, selection):
		columns = selection if isinstance(selection, (list, tuple)) else [selection]
		for column in columns:
			if column not in self.turn_cols:
				self.turn_cols.append(column)
			self.turn_progress[column] = self.turn_progress.get(column, 0) + 1


	def select_combo(self, num_options):
		choice = input("Select Combination Option (1-" + str(num_options) + ")\n")
		try:
			choice = int(choice)
			if (choice >= 1 and choice <= num_options):
				return (choice-1)
			else:
				print("Invalid Selection, Pick Again")
				return self.select_combo(num_options)
		except (TypeError, ValueError):
			print("Invalid Selection, Pick Again")
			return self.select_combo(num_options)


	def roll_sequence(self):
		dice_roll = DiceRoll()
		if self.round_logging:
			print(dice_roll.dice)
		all_options = []
		for combo in dice_roll.combinations:
			all_options.extend(self.filter_combo(combo))
		if self.round_logging:
			print(all_options)
		return all_options

	def filter_combo(self, combination):
		options = []
		first_element, second_element = combination
		if first_element == second_element:
			if self._column_available(first_element):
				options.append(first_element)
			return options

		first_available = self._column_available(first_element)
		second_available = self._column_available(second_element)
		if not first_available and not second_available:
			return options

		active = set(self.turn_cols)
		new_columns = {c for c in (first_element, second_element) if c not in active}
		if first_available and second_available and (len(active) + len(new_columns) <= self.max_columns_in_turn):
			options.append([first_element, second_element])
			return options

		if first_available and (first_element in active or len(active) < self.max_columns_in_turn):
			options.append(first_element)
		if second_available and (second_element in active or len(active) < self.max_columns_in_turn):
			options.append(second_element)
		return options

	def _column_available(self, column_value):
		column = self.board.columns[column_value-2]
		if column.completed:
			return False
		return True

	def bank_progress(self):
		player = self.players[self.player_ref]
		for column_value, delta in self.turn_progress.items():
			completed = self.board.columns[column_value-2].advance(self.player_ref, delta)
			if completed:
				player.register_column_win(column_value)
