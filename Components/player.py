import random

class Player:

	column_win_threshold = 3

	def __init__(self, num_players, player_ref, strategy="balanced"):
		self.num_players = num_players
		self.player_ref = player_ref
		self.columns_won = 0
		self.is_winner = False
		self.strategy = strategy
		self.completed_columns = set()

	def get_player_column_value(self, column_value, board):
		return board.columns[column_value-2].player_scores[self.player_ref]

	def register_column_win(self, column_value):
		if column_value in self.completed_columns:
			return
		self.completed_columns.add(column_value)
		self.columns_won += 1
		if self.columns_won >= self.column_win_threshold:
			self.is_winner = True

	def choose_option(self, options, board, turn_progress):
		if not options:
			return None
		if self.strategy == "random":
			return random.choice(options)
		if self.strategy == "aggressive":
			return self._choose_highest_progress(options, board, turn_progress)
		if self.strategy == "cautious":
			return self._choose_safest(options, board, turn_progress)
		return self._choose_highest_progress(options, board, turn_progress)

	def decide_stop(self, board, turn_progress, turn_cols):
		if not turn_progress:
			return False
		if self.strategy == "aggressive":
			return self._aggressive_stop(board, turn_progress)
		if self.strategy == "cautious":
			return self._cautious_stop(board, turn_progress)
		return self._balanced_stop(board, turn_progress, turn_cols)

	def _choose_highest_progress(self, options, board, turn_progress):
		def score(option):
			cols = option if isinstance(option, (list, tuple)) else [option]
			return sum(self._column_risk_value(col, board, turn_progress) for col in cols)
		return max(options, key=score)

	def _choose_safest(self, options, board, turn_progress):
		def score(option):
			cols = option if isinstance(option, (list, tuple)) else [option]
			return sum(self._column_completion_value(col, board, turn_progress) for col in cols)
		return max(options, key=score)

	def _column_risk_value(self, column_value, board, turn_progress):
		col = board.columns[column_value-2]
		current = col.player_scores[self.player_ref] + turn_progress.get(column_value, 0)
		return min(current + 1, col.spaces)

	def _column_completion_value(self, column_value, board, turn_progress):
		col = board.columns[column_value-2]
		current = col.player_scores[self.player_ref] + turn_progress.get(column_value, 0)
		return col.spaces - min(current + 1, col.spaces)

	def _aggressive_stop(self, board, turn_progress):
		likely_finish = self._would_finish_column(board, turn_progress)
		return likely_finish and self.columns_won >= (self.column_win_threshold - 1)

	def _cautious_stop(self, board, turn_progress):
		progress = sum(turn_progress.values())
		return progress >= 2

	def _balanced_stop(self, board, turn_progress, turn_cols):
		progress = sum(turn_progress.values())
		finish = self._would_finish_column(board, turn_progress)
		if finish:
			return True
		return progress >= 3 or len(turn_cols) >= 3

	def _would_finish_column(self, board, turn_progress):
		for column_value, delta in turn_progress.items():
			col = board.columns[column_value-2]
			current = col.player_scores[self.player_ref]
			if current + delta >= col.spaces:
				return True
		return False
