class LevelExp:
    DATA = {
        1: 0,
        2: 6,
        3: 16,
        4: 33,
        5: 57,
        6: 91,
        7: 138,
        8: 198,
        9: 274,
        10: 369,
        11: 483,
        12: 600,
        13: 760,
        14: 981,
        15: 1281,
        16: 1681,
        17: 2202,
        18: 2862,
        19: 3682,
        20: 4683,
        21: 5883,
        22: 7140,
        23: 8520,
        24: 10080,
        25: 11880,
        26: 13980,
        27: 16440,
        28: 19320,
        29: 22680,
        30: 26580,
        31: 31080,
        32: 35740,
        33: 40640,
        34: 45900,
        35: 51640,
        36: 57980,
        37: 65040,
        38: 72940,
        39: 81800,
        40: 91740,
        41: 102880,
        42: 115340,
        43: 129240,
        44: 144700,
        45: 161840,
        46: 180780,
        47: 201640,
        48: 224540,
        49: 249600,
        50: 277040,
    }

    @classmethod
    def get_total_exp(cls, level: int) -> int | None:
        """Return total experience required for the given level."""
        return cls.DATA.get(level)

def exp_to_next_lvl(level: int, current_exp: int) -> int | None:
    """
    Returns the amount of experience needed to reach the next level.

    Args:
        level (int): Current level (1–49).
        current_exp (int): Total accumulated experience points.

    Returns:
        int | None: Experience points needed to reach next level,
                    or None if max level is reached or level is invalid.
    """
    if level < 1 or level >= 50:
        return None

    current_level_exp = LevelExp.get_total_exp(level)
    next_level_exp = LevelExp.get_total_exp(level + 1)

    if current_level_exp is None or next_level_exp is None:
        return None

    return max(0, next_level_exp - current_exp)


class Digimon:
    id = 0
    def __init__(self, player_name: str, digimon_name: str, lvl=1, exp=0):
        Digimon.id += 1
        self.player_name = player_name
        self.digimon_name = digimon_name
        self.starting_lvl = lvl
        self.lvl = lvl
        self.starting_exp = exp if exp else self.get_exp()
        self.exp = exp if exp else self.get_exp()
        self.fight_ids = list()
        self.id = Digimon.id

    def get_exp(self):
        return LevelExp.get_total_exp(self.lvl)

    def add_exp(self, exp: int):
        self.exp += exp
        self.lvl_up()

    def exp_needed(self):
        return exp_to_next_lvl(self.lvl, self.exp)

    def lvl_up(self):
        if exp_to_next_lvl(self.lvl, self.exp) == 0:
            self.lvl += 1

    def win_fight(self, fight_id):
        self.fight_ids.append(fight_id)

    def remove_fight(self, fight_id):
        if fight_id in self.fight_ids:
            self.fight_ids.remove(fight_id)

    def calculate_exp(self, fights):
        self.exp = self.starting_exp
        self.lvl = self.starting_lvl

        for tree_id in self.fight_ids:
            self.add_exp(fights.get_fights()[tree_id])

    def __repr__(self):
        res_str = ''
        res_str += 'Name: ' + self.player_name + '\n'
        res_str += 'Digimon: ' + self.digimon_name + '\n'
        res_str += 'Exp: ' + str(self.exp) + '\n'
        res_str += 'Lvl: ' + str(self.lvl) + '\n'
        return res_str
