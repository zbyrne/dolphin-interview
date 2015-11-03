import random
import uuid


BOARD_SIZE = 10


def random_pair():
    return (random.randrange(BOARD_SIZE),
            random.randrange(BOARD_SIZE))


class BattleNode(object):
    def __init__(self):
        self.uuid = uuid.uuid1()
        self.position = random_pair()
        self._victim = None
        self._attacker = None

    def __eq__(self, other):
        return self.uuid == other.uuid

    def __ne__(self, other):
        return self.uuid != other.uuid

    @property
    def victim(self):
        return self._victim

    @victim.setter
    def victim(self, val):
        self._victim = val
        self._victim.attacker = self

    @property
    def attacker(self):
        return self._attacker

    @attacker.setter
    def attacker(self, val):
        self._attacker = val

    def attack(self):
        pos = random_pair()
        self._victim.defend(pos)

    def defend(self, pos):
        if pos == self.position:
            self._attacker.victim = self._victim
