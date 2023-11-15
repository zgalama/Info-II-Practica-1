import socket
import threading
from utils_2 import Cliente

lobby = []
c_id = 0 # -- cuando se reinicia el servidor las id empezaran desde 0


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 5454))

# -- FUNCIONES DEL SERVIDOR --
def conexión_entrante(cl_sock):
    c_id += 1
    name = cl_sock.recv(1024).decode()
    cl = Cliente(name, cl_sock, c_id)

    if len(lobby) != 2:
        lobby.append(cl)

def start_game(cl1, cl2):
    lobby = []
    pass

# -- PROGRAMA SERVIDOR --

server_socket.listen()

while True:
    cl_socket, addr = server_socket.accept()

    conexión_entrante(cl_socket)
    print(f'Cliente {c_id} conectado')

    if len(lobby) == 2:
        start_game()












