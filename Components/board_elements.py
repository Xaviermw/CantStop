

class Board:

	column_values = [2,3,4,5,6,7,8,9,10,11,12]
	column_spaces = [3,5,7,9,11,13,11,9,7,5,3]
	def __init__(self, num_players):
		self.columns = []
		self.num_players = num_players
		self.create_columns()

	def create_columns(self):
		for i in range(len(self.column_values)):
			self.columns.append(Column(self.column_values[i], self.column_spaces[i], self.num_players))

class Column:

	def __init__(self, value, spaces, num_players):
		self.value = value
		self.spaces = spaces
		self.num_players = num_players
		self.completed = False
		self.winner = None
		self.player_scores = []
		self.initialize_player_scores()

	def initialize_player_scores(self):
		for i in range(self.num_players):
			self.player_scores.append(0)

	def increment(self, player_ref):
		self.player_scores[player_ref] = min(self.player_scores[player_ref]+1, self.spaces)
		if self.player_scores[player_ref] >= self.spaces:
			self.completed = True
			self.winner = player_ref



