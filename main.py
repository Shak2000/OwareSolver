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

    def move(self, house):
        if 0 < house < 7:
            self.history.append(([i for i in self.board], self.top, self.bottom, self.player))
            start_index = 0
            if self.player == 'T':
                start_index = 12 - house
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
