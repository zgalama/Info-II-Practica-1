import random
import socket
import pickle
import sys
import threading

from cola import Cola, Nodo

# puerto = int(sys.argv[1])
# max_partidas = int(sys.argv[2])

puerto = 5555
max_partidas = 1

lock_lobby = threading.Lock()
lock_partidas = threading.Lock()
usuarios_lobby = []
partidas = []

class Partida:
    def __init__(self, j1, j2):
        self.j1 = j1
        self.j2 = j2

class Cliente:
    def __init__(self, nombre, skt):
        self.nombre = nombre
        self.socket = skt

def bienvenida_usuario(clt_socket):
    global lock_lobby
    global lock_partidas
    # Elegir nombre de usuario
    nombre = clt_socket.recv(1024)
    if not nombre:
        clt_socket.close()
        print("El cliente ha cancelado la conexión antes de elegir nombre")
        return
    nombre_decoded = nombre.decode()

    # Meter cliente a lobby o emparejar si hay alguien esperando
    lock_lobby.acquire()
    if len(usuarios_lobby) != 0:  # Alguien esperando a jugar, emparejar
        assert len(usuarios_lobby) == 1
        j1 = usuarios_lobby[0]
        del usuarios_lobby[0]
        j2 = Cliente(nombre_decoded, clt_socket)
        lock_partidas.acquire()
        juego = Partida(j1, j2)
        partidas.append(juego)
        lock_partidas.release()
        threading.Thread(target=jugar_partida, args=(juego,)).start()
        print(f'{len(partidas)}')
    else:  # Registrar usuario al lobby
        usuarios_lobby.append(Cliente(nombre_decoded, clt_socket))  # Usuario en lobby
    lock_lobby.release()


def jugar_partida(partida):
    print(f"Partida comenzada entre {partida.j1.nombre} y {partida.j2.nombre}")

    jugadores = [partida.j1, partida.j2]  # Facilitar turnos de jugadores

    # Les damos a conocer
    jugadores[0].socket.sendall(jugadores[1].nombre.encode())
    jugadores[1].socket.sendall(jugadores[0].nombre.encode())

    # Tirar moneda para ver quien empieza
    jugador_activo = random.randint(0, 1)
    empieza_j1 = jugador_activo == 0

    # Les indico quien empieza
    jugadores[0].socket.sendall(pickle.dumps(empieza_j1))
    jugadores[1].socket.sendall(pickle.dumps(not empieza_j1))

    # Espero a que tengan los tableros preparados. TODO Comprobar mensaje?
    jugadores[0].socket.recv(1024)
    jugadores[1].socket.recv(1024)

    # Bucle de turnos
    turno = 1
    while True:
        print("Ronda", turno, ". Ataca:", jugadores[jugador_activo].nombre, "Defiende:", jugadores[jugador_activo-1].nombre)
        # Recibir acción del jugador activo
        codigo = jugadores[jugador_activo].socket.recv(1024)

        # Enviar acción al jugador que espera
        print("Contactando con el oponente para recibir resultado")
        jugadores[jugador_activo-1].socket.sendall(codigo)

        # Recibir resultado del jugador atacado
        resultado = jugadores[jugador_activo-1].socket.recv(1024)
        resultado_decodificado = pickle.loads(resultado)
        print("Resultado recibido:", resultado_decodificado)

        # Enviar resultado de la acción al jugador que atacó
        print("Enviando resultado al atacante")
        jugadores[jugador_activo].socket.sendall(resultado)

        if resultado_decodificado is not None and resultado_decodificado["victoria"]:
            print("Partida terminada. Ha ganado:", jugadores[jugador_activo].nombre)
            # TODO Actualizar algo en la lista de partidas?
            break

        # Actualizar el índice del jugador activo
        jugador_activo = (jugador_activo+1) % 2

        turno += 1

    print(len(partidas))

print("Arrancando servidor...")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', puerto))
server_socket.listen()

# Imprimir IP del servidor
nombre_server = socket.gethostname()
print(socket.gethostbyname(nombre_server))
# Crear objeto cola
cola = Cola()

try:
    while True:
        client_socket, addr = server_socket.accept()
        if client_socket:
            print("Cliente conectado: ", addr)
            threading.Thread(target=bienvenida_usuario, args=(client_socket,)).start()

except KeyboardInterrupt:
    print("Apagado solicitado")

server_socket.close()
print("Apagando servidor...")