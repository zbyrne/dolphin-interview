import random
import socket
from threading import Thread
from SimpleXMLRPCServer import SimpleXMLRPCServer as RPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler as RPCHandler
from xmlrpclib import ServerProxy, Error


socket.setdefaulttimeout(0.2)


BOARD_SIZE = 10


def random_pair():
    return (random.randrange(BOARD_SIZE),
            random.randrange(BOARD_SIZE))


class BattleNode(object):
    def __init__(self, addr):
        self.addr = addr
        self.position = random_pair()
        self._victim = None
        self._victim_addr = None
        self.server = RPCServer(addr,requestHandler=RPCHandler)
        self.server_thread = Thread(target=self.server.serve_forever)
        self.server.register_function(self.defend, 'defend')
        self.server.register_function(self.insert, 'insert')
        self.server_thread.start()

    def __eq__(self, other):
        return self.addr == other.addr

    def __ne__(self, other):
        return self.addr != other.addr

    def __del__(self):
        self.server.shutdown()
        self.server_thread.join()

    @property
    def victim(self):
        return self._victim_addr

    @victim.setter
    def victim(self, val):
        self._victim_addr = tuple(val)
        self._victim = ServerProxy('http://{}:{}'.format(*val))

    def attack(self, pos=None):
        if pos is None:
            pos = random_pair()
        self.victim = self._victim.defend(pos)

    def defend(self, pos):
        if tuple(pos) == self.position:
            return self._victim_addr
        return self.addr

    def insert(self, addr):
        old_victim = self._victim_addr
        self.victim = addr
        return old_victim

    def join(self, addr):
        attacker = ServerProxy('http://{}:{}'.format(*addr))
        self.victim = attacker.insert(self.addr)
