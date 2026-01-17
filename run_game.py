from Components.game import CantStop


strategies = ["aggressive", "cautious"]
round_logging = False

new_game = CantStop(len(strategies), round_logging, strategies=strategies)
players, board = new_game.run_game()

winner = next((player for player in players if player.is_winner), None)
if winner:
	print(f"Winner: Player {winner.player_ref} ({winner.strategy})")
	print(f"Columns won: {winner.columns_won}")
else:
	print("No winner detected.")

