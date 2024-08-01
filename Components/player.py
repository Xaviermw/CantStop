from .board_elements import Board, Column

class Player:

	column_win_threshold = 3

	def __init__(self, num_players, player_ref):
		self.num_players = num_players
		self.player_ref = player_ref
		self.columns_won = 0
		self.is_winner = False

	def get_player_column_value(self, column_value, board):
		return board.columns[column_value-2].player_scores[self.player_ref]

	def won_column(self):
		self.columns_won += 1
		if (self.columns_won >= column_win_threshold):
			self.is_winner = True
