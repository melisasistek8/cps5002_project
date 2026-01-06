import random

from environment import Environment, EMPTY
from entities import DekAgent, Thia, ClanMember

GRID_SIZE = 20

DEK = "D"
WILDLIFE = "W"
MONSTER = "M"
THIA = "T"
FATHER = "F"
BROTHER = "B"
TRAP = "X"
KAIJU = "K"


def clan_trial(dek: DekAgent, challenger: ClanMember) -> None:
    dek.stamina -= 2
    power = dek.stamina + (dek.honour * 2)

    if power >= challenger.strength:
        dek.honour += 5
        print(f"Trial: Dek proved his worth against {challenger.role} (+5 honour).")
    else:
        dek.honour -= 5
        dek.health -= 10
        print(f"Trial: Dek failed against {challenger.role} (-5 honour, -10 health).")


def clan_judgement(dek: DekAgent, event: str) -> None:
    if event == "hunt_unworthy":
        dek.honour -= 4
        print("Clan disapproves, hunting the unworthy is forbidden (-4 honour).")
    elif event == "hunt_worthy":
        dek.honour += 3
        print("Clan approves, worthy prey brings honour (+3 honour).")


def move_clan_member(member: ClanMember, env: Environment) -> None:

    "Clan members move one step but only onto EMPTY or DEK. This prevents them overwriting traps, Kaiju or Thia and deleting them."
    
    valid_moves = []
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nx = (member.x + dx) % env.size
        ny = (member.y + dy) % env.size
        if env.grid[ny][nx] in (EMPTY, DEK):
            valid_moves.append((nx, ny))

    if valid_moves:
        member.x, member.y = random.choice(valid_moves)


def main() -> None:
    env = Environment(GRID_SIZE)

    #created dek
    x, y = env.random_empty_cell()
    dek = DekAgent(x, y)

    #thia intel and shield
    thia_trap_shield_used = False
    thia_boss_hint_given = False
    kaiju_alive = True

    #objects
    wx, wy = env.random_empty_cell()
    env.set_cell(wx, wy, WILDLIFE)

    mx, my = env.random_empty_cell()
    env.set_cell(mx, my, MONSTER)

    trap_x, trap_y = env.random_empty_cell()
    env.set_cell(trap_x, trap_y, TRAP)

    kx, ky = env.random_empty_cell()
    env.set_cell(kx, ky, KAIJU)

    #thia
    tx, ty = env.random_empty_cell()
    thia = Thia(tx, ty)
    env.set_cell(thia.x, thia.y, THIA)

    #clan members
    fx, fy = env.random_empty_cell()
    father = ClanMember(fx, fy, "Father")
    env.set_cell(father.x, father.y, FATHER)

    bx, by = env.random_empty_cell()
    brother = ClanMember(bx, by, "Brother")
    env.set_cell(brother.x, brother.y, BROTHER)

    env.set_cell(dek.x, dek.y, DEK)

    for step in range(60):
        env.print_grid()
        print(
            f"Step {step} | Health={dek.health} Stamina={dek.stamina} "
            f"Strength={dek.strength} Honour={dek.honour} Trophies={dek.trophies}"
        )

        env.clear_cell(dek.x, dek.y)
        env.clear_cell(father.x, father.y)
        env.clear_cell(brother.x, brother.y)

        #dek
        dek.move(env)
        cell = env.grid[dek.y][dek.x]

        #meetings w others on gane 
        if cell == WILDLIFE:
            dek.health += 10
            dek.trophies += 1
            dek.strength += 1
            dek.stamina -= 1
            clan_judgement(dek, "hunt_unworthy")
            print(f"Step {step}: Dek hunted wildlife (+10 health, trophy={dek.trophies}).")

        elif cell == MONSTER:
            dek.health -= 25
            dek.stamina -= 3
            if dek.health > 0:
                dek.trophies += 1
                clan_judgement(dek, "hunt_worthy")
                print(f"Step {step}: Dek defeated a monster (-25 health, trophy={dek.trophies}).")
            else:
                print(f"Step {step}: Dek was slain by a monster.")

        elif cell == TRAP:
            health_damage = 5
            stamina_damage = 5

            if dek.carrying_thia and not thia_trap_shield_used:
                health_damage = 2
                stamina_damage = 2
                thia_trap_shield_used = True
                print(f"Step {step}: Thia reduced trap damage (one-time support).")

            dek.health -= health_damage
            dek.stamina -= stamina_damage
            dek.honour -= 1
            print(
                f"Step {step}: Dek triggered a trap (-{health_damage} health, -{stamina_damage} stamina, -1 honour)."
            )

        elif cell == KAIJU:
            if kaiju_alive and dek.strength >= 15 and dek.stamina >= 6:
                kaiju_alive = False
                dek.honour += 10
                dek.trophies += 1
                print(f"Step {step}: Dek defeated the Kaiju! (+10 honour, trophy={dek.trophies})")
                env.set_cell(kx, ky, EMPTY)
                break
            else:
                dek.health -= 40
                dek.stamina -= 6
                dek.honour -= 2
                print(f"Step {step}: Dek confronted the Kaiju (-40 health, -6 stamina, -2 honour).")

        elif cell == THIA:
            if not dek.carrying_thia:
                dek.carrying_thia = True
                env.clear_cell(thia.x, thia.y)  

                clue = thia.provide_clue()
                if clue:
                    print(f"Step {step}: {clue}")
                print(f"Step {step}: Dek is now carrying Thia.")

                if not thia_boss_hint_given and kaiju_alive:
                    print(f"Step {step}: Thia intel: Kaiju detected near ({kx},{ky}).") # thia gives one clue
                    thia_boss_hint_given = True

        elif cell == FATHER:
            clan_trial(dek, father)

        elif cell == BROTHER:
            clan_trial(dek, brother)

        move_clan_member(father, env)
        move_clan_member(brother, env)

        #trial w dek
        if father.x == dek.x and father.y == dek.y:
            clan_trial(dek, father)
        if brother.x == dek.x and brother.y == dek.y:
            clan_trial(dek, brother)

        env.set_cell(dek.x, dek.y, DEK)
        env.set_cell(father.x, father.y, FATHER)
        env.set_cell(brother.x, brother.y, BROTHER)

        if not dek.carrying_thia:
            env.set_cell(thia.x, thia.y, THIA)

        if dek.health <= 0 or dek.stamina <= 0:
            print("Simulation ended: Dek can no longer continue.")
            break

        if dek.honour <= -20:
            print("Clan judgement: Banishment. Dek has broken the code too many times.")
            break


if __name__ == "__main__":
    main()
