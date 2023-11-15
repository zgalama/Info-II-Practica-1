import socket

class Partida:
    def __init__(self, sock1, sock2, n1, n2, id_p):
        self.sockets = [sock1, sock2]
        self.names = [n1, n2]
        self.id = id_p
class Server:
    def __init__(self):
        self.lobby = []
        self.partidas = []
        self.sockets = []

class Cliente:
    def __init__(self, name, sck):
        self.name = name
        self.socket = sck
        self.id = 0






