import random
import copy


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
        # A player wins if they capture more than 24 beads.
        if self.top > 24 or self.bottom > 24:
            if self.top > self.bottom:
                return 'T'
            elif self.bottom > self.top:
                return 'B'
            else:
                return 'Tie'

        # Check for game end conditions where a player's side is empty
        top_side_empty = all(bead == 0 for bead in self.board[6:12])
        bottom_side_empty = all(bead == 0 for bead in self.board[0:6])

        if top_side_empty and self.player == 'T':
            self.bottom += sum(self.board[0:6])
            for i in range(6):
                self.board[i] = 0
            if self.bottom > self.top:
                return 'B'
            elif self.top > self.bottom:
                return 'T'
            else:
                return 'Tie'

        if bottom_side_empty and self.player == 'B':
            self.top += sum(self.board[6:12])
            for i in range(6, 12):
                self.board[i] = 0
            if self.top > self.bottom:
                return 'T'
            elif self.bottom > self.top:
                return 'B'
            else:
                return 'Tie'

        # Check if the game is stalled and no further moves are possible
        if not self.get_possible_moves(self.board, self.player):
            self.top += sum(self.board[6:12])
            self.bottom += sum(self.board[0:6])
            for i in range(12):
                self.board[i] = 0
            if self.top > self.bottom:
                return 'T'
            elif self.bottom > self.top:
                return 'B'
            else:
                return 'Tie'

        return None

    def undo(self):
        """Undoes the last move."""
        if len(self.history) > 0:
            self.board, self.top, self.bottom, self.player = self.history.pop()
            return True
        return False

    def simulate_move(self, house, board, top_score, bottom_score, player):
        """
        Simulates a move on a deep copy of the board state and returns the new state.
        This is for the minimax algorithm and does not modify the game object's state.
        """
        sim_board = copy.deepcopy(board)
        sim_top = top_score
        sim_bottom = bottom_score

        start_index = 0
        if player == 'T':
            start_index = 5 + house
            if sim_board[start_index] == 0:
                return None, None, None
        else:  # player == 'B'
            start_index = house - 1
            if sim_board[start_index] == 0:
                return None, None, None

        # Check feeding rule for simulation
        is_opponent_side_empty = (player == 'T' and all(sim_board[i] == 0 for i in range(6))) or \
                                 (player == 'B' and all(sim_board[i] == 0 for i in range(6, 12)))

        if is_opponent_side_empty:
            can_feed = False
            player_start_index = 6 if player == 'T' else 0
            player_end_index = 12 if player == 'T' else 6
            for i in range(player_start_index, player_end_index):
                if sim_board[i] > 0:
                    temp_beads_to_sow = sim_board[i]
                    temp_board = list(sim_board)
                    temp_board[i] = 0
                    current_index = i
                    while temp_beads_to_sow > 0:
                        current_index = (current_index + 1) % 12
                        temp_board[current_index] += 1
                        temp_beads_to_sow -= 1

                    if player == 'T' and any(temp_board[j] > sim_board[j] for j in range(6)):
                        can_feed = True
                        break
                    elif player == 'B' and any(temp_board[j] > sim_board[j] for j in range(6, 12)):
                        can_feed = True
                        break

            if can_feed:
                current_beads = sim_board[start_index]
                if player == 'T':
                    if start_index + current_beads < 6:
                        return None, None, None
                else:  # player 'B'
                    if (start_index + current_beads) % 12 < 6 and (start_index + current_beads) % 12 > start_index:
                        return None, None, None

        # Sowing the beads
        beads_to_sow = sim_board[start_index]
        sim_board[start_index] = 0
        current_index = start_index

        while beads_to_sow > 0:
            current_index = (current_index + 1) % 12
            if current_index == start_index:
                continue
            sim_board[current_index] += 1
            beads_to_sow -= 1

        last_index = current_index
        while True:
            if player == 'T':
                if 0 <= last_index < 6:
                    if sim_board[last_index] in [2, 3]:
                        sim_top += sim_board[last_index]
                        sim_board[last_index] = 0
                        last_index = (last_index - 1 + 12) % 12
                    else:
                        break
                else:
                    break
            else:  # player 'B'
                if 6 <= last_index < 12:
                    if sim_board[last_index] in [2, 3]:
                        sim_bottom += sim_board[last_index]
                        sim_board[last_index] = 0
                        last_index = (last_index - 1 + 12) % 12
                    else:
                        break
                else:
                    break

        return sim_board, sim_top, sim_bottom

    def move(self, house):
        """Executes a move for the current player on the actual game board."""
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

        # Check the "feeding" rule
        is_opponent_side_empty = False
        if self.player == 'T':
            if all(self.board[i] == 0 for i in range(6)):
                is_opponent_side_empty = True
        else:
            if all(self.board[i] == 0 for i in range(6, 12)):
                is_opponent_side_empty = True

        if is_opponent_side_empty:
            feeding_moves = []
            player_start_index = 6 if self.player == 'T' else 0
            player_end_index = 12 if self.player == 'T' else 6
            for i in range(player_start_index, player_end_index):
                if self.board[i] > 0:
                    temp_state, _, _ = self.simulate_move(i - 5 if self.player == 'T' else i + 1, self.board, self.top,
                                                          self.bottom, self.player)
                    if temp_state:
                        if self.player == 'T' and any(temp_state[j] > self.board[j] for j in range(6)):
                            feeding_moves.append(i - 5)
                        elif self.player == 'B' and any(temp_state[j] > self.board[j] for j in range(6, 12)):
                            feeding_moves.append(i + 1)

            if feeding_moves:
                if house not in set(feeding_moves):
                    print(
                        f"Invalid move. Your opponent's side is empty. You must make a move that feeds them. "
                        f"Possible feeding moves: {sorted(list(set(feeding_moves)))}")
                    return False

        # Save the current state for undo
        self.history.append((copy.deepcopy(self.board), self.top, self.bottom, self.player))

        # Sowing the beads
        beads_to_sow = self.board[start_index]
        self.board[start_index] = 0
        current_index = start_index

        while beads_to_sow > 0:
            current_index = (current_index + 1) % 12
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

    def get_possible_moves(self, board, player):
        """Returns a list of all possible valid moves for the current player."""
        possible_moves = []
        if player == 'T':
            for house in range(6, 12):
                if board[house] > 0:
                    possible_moves.append(house - 5)
        else:  # player 'B'
            for house in range(6):
                if board[house] > 0:
                    possible_moves.append(house + 1)
        return possible_moves

    def evaluate_board(self, board, top_score, bottom_score):
        """
        Evaluates the board state.
        +999 for a top player win, -999 for a bottom player win.
        Otherwise, returns the difference in scores.
        """
        # The game could end in the middle of the minimax tree. Check for a winner.
        temp_game = Game()
        temp_game.board = copy.deepcopy(board)
        temp_game.top = top_score
        temp_game.bottom = bottom_score

        winner = temp_game.get_winner()
        if winner == 'T':
            return 999
        elif winner == 'B':
            return -999
        else:
            return top_score - bottom_score

    def minimax(self, board, top_score, bottom_score, player, depth, alpha, beta):
        """
        Minimax algorithm with alpha-beta pruning.
        Returns the best score and the corresponding move.
        """
        winner = self.get_winner()
        if winner or depth == 0:
            return self.evaluate_board(board, top_score, bottom_score), None

        if player == 'T':  # Maximizing player
            max_eval = float('-inf')
            best_move = None
            moves = self.get_possible_moves(board, player)
            for move_choice in moves:
                new_board, new_top, new_bottom = self.simulate_move(move_choice, board, top_score, bottom_score,
                                                                    player)
                if new_board:
                    val, _ = self.minimax(new_board, new_top, new_bottom, 'B', depth - 1, alpha, beta)
                    if val > max_eval:
                        max_eval = val
                        best_move = move_choice
                    alpha = max(alpha, val)
                    if beta <= alpha:
                        break
            return max_eval, best_move
        else:  # Minimizing player
            min_eval = float('inf')
            best_move = None
            moves = self.get_possible_moves(board, player)
            for move_choice in moves:
                new_board, new_top, new_bottom = self.simulate_move(move_choice, board, top_score, bottom_score,
                                                                    player)
                if new_board:
                    val, _ = self.minimax(new_board, new_top, new_bottom, 'T', depth - 1, alpha, beta)
                    if val < min_eval:
                        min_eval = val
                        best_move = move_choice
                    beta = min(beta, val)
                    if beta <= alpha:
                        break
            return min_eval, best_move

    def ai_move(self, depth):
        """Finds and executes the best move using the minimax algorithm."""
        print(f"Computer ('{self.player}') is thinking with a depth of {depth}...")
        _, best_move = self.minimax(self.board, self.top, self.bottom, self.player, depth, float('-inf'), float('inf'))

        if best_move:
            self.move(best_move)
            print(f"Computer ('{self.player}') chose to move from house {best_move}.")
            self.switch()
            return True
        print("Computer failed to find a valid move.")
        return False


