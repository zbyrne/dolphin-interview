from unittest import TestCase
from battledot import BattleNode


class TestBattleNode(TestCase):
    def test_set_victim(self):
        a = BattleNode()
        b = BattleNode()
        a.victim = b
        b.victim = a
        self.assertEqual(a._victim, b)
        self.assertEqual(b._attacker, a)
        self.assertEqual(b._victim, a)
        self.assertEqual(a._attacker, b)

    def test_defend(self):
        a = BattleNode()
        b = BattleNode()
        c = BattleNode()
        a.victim = b
        b.victim = c
        c.victim = a
        b.defend(b.position)
        self.assertEqual(a._victim, c)
        self.assertEqual(c._attacker, a)
