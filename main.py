import random


class Game:
    def __init__(self):
        self.board = [4 for i in range(12)]
        self.top = 0
        self.bottom = 0
        self.player = ''
        self.history = []

    def start(self):
        self.board = [4 for i in range(12)]
        self.top = 0
        self.bottom = 0
        self.history = []
        if random.randint(1, 2) == 1:
            self.player = 'T'
        else:
            self.player = 'B'

    def switch(self):
        if self.player == 'T':
            self.player = 'B'
        else:
            self.player = 'T'

    def get_winner(self):
        if self.top == 24 and self.bottom == 24:
            return 'Tie'
        elif self.top > 25:
            return 'T'
        elif self.bottom > 25:
            return 'B'
        else:
            return None

    def capture_top(self, index):
        if 0 <= index < 6:
            while index >= 0 and (1 < self.board[index] < 4):
                self.top += self.board[index]
                index -= 1
            return True
        return False

    def capture_bottom(self, index):
        if 5 < index < 12:
            while index > 5 and (1 < self.board[index] < 4):
                self.bottom += self.board[index]
                index -= 1
            return True
        return False

    def capture_top_end(self):
        for i in range(6):
            if self.board[i] == 0:
                return False
        for i in range(6, 12):
            self.top += self.board[i]
            self.board[i] = 0
        return True

    def capture_bottom_end(self):
        for i in range(6, 12):
            if self.board[i] == 0:
                return False
        for i in range(6):
            self.bottom += self.board[i]
            self.board[i] = 0
        return True

    def move(self, house):
        if 0 < house < 7:
            # First, check the "feeding" rule.
            # A player must feed an empty opponent's side if possible.

            # Determine the opponent's side and check if it's empty
            is_opponent_side_empty = False
            if self.player == 'T':
                # Opponent is 'B', their houses are indices 0-5
                if all(self.board[i] == 0 for i in range(6)):
                    is_opponent_side_empty = True
            else:  # self.player == 'B'
                # Opponent is 'T', their houses are indices 6-11
                if all(self.board[i] == 0 for i in range(6, 12)):
                    is_opponent_side_empty = True

            if is_opponent_side_empty:
                # Find all possible feeding moves for the current player
                feeding_moves = []
                player_start_index = 6 if self.player == 'T' else 0
                player_end_index = 12 if self.player == 'T' else 6

                for i in range(player_start_index, player_end_index):
                    if self.board[i] > 0:
                        # Simulate the move to see if any bead lands on the opponent's side
                        num_beads = self.board[i]
                        current_index = i
                        for _ in range(num_beads):
                            current_index = (current_index + 1) % 12

                            # Check if the bead lands in the opponent's range
                            if self.player == 'T':
                                if 0 <= current_index < 6:
                                    feeding_moves.append(i - 5)  # Convert index to house number (1-6)
                                    break
                            else:  # self.player == 'B'
                                if 6 <= current_index < 12:
                                    feeding_moves.append(i + 1)  # Convert index to house number (1-6)
                                    break

                # If feeding moves are available, the selected move must be one of them
                if feeding_moves:
                    if house not in feeding_moves:
                        print(
                            f"Invalid move. Your opponent's side is empty. You must make a move that feeds them. "
                            f"Possible feeding moves: {feeding_moves}")
                        return False

            # If the move is valid (or the feeding rule doesn't apply), proceed with the move.
            self.history.append(([i for i in self.board], self.top, self.bottom, self.player))

            start_index = 0
            if self.player == 'T':
                start_index = house + 5
            else:
                start_index = house - 1

            # Correctly distribute the beads, skipping the starting house
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

            return True
        return False


def main():
    print("Welcome to the Oware Solver!")


if __name__ == "__main__":
    main()
