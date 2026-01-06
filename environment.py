import random

EMPTY = "."


class Environment:
    
    "Planet Kalisk."
    

    def __init__(self, size: int):
        self.size = size
        self.grid = [[EMPTY for _ in range(size)] for _ in range(size)]

    def clear_cell(self, x: int, y: int) -> None:
        self.grid[y][x] = EMPTY

    def set_cell(self, x: int, y: int, symbol: str) -> None:
        self.grid[y][x] = symbol

    def random_empty_cell(self) -> tuple[int, int]:
        while True:
            x = random.randrange(self.size)
            y = random.randrange(self.size)
            if self.grid[y][x] == EMPTY:
                return x, y

    def print_grid(self) -> None:
        for row in self.grid:
            print(" ".join(row))
        print()