def main():
    def display_board(curr_game):
        """
        Displays the game board with the specified formatting.
        Top houses (player 'T'): indices 11 down to 6.
        Bottom houses (player 'B'): indices 0 up to 5.
        """
        print("-" * 35)
        print("Top Player Score: ", curr_game.top)
        print("     6       5       4       3       2       1  <-- Top Player Houses")
        print("   " + "    ".join([f"[{curr_game.board[i]:2}]" for i in range(11, 5, -1)]))
        print("  " + "-" * 30)
        print("   " + "    ".join([f"[{curr_game.board[i]:2}]" for i in range(6)]))
        print("     1       2       3       4       5       6  <-- Bottom Player Houses")
        print("Bottom Player Score: ", curr_game.bottom)
        print("-" * 35)
        print(f"Current Player: '{curr_game.player}'")

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

            print("\n(1) Make a human move")
            print("(2) Let computer make a move")
            print("(3) Undo last move")
            print("(4) Restart game")
            print("(5) Quit")
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
                try:
                    depth = int(input("Enter minimax depth: "))
                    if game.ai_move(depth):
                        print("Computer move successful!")
                    else:
                        print("Computer move failed.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            elif choice == '3':
                if game.undo():
                    print("Last move undone.")
                    game.switch()
                else:
                    print("Cannot undo. No moves in history.")
            elif choice == '4':
                game.start()
            elif choice == '5':
                print("Thanks for playing!")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
