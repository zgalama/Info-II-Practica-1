import socket
import threading
import time

from utils_2 import Cliente, Server, Partida, tirar_moneda

s = Server()
id_c = 0 # -- cuando se reinicia el servidor las id empezaran desde 0
id_p = 0

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 5454))

# -- FUNCIONES DEL SERVIDOR --

# -- Funcion que gestiona conexiones entrantes
def conexión_entrante(cl_sock):

    # RECV 1
    name = cl_sock.recv(1024).decode()
    cl = Cliente(name, cl_sock)

    if len(s.lobby) != 2:
        s.lobby.append(cl)
        if len(s.lobby) == 1:
            id_c = 0
            cl_socket.send((f'Lobby: [{s.lobby[0].name}]').encode())
            print(f'Lobby: [{s.lobby[0].name}]')

        else:
            id_c = 1
            cl_socket.send((f'Lobby: [{s.lobby[0].name}, {s.lobby[1].name}]').encode())
            print(f'Lobby: [{s.lobby[0].name, s.lobby[1].name}]')


    return cl

def intercambiar_info_jugadores():
    info_j1 = cl1.socket.recv(1024)
    info_j2 = cl2.socket.recv(1024)

    opo_j1 = cl1.socket.sendall(info_j2)
    opo_j2 = cl2.socket.sendall(info_j1)

# -- Funcion de ejecución del Juego para cada partida (en hilo)

def start_game(cl1, cl2):
    global id_p
    global s
    s.lobby = [] # -- Vaciar el Lobby
    p = Partida(cl1.socket,cl2.socket,cl1.name,cl2.name,id_p) # -- Crear un objeto partida
    id_p += 1 # -- Para que la siguiente partida tenga un id distinto

    s.sockets.extend([cl1.socket,cl2.socket])

    # ENV 1

    mensaje_inicio = (f'Partida comenzada [{cl1.name} vs {cl2.name}]')
    cl1.socket.send(mensaje_inicio.encode())
    cl2.socket.send(mensaje_inicio.encode())

    time.sleep(2)

    # Seleccionar primer turno lanzando una moneda

    turno = p.tirar_moneda()

    if turno == 1:
        cl1.socket.send(str(0).encode())
        cl2.socket.send(str(1).encode())
    elif turno == 0:
        cl1.socket.send(str(1).encode())
        cl2.socket.send(str(0).encode())

    # Confirmacion de que ambos han colocado su equipo

    ok1 = cl1.socket.recv(1024)
    ok2 = cl2.socket.recv(1024)

    time.sleep(1)

    ### - RECIBIR INFO DE J1 Y J2 CON PICKLE
    info_j1 = cl1.socket.recv(1024)
    info_j2 = cl2.socket.recv(1024)

    opo_j1 = cl1.socket.sendall(info_j2)
    opo_j2 = cl2.socket.sendall(info_j1)


    if turno == 0:

        men = cl1.socket.recv(1024)  # Accion j1
        cl2.socket.send(men)

        act = cl1.socket.recv(1024)
        cl2.socket.send(act)

        men = cl2.socket.recv(1024) # Accion j2
        cl1.socket.send(men)

        act = cl2.socket.recv(1024)
        cl1.socket.send(act)

        fin = False

        while not fin:

            men = cl1.socket.recv(1024) # Accion j1
            if men.decode() == 'fin1':
                fin = True
                break
            cl2.socket.send(men)

            act = cl1.socket.recv(1024)
            cl2.socket.send(act)

            act1 = cl1.socket.recv(1024)
            cl2.socket.send(act)

            men = cl2.socket.recv(1024)  # Accion j2
            if men.decode() == 'fin0':
                fin = True
                break
            cl1.socket.send(men)

            act = cl2.socket.recv(1024)
            cl1.socket.send(act)

    if turno == 1:

        men = cl1.socket.recv(1024)  # Accion j1
        cl2.socket.send(men)

        act = cl1.socket.recv(1024)
        cl2.socket.send(act)

        men = cl2.socket.recv(1024)  # Accion j2
        cl1.socket.send(men)

        act = cl2.socket.recv(1024)
        cl1.socket.send(act)

        fin = False

        while not fin:

            men = cl1.socket.recv(1024)  # Accion j1
            if men.decode() == 'fin1':
                fin = True
                break
            cl2.socket.send(men)

            act = cl2.socket.recv(1024)
            cl1.socket.send(act)

            men = cl2.socket.recv(1024)  # Accion j2
            if men.decode() == 'fin0':
                fin = True
                break
            cl1.socket.send(men)

            act = cl2.socket.recv(1024)
            cl1.socket.send(act)

    if men == 'fin0':
        print(f'Ha ganado {p.names[0]}')
    elif men == 'fin1':
        print(f'Ha ganado {p.names[1]}')







# -- PROGRAMA SERVIDOR --

print('-- Servidor operativo -- \n')
server_socket.listen()

while True:

    try:
        cl_socket, addr = server_socket.accept()

        cl = conexión_entrante(cl_socket)
        print(f'Jugador conectado: [{cl.name}]')

        if len(s.lobby) == 2:
            print('Partida comenzada')
            mi_hilo = threading.Thread(target=start_game, args=(s.lobby[0],s.lobby[1]))
            mi_hilo.start()
        else:
            print('Esperando otro jugador...')

    except KeyboardInterrupt:
        print(' - Servidor cerrado - ')
        break

# -- Cerrar servidor --

for socket in s.sockets:
    socket.close()
server_socket.close()

















