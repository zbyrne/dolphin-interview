import sys
import random
import socket
import time
from threading import Thread, Lock, Event
from SimpleXMLRPCServer import SimpleXMLRPCServer as RPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler as RPCHandler
from xmlrpclib import ServerProxy, Error


socket.setdefaulttimeout(0.2)


BOARD_SIZE = 10


class SilentRPCHandler(RPCHandler):
    def log_request(*args):
        pass


def random_pair():
    return (random.randrange(BOARD_SIZE),
            random.randrange(BOARD_SIZE))


class BattleNode(object):
    def __init__(self, addr):
        self.addr = addr
        self.position = random_pair()
        self._victim = None
        self._victim_addr = None
        self._victim_lock = Lock()
        self.lost = Event()
        self.server = RPCServer(addr,requestHandler=SilentRPCHandler)
        self.server.register_function(self.defend, 'defend')
        self.server.register_function(self.insert, 'insert')
        self.server.register_function(self.ping, 'ping')
        self.server_thread = Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        self.fail_over = None
        self.loop_event = Event()
        self.loop_thread = Thread(target=self.ping_loop)
        self.loop_thread.daemon = True
        self.loop_thread.start()

    def __eq__(self, other):
        return self.addr == other.addr

    def __ne__(self, other):
        return self.addr != other.addr

    def stop(self):
        self.loop_event.clear()
        self.loop_thread.join()
        self.server.shutdown()
        self.server_thread.join()

    @property
    def victim(self):
        return self._victim_addr

    @victim.setter
    def victim(self, val):
        self._victim_addr = val
        self._victim = ServerProxy('http://{}:{}'.format(*val))
        self.loop_event.set()

    def attack(self, pos=None):
        if pos is None:
            pos = random_pair()
        with self._victim_lock:
            new_victim = tuple(self._victim.defend(pos))
            if new_victim != self.victim:
                self.victim = new_victim
                return True
        return False

    def defend(self, pos):
        if tuple(pos) == self.position:
            self.lost.set()
            return self._victim_addr
        return self.addr

    def insert(self, addr):
        with self._victim_lock:
            old_victim = self._victim_addr
            self.victim = tuple(addr)
            return old_victim

    def join(self, addr):
        attacker = ServerProxy('http://{}:{}'.format(*addr))
        with self._victim_lock:
            self.victim = tuple(attacker.insert(self.addr))

    def ping(self):
        if self.victim:
            return self.victim
        return self.addr

    def ping_victim(self):
        if self.victim:
            try:
                fail_over = tuple(self._victim.ping())
                if fail_over != self.victim:
                    self.fail_over = fail_over
            except IOError:
                if self.loop_event.is_set():
                    self.victim = self.fail_over

    def ping_loop(self):
        self.loop_event.wait()
        while self.loop_event.is_set():
            time.sleep(0.1)
            with self._victim_lock:
                self.ping_victim()


def prompt_for_host_addr():
    while True:
        inp = raw_input("Please enter the <host>:<port> ")
        try:
            host, addr = inp.split(":")
            addr = int(addr)
        except:
            print "Bad format."
            continue
        return host, addr


MENU_STRING = \
"""
1: Specify Victim
2: Insert After Player
3: Attack Victim
4: Quit
Action: 
"""


def main():
    addr = prompt_for_host_addr()
    node = BattleNode(addr)
    while True:
        inp = raw_input(MENU_STRING)
        if node.lost.is_set():
            print "Sorry, you lost."
            node.stop()
            break
        try:
            choice = int(inp)
        except TypeError:
            print "Bad format."
            continue
        if choice not in range(1, 5):
            print "Invalid choice."
            continue
        if choice == 1:
            print "Specify Victim."
            addr = prompt_for_host_addr()
            node.victim = addr
        elif choice == 2:
            print "Insert After Player."
            addr = prompt_for_host_addr()
            node.join(addr)
        elif choice == 3:
            print "Attack Victim."
            if node.attack():
                print "You got him!"
            else:
                print "You missed."
        elif choice == 4:
            print "Good bye!"
            node.stop()
            break
        if node.addr == node.victim:
            print "You're the only player left in this ring. You Won!"
            break


if __name__ == '__main__':
    sys.exit(main())
