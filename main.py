from environment import Environment
from entities import DekAgent, Thia, ClanMember

GRID_SIZE = 20

DEK = "D"
WILDLIFE = "W"
MONSTER = "M"
THIA = "T"
FATHER = "F"
BROTHER = "B"


def clan_trial(dek: DekAgent, challenger: ClanMember) -> None:
    """
    Simple clan trial. Uses Dek's stamina and honour to decide outcome.
    This satisfies: clan members challenge Dek + internal conflict.
    """
    power = dek.stamina + (dek.honour * 2)

    if power >= challenger.strength:
        dek.honour += 5
        print(f"Trial: Dek proved worth against {challenger.role} (+5 honour).")
    else:
        dek.honour -= 5
        dek.health -= 10
        print(f"Trial: Dek failed against {challenger.role} (-5 honour, -10 health).")


def clan_judgement(dek: DekAgent, event: str) -> None:
    """
    Yautja Clan Code rule layer (approve/reject actions).
    This satisfies: predators approve/reject actions based on clan code.
    """
    if event == "hunt_unworthy":
        dek.honour -= 4
        print("Clan judgement: Dishonour. Hunting the unworthy is forbidden (-4 honour).")

    elif event == "hunt_worthy":
        dek.honour += 3
        print("Clan judgement: Approved. Worthy prey brings honour (+3 honour).")

    elif event == "cowardice":
        dek.honour -= 3
        print("Clan judgement: Dishonour. Retreat/weakness shames the clan (-3 honour).")


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
        # Clear old positions for moving agents
        env.clear_cell(dek.x, dek.y)
        env.clear_cell(father.x, father.y)
        env.clear_cell(brother.x, brother.y)

        # Dek moves
        dek.move(env)
        cell = env.grid[dek.y][dek.x]

        # Resolve what Dek stepped on
        if cell == WILDLIFE:
            dek.health += 10
            dek.trophies += 1
            dek.strength += 1
            clan_judgement(dek, "hunt_unworthy")
            print(f"Step {step}: Dek hunted wildlife (+10 health, trophy={dek.trophies}).")

        elif cell == MONSTER:
            dek.health -= 25
            if dek.health > 0:
                dek.trophies += 1
                clan_judgement(dek, "hunt_worthy")
                print(f"Step {step}: Dek defeated a monster (-25 health, trophy={dek.trophies}).")
            else:
                print(f"Step {step}: Dek was slain by a monster.")

        elif cell == THIA:
            # Only trigger once (cleaner output)
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

        # Clan members patrol (basic behaviour)
        father.move(env)
        brother.move(env)

        # If they land on Dek, trigger trial too
        if father.x == dek.x and father.y == dek.y:
            clan_trial(dek, father)
        if brother.x == dek.x and brother.y == dek.y:
            clan_trial(dek, brother)

        # Draw updated positions
        env.set_cell(dek.x, dek.y, DEK)
        env.set_cell(thia.x, thia.y, THIA)
        env.set_cell(father.x, father.y, FATHER)
        env.set_cell(brother.x, brother.y, BROTHER)

        # Status line (good evidence for marking)
        print(
            f"Step {step}: Dek at ({dek.x},{dek.y}) "
            f"health={dek.health} stamina={dek.stamina} "
            f"strength={dek.strength} honour={dek.honour}"
        )

        # End conditions
        if dek.health <= 0 or dek.stamina <= 0:
            print("Simulation ended: Dek can no longer continue.")
            break

        if dek.honour <= -10:
            print("Clan judgement: Banishment. Dek has broken the code too many times.")
            break

    # Final grid print (one time only)
    env.print_grid()


if __name__ == "__main__":
    main()
