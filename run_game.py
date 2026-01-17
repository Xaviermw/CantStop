import sys

from Components.game import CantStop


def parse_round_logging(args):
	if not args:
		return True
	value = args[0].strip().lower()
	return value in {"true", "1", "yes", "y", "on"}


strategies = ["aggressive", "cautious"]
round_logging = parse_round_logging(sys.argv[1:])

new_game = CantStop(len(strategies), round_logging, strategies=strategies)
players, board = new_game.run_game()

winner = next((player for player in players if player.is_winner), None)
if winner:
	print(f"Winner: Player {winner.player_ref} ({winner.strategy})")
	print(f"Columns won: {winner.columns_won}")
else:
	print("No winner detected.")
