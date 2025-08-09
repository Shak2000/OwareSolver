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
            self.history.append(([i for i in self.board], self.top, self.bottom, self.player))
            start_index = 0
            if self.player == 'T':
                start_index = house + 5
            else:
                start_index = house - 1
            index = (start_index + 1) % 12
            while self.board[start_index] > 0:
                if index != start_index:
                    self.board[index] += 1
                    self.board[start_index] -= 1
                index = (index + 1) % 12
            return True
        return False


def main():
    print("Welcome to the Oware Solver!")


if __name__ == "__main__":
    main()
