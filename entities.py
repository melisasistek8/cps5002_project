import random

MOVES = [(1, 0), (-1, 0), (0, 1), (0, -1)]


class DekAgent:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.health = 100
        self.stamina = 50
        self.carrying_thia = False
        self.strength = 10

        #clan honours/trophies
        self.honour = 0
        self.trophies = 0

    def move(self, env) -> None:
        dx, dy = random.choice(MOVES)
        self.x = (self.x + dx) % env.size
        self.y = (self.y + dy) % env.size
        self.stamina -= 2 if self.carrying_thia else 1

    def rest(self) -> None:
        self.stamina = min(100, self.stamina + 10)


class Thia:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.damaged = True
        self.provided_clue = False

    def provide_clue(self):
        if not self.provided_clue:
            self.provided_clue = True
            return "Thia warning: Avoid direct contact adversary until stamina is high."
        return None


class ClanMember:
    def __init__(self, x: int, y: int, role: str):
        self.x = x
        self.y = y
        self.role = role
        self.strength = 60 if role == "Father" else 45

    def move(self, env) -> None:
        dx, dy = random.choice(MOVES)
        self.x = (self.x + dx) % env.size
        self.y = (self.y + dy) % env.size
