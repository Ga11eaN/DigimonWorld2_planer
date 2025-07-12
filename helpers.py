class Fights:
    def __init__(self):
        self.fights = dict()

    def add_fight(self, tree_id, exp):
        self.fights[tree_id] = exp

    def remove_fights(self, tree_id):
        if tree_id in self.fights:
            del self.fights[tree_id]

    def get_fights(self):
        return self.fights

    def get_fights_ids(self):
        return list(self.fights.keys())

    def __repr__(self):
        repr_str = ''
        for k,v in self.fights.items():
            repr_str += f'{k}: {v}\n'
        return repr_str