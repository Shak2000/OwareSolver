import random


class Game:
    """
    Represents an Oware game.
    """

    def __init__(self):
        # The board is a single list of 12 houses.
        # Houses 0-5 belong to the bottom player.
        # Houses 6-11 belong to the top player.
        self.board = [4 for _ in range(12)]
        self.top = 0
        self.bottom = 0
        self.player = ''  # 'T' for top, 'B' for bottom
        self.history = []

    def start(self):
        """Initializes a new game."""
        self.board = [4 for _ in range(12)]
        self.top = 0
        self.bottom = 0
        self.history = []
        if random.randint(1, 2) == 1:
            self.player = 'T'
        else:
            self.player = 'B'
        print(f"A new game has started! Player '{self.player}' goes first.")

    def switch(self):
        """Switches the current player."""
        if self.player == 'T':
            self.player = 'B'
        else:
            self.player = 'T'

    def get_winner(self):
        """Checks for a winner and returns the winner's player character ('T' or 'B'), 'Tie', or None."""
        if self.top > 24 or self.bottom > 24:
            if self.top > self.bottom:
                return 'T'
            elif self.bottom > self.top:
                return 'B'
            else:
                return 'Tie'

        # Check for game end conditions
        if self.capture_top_end():
            return 'T' if self.top > self.bottom else ('B' if self.bottom > self.top else 'Tie')
        if self.capture_bottom_end():
            return 'B' if self.bottom > self.top else ('T' if self.top > self.bottom else 'Tie')

        return None

    def capture_top(self, index):
        """Captures beads for the top player."""
        if 0 <= index < 6:
            while index >= 0 and (1 < self.board[index] < 4):
                self.top += self.board[index]
                self.board[index] = 0
                index -= 1
            return True
        return False

    def capture_bottom(self, index):
        """Captures beads for the bottom player."""
        if 5 < index < 12:
            while index > 5 and (1 < self.board[index] < 4):
                self.bottom += self.board[index]
                self.board[index] = 0
                index -= 1
            return True
        return False

    def capture_top_end(self):
        """End-of-game capture for the top player."""
        # Check if the bottom player has any beads.
        if all(self.board[i] == 0 for i in range(6)):
            # If so, the top player captures all remaining beads on their side.
            self.top += sum(self.board[6:12])
            for i in range(6, 12):
                self.board[i] = 0
            return True
        return False

    def capture_bottom_end(self):
        """End-of-game capture for the bottom player."""
        # Check if the top player has any beads.
        if all(self.board[i] == 0 for i in range(6, 12)):
            # If so, the bottom player captures all remaining beads on their side.
            self.bottom += sum(self.board[0:6])
            for i in range(6):
                self.board[i] = 0
            return True
        return False

    def undo(self):
        """Undoes the last move."""
        if len(self.history) > 0:
            self.board, self.top, self.bottom, self.player = self.history.pop()
            self.switch()
            return True
        return False

    def move(self, house):
        """Executes a move for the current player."""
        # Input validation for house number (1-6)
        if not 1 <= house <= 6:
            print("Invalid move. Please choose a house number between 1 and 6.")
            return False

        # Determine the starting index based on the player and house number
        start_index = 0
        if self.player == 'T':
            start_index = 5 + house
            # Check if the chosen house is empty
            if self.board[start_index] == 0:
                print("Invalid move. You cannot sow from an empty house.")
                return False
        else:  # self.player == 'B'
            start_index = house - 1
            # Check if the chosen house is empty
            if self.board[start_index] == 0:
                print("Invalid move. You cannot sow from an empty house.")
                return False

        # First, check the "feeding" rule: A player must feed an empty opponent's side if possible.
        is_opponent_side_empty = False
        if self.player == 'T':
            if all(self.board[i] == 0 for i in range(6)):
                is_opponent_side_empty = True
        else:  # self.player == 'B'
            if all(self.board[i] == 0 for i in range(6, 12)):
                is_opponent_side_empty = True

        if is_opponent_side_empty:
            feeding_moves = []
            player_start_index = 6 if self.player == 'T' else 0
            player_end_index = 12 if self.player == 'T' else 6
            for i in range(player_start_index, player_end_index):
                if self.board[i] > 0:
                    num_beads = self.board[i]
                    current_index = i
                    temp_board = list(self.board)

                    # Simulate the move to check if it feeds the opponent
                    temp_beads_to_sow = temp_board[i]
                    temp_board[i] = 0

                    while temp_beads_to_sow > 0:
                        current_index = (current_index + 1) % 12
                        temp_board[current_index] += 1
                        temp_beads_to_sow -= 1

                    # Check if any bead landed on the opponent's side
                    if self.player == 'T':
                        # Opponent is 'B', their houses are indices 0-5
                        if any(temp_board[j] > self.board[j] for j in range(6)):
                            feeding_moves.append(i - 5)
                    else:  # self.player == 'B'
                        # Opponent is 'T', their houses are indices 6-11
                        if any(temp_board[j] > self.board[j] for j in range(6, 12)):
                            feeding_moves.append(i + 1)

            if feeding_moves:
                if house not in feeding_moves:
                    print(
                        f"Invalid move. Your opponent's side is empty. You must make a move that feeds them. "
                        f"Possible feeding moves: {sorted(list(set(feeding_moves)))}")
                    return False

        # If the move is valid, proceed with the move.
        self.history.append(([i for i in self.board], self.top, self.bottom, self.player))

        # Sowing the beads
        beads_to_sow = self.board[start_index]
        self.board[start_index] = 0
        current_index = start_index

        while beads_to_sow > 0:
            current_index = (current_index + 1) % 12
            # Skip the starting hole as per Oware rules
            if current_index == start_index:
                continue
            self.board[current_index] += 1
            beads_to_sow -= 1

        # Check for captures
        last_index = current_index
        while True:
            if self.player == 'T':
                if 0 <= last_index < 6:
                    if self.board[last_index] in [2, 3]:
                        self.top += self.board[last_index]
                        self.board[last_index] = 0
                        last_index = (last_index - 1 + 12) % 12
                    else:
                        break
                else:
                    break
            else:  # player 'B'
                if 6 <= last_index < 12:
                    if self.board[last_index] in [2, 3]:
                        self.bottom += self.board[last_index]
                        self.board[last_index] = 0
                        last_index = (last_index - 1 + 12) % 12
                    else:
                        break
                else:
                    break

        return True


