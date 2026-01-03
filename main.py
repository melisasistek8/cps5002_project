import random

GRID_SIZE = 20
EMPTY = "."
DEK = "D"
WILDLIFE = "W"
MONSTER = "M"

MOVES = [(1,0), (-1,0), (0,1), (0,-1)]

class Environment:
    def __init__(self, size):
        self.size = size
        self.grid = [[EMPTY for _ in range(size)] for _ in range(size)]

    def clear_cell(self, x, y):
        self.grid[y][x] = EMPTY

    def set_cell(self, x, y, symbol):
        self.grid[y][x] = symbol

    def random_empty_cell(self):
        while True:
            x = random.randrange(self.size)
            y = random.randrange(self.size)
            if self.grid[y][x] == EMPTY:
                return x, y

    def print_grid(self):
        for row in self.grid:
            print(" ".join(row))

class DekAgent:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 100
        self.stamina = 50

    def move(self, env):
        dx, dy = random.choice(MOVES)
        self.x = (self.x + dx) % env.size
        self.y = (self.y + dy) % env.size
        self.stamina -= 1

def main():
    env = Environment(GRID_SIZE)

    # Place Dek
    x, y = env.random_empty_cell()
    dek = DekAgent(x, y)
    env.set_cell(dek.x, dek.y, DEK)

    # Place Wildlife + Monster
    wx, wy = env.random_empty_cell()
    env.set_cell(wx, wy, WILDLIFE)

    mx, my = env.random_empty_cell()
    env.set_cell(mx, my, MONSTER)

    # Simple simulation
    for step in range(20):
        env.clear_cell(dek.x, dek.y)
        dek.move(env)

        cell = env.grid[dek.y][dek.x]
        if cell == WILDLIFE:
            dek.health += 10
            print(f"Step {step}: Dek hunted wildlife (+10 health).")
        elif cell == MONSTER:
            dek.health -= 25
            print(f"Step {step}: Dek fought monster (-25 health).")

        env.set_cell(dek.x, dek.y, DEK)
        print(f"Step {step}: Dek at ({dek.x},{dek.y}) health={dek.health} stamina={dek.stamina}")

    env.print_grid()

if __name__ == "__main__":
    main()
