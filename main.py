from environment import Environment
from entities import DekAgent, Thia, ClanMember

GRID_SIZE = 20

DEK = "D"
WILDLIFE = "W"
MONSTER = "M"
THIA = "T"
FATHER = "F"
BROTHER = "R"


def clan_trial(dek: DekAgent, challenger: ClanMember) -> None:
    """Simple trial/combat: honour and health change based on Dek's current power."""
    power = dek.stamina + (dek.honour * 2)

    if power >= challenger.strength:
        dek.honour += 5
        print(f"Trial: Dek proved worth against {challenger.role} (+5 honour).")
    else:
        dek.honour -= 5
        dek.health -= 10
        print(f"Trial: Dek failed against {challenger.role} (-5 honour, -10 health).")


def main() -> None:
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

    # Place Thia (synthetic)
    tx, ty = env.random_empty_cell()
    thia = Thia(tx, ty)
    env.set_cell(thia.x, thia.y, THIA)

    # Place Father + Brother (clan obstacles)
    fx, fy = env.random_empty_cell()
    father = ClanMember(fx, fy, "Father")
    env.set_cell(father.x, father.y, FATHER)

    bx, by = env.random_empty_cell()
    brother = ClanMember(bx, by, "Brother")
    env.set_cell(brother.x, brother.y, BROTHER)

    for step in range(30):
        # Clear old positions (only moving agents)
        env.clear_cell(dek.x, dek.y)
        env.clear_cell(father.x, father.y)
        env.clear_cell(brother.x, brother.y)

        # Dek acts
        dek.move(env)
        cell = env.grid[dek.y][dek.x]

        if cell == WILDLIFE:
            dek.health += 10
            dek.honour += 2
            dek.trophies += 1
            dek.strength += 1 
            print(f"Step {step}: Dek hunted wildlife (+10 health, +2 honour, trophy={dek.trophies}).")

        elif cell == MONSTER:
            dek.health -= 25
            dek.honour -= 1
            print(f"Step {step}: Dek fought a monster (-25 health, -1 honour).")

        elif cell == THIA:
           if not dek.carrying_thia:
            dek.carrying_thia = True
            clue = thia.provide_clue()
            if clue:
             print(f"Step {step}: {clue}")
            print(f"Step {step}: Dek is now carrying Thia (movement costs more stamina).")

        elif cell == FATHER:
            clan_trial(dek, father)

        elif cell == BROTHER:
            clan_trial(dek, brother)

        # Clan members act (patrol)
        father.move(env)
        brother.move(env)

        # Internal conflict: if clan moves onto Dek, trigger trial
        if father.x == dek.x and father.y == dek.y:
            clan_trial(dek, father)
        if brother.x == dek.x and brother.y == dek.y:
            clan_trial(dek, brother)

        # Draw positions back onto the grid
        env.set_cell(dek.x, dek.y, DEK)
        env.set_cell(thia.x, thia.y, THIA)     # Thia is static
        env.set_cell(father.x, father.y, FATHER)
        env.set_cell(brother.x, brother.y, BROTHER)

        # Status line
        print(f"Step {step}: Dek at ({dek.x},{dek.y}) health={dek.health} stamina={dek.stamina} honour={dek.honour} strength={dek.strength}")

        if dek.health <= 0 or dek.stamina <= 0:
            print("Simulation ended: Dek can no longer continue.")
            break

    # Print final grid once (not every step)
    env.print_grid()


if __name__ == "__main__":
    main()