def display_board(game):
    """
    Displays the game board with the specified formatting.
    Top houses (player 'T'): indices 11 down to 6.
    Bottom houses (player 'B'): indices 0 up to 5.
    """
    print("-" * 35)
    print("Top Player Score: ", game.top)
    print("     6       5       4       3       2       1  <-- Top Player Houses")
    print("   " + "    ".join([f"[{game.board[i]:2}]" for i in range(11, 5, -1)]))
    print("  " + "-" * 30)
    print("   " + "    ".join([f"[{game.board[i]:2}]" for i in range(6)]))
    print("     1       2       3       4       5       6  <-- Bottom Player Houses")
    print("Bottom Player Score: ", game.bottom)
    print("-" * 35)
    print(f"Current Player: '{game.player}'")


def main():
    """Main function to run the Oware Solver."""
    print("Welcome to the Oware Solver!")
    game = Game()
    game_active = False

    while True:
        if not game_active:
            print("\n(1) Start a new game")
            print("(2) Quit")
            choice = input("Enter your choice: ")
            if choice == '1':
                game.start()
                game_active = True
            elif choice == '2':
                print("Thanks for playing!")
                break
            else:
                print("Invalid choice. Please try again.")
        else:
            display_board(game)

            winner = game.get_winner()
            if winner:
                if winner == 'Tie':
                    print("\nGame Over! It's a tie!")
                else:
                    print(f"\nGame Over! Player '{winner}' wins!")
                game_active = False
                continue

            print("\n(1) Make a move")
            print("(2) Undo move")
            print("(3) Restart game")
            print("(4) Quit")
            choice = input("Enter your choice: ")

            if choice == '1':
                try:
                    move_choice = int(input(f"Player '{game.player}', choose a house to move (1-6): "))
                    if game.move(move_choice):
                        print("Move successful!")
                        game.switch()
                    else:
                        print("Move failed.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            elif choice == '2':
                if game.undo():
                    print("Last move undone.")
                    game.switch()
                else:
                    print("Cannot undo. No moves in history.")
            elif choice == '3':
                game.start()
            elif choice == '4':
                print("Thanks for playing!")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
