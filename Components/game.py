from .board_elements import Board, Column
from .player import Player
from .dice import DiceRoll
import copy

class CantStop:

	round_logging = False
	is_over = False

	def __init__(self, num_players, round_logging):
		self.round_logging = round_logging
		self.num_players = num_players
		self.rounds_played = 0

	def run_game(self):

		# Initialize Board and Players 
		board = Board(self.num_players)
		players = []
		for i in range(self.num_players):
			players.append(Player(self.num_players, i))

		turn_increment = 0
		while self.is_over == False:
			player_ref = turn_increment % self.num_players
			new_turn = Turn(players, copy.deepcopy(board), player_ref)
			turn_over = False
			new_turn.run_turn()
			# while turn_over == False:
				


			turn_increment += 1

class Turn:

	max_columns_in_turn = 3

	def __init__(self, players, board, player_ref):
		self.players = players
		self.board = board
		self.turn_cols = []
		self.turn_over = False
		self.player_ref = player_ref

	def run_turn(self):
		while (self.turn_over == False):
			options = self.roll_sequence()
			if not options:
				print("No Valid Choice - Progress Lost")
				self.turn_over = True
			else:
				choice = self.select_combo(len(options))
				print(options[choice])
				self.update_turn(options[choice])

	def update_turn(self, selection):
		if isinstance(selection, int):
			if selection not in self.turn_cols:
				self.turn_cols.append(selection)
			self.board.columns[selection-2].increment(self.player_ref)
		else: 
			for column in selection:
				if column not in self.turn_cols:
					self.turn_cols.append(column)
				self.board.columns[column-2].increment(self.player_ref)


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
		print(dice_roll.dice)
		option_one = self.filter_combo(dice_roll.combinations[0])
		option_two = self.filter_combo(dice_roll.combinations[1])
		option_three = self.filter_combo(dice_roll.combinations[2])
		all_options = option_one + option_two + option_three
		print(all_options)
		return all_options

	def filter_combo(self, combination):
		return_combo = []
		first_element = combination[0]
		second_element = combination[1]
		first_completed = self.board.columns[first_element-2].completed
		second_completed = self.board.columns[second_element-2].completed
		first_in_turn_cols = (first_element in self.turn_cols)
		second_in_turn_cols = (second_element in self.turn_cols)
		cols_this_turn = len(self.turn_cols)

		if (first_completed and second_completed):
			pass
		elif cols_this_turn == 3:
			first_valid = (not first_completed and first_in_turn_cols)
			second_valid = (not second_completed and second_in_turn_cols)
			if (first_valid):
				if (second_valid):
					return_combo.append([first_element, second_element])
				return_combo.append(first_element)
			elif (second_valid):
				return_combo.append(second_element)
		elif (cols_this_turn == 2):
			if (first_completed):
				return_combo.append(second_element)
			elif (second_completed):
				return_combo.append(first_element)
			elif (not first_in_turn_cols and not second_in_turn_cols):
				return_combo.append(first_element)
				return_combo.append(second_element)
			else:
				return_combo.append([first_element, second_element])
		else:
			if (first_completed):
				return_combo.append(second_element)
			elif (second_completed):
				return_combo.append(first_element)
			else:
				return_combo.append([first_element, second_element])
		return return_combo

