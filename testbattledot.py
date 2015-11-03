import time
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
        a.stop()
        b.stop()

    def test_defend(self):
        a = BattleNode(('localhost', 9902))
        b = BattleNode(('localhost', 9903))
        c = BattleNode(('localhost', 9904))
        a.victim = b.addr
        b.victim = c.addr
        c.victim = a.addr
        a.attack(b.position)
        self.assertEqual(a.victim, c.addr)
        a.stop()
        b.stop()
        c.stop()

    def test_insert(self):
        a = BattleNode(('localhost', 9905))
        b = BattleNode(('localhost', 9906))
        c = BattleNode(('localhost', 9907))
        a.victim = b.addr
        b.victim = a.addr
        c.join(a.addr)
        self.assertEqual(a.victim, c.addr)
        self.assertEqual(c.victim, b.addr)
        a.stop()
        b.stop()
        c.stop()

    def test_drop_node(self):
        a = BattleNode(('localhost', 9908))
        b = BattleNode(('localhost', 9909))
        c = BattleNode(('localhost', 9910))
        a.victim = b.addr
        b.victim = c.addr
        c.victim = a.addr
        time.sleep(1)
        b.stop()
        time.sleep(1)
        self.assertEqual(a.victim, c.addr)
        a.stop()
        c.stop()
