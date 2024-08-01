import random

class DiceRoll:

	total_dice = 4

	def __init__(self):
		self.dice = []
		self.combinations = []
		for i in range(self.total_dice):
			self.dice.append(random.randint(1,6))
		self.calculate_combinations()

	def calculate_combinations(self):
		self.combinations.append([self.dice[0] + self.dice[1], self.dice[2] + self.dice[3]])
		self.combinations.append([self.dice[0] + self.dice[2], self.dice[1] + self.dice[3]])
		self.combinations.append([self.dice[0] + self.dice[3], self.dice[1] + self.dice[2]])