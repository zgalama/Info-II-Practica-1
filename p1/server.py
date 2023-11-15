import socket
import threading
from utils_2 import Cliente, Server, Partida

s = Server()
id_c = 0 # -- cuando se reinicia el servidor las id empezaran desde 0
id_p = 0

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 5454))

# -- FUNCIONES DEL SERVIDOR --
def conexión_entrante(cl_sock):
    name = cl_sock.recv(1024).decode()
    cl = Cliente(name, cl_sock)

    if len(s.lobby) != 2:
        s.lobby.append(cl)
        if len(s.lobby) == 1:
            cl_socket.send(('Esperando oponente...').encode())
        else:
            cl_socket.send(('Rival encontrado').encode())

def start_game(cl1, cl2):
    global id_p
    s.lobby = [] # -- Vaciar el Lobby
    p = Partida(cl1.socket,cl2.socket,cl1.name,cl2.name,id_p) # -- Crear un objeto partida
    id_p += 1 # -- Para que la siguiente partida tenga un id distinto

    s.sockets.extend([cl1.socket,cl2.socket])

    mensaje_inicio = (f'Partida comenzada con {cl1.name} y {cl2.name}')
    cl1.socket.send(mensaje_inicio.encode())
    cl2.socket.send(mensaje_inicio.encode())
    pass


# -- PROGRAMA SERVIDOR --

print('-- Servidor operativo -- \n')
server_socket.listen()

while True:

    try:
        cl_socket, addr = server_socket.accept()

        conexión_entrante(cl_socket)
        print(f'Jugador conectado')

        if len(s.lobby) == 2:
            print('Partida comenzada')
            mi_hilo = threading.Thread(target=start_game, args=(s.lobby[0],s.lobby[1]))
            mi_hilo.start()
        else:
            print('Esperando otro jugador')

    except KeyboardInterrupt:
        print(' - Servidor cerrado - ')
        break

for socket in s.sockets:
    socket.close()
server_socket.close()

















