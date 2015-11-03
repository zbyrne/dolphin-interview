from unittest import TestCase
from battledot import BattleNode


class TestBattleNode(TestCase):
    def test_set_victim(self):
        a = BattleNode(('localhost', 9900))
        b = BattleNode(('localhost', 9901))
        a.victim = b.addr
        b.victim = a.addr
        self.assertEqual(a.victim, b.addr)
        self.assertEqual(b.victim, a.addr)

    def test_defend(self):
        a = BattleNode(('localhost', 9902))
        b = BattleNode(('localhost', 9903))
        c = BattleNode(('localhost', 9904))
        a.victim = b.addr
        b.victim = c.addr
        c.victim = a.addr
        a.attack(b.position)
        self.assertEqual(a.victim, c.addr)

    def test_insert(self):
        a = BattleNode(('localhost', 9905))
        b = BattleNode(('localhost', 9906))
        c = BattleNode(('localhost', 9907))
        a.victim = b.addr
        b.victim = a.addr
        c.join(a.addr)
        self.assertEqual(a.victim, c.addr)
        self.assertEqual(c.victim, b.addr)
