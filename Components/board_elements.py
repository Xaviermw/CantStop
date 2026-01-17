

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

	def format_state(self):
		lines = []
		for column in self.columns:
			status = "completed" if column.completed else "open"
			scores = ", ".join(str(score) for score in column.player_scores)
			lines.append(f"{column.value}: [{scores}] ({status})")
		return "\n".join(lines)

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

	def advance(self, player_ref, steps):
		if self.completed:
			return False
		previous = self.player_scores[player_ref]
		self.player_scores[player_ref] = min(self.player_scores[player_ref] + steps, self.spaces)
		if previous < self.spaces and self.player_scores[player_ref] >= self.spaces:
			self.completed = True
			self.winner = player_ref
			return True
		return False


