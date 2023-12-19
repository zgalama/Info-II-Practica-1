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
lock_cola_espera = threading.Lock()  # Agrega la declaración del candado aquí

usuarios_lobby = []
partidas_en_curso = []
cola_espera = Cola()

class Partida:
    def __init__(self, j1, j2):
        self.j1 = j1
        self.j2 = j2

class Cliente:
    def __init__(self, nombre, skt):
        self.nombre = nombre
        self.socket = skt

def manejar_cola_espera():
    while True:
        if not cola_espera.vacia() and len(partidas_en_curso) < max_partidas:
            lock_cola_espera.acquire()
            cliente_en_espera = cola_espera.desencolar()
            lock_cola_espera.release()

            lock_partidas.acquire()
            j1 = usuarios_lobby[0]
            j2 = cliente_en_espera
            juego = Partida(j1, j2)
            partidas_en_curso.append(juego)
            threading.Thread(target=jugar_partida, args=(juego,)).start()
            print(f'{len(partidas_en_curso)} partidas en curso')
            lock_partidas.release()

def bienvenida_usuario(clt_socket):
    global lock_lobby,lock_partidas,lock_cola_espera,partidas_en_curso
    global cola_espera
    global max_partidas

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
        j1= usuarios_lobby[0]
        j2=Cliente(nombre_decoded,clt_socket)

        lock_partidas.acquire()
        try:
            if len(partidas_en_curso) < max_partidas:  # Asegurémonos de que no exceda el límite
                juego = Partida(j1, j2)
                partidas_en_curso.append(juego)
                threading.Thread(target=jugar_partida, args=(juego,)).start()
                print(f'{len(partidas_en_curso)} partidas en curso')
            else:
                lock_cola_espera.acquire()
                cola_espera.encolar(j2)
                lock_cola_espera.release()
                print(f'Cliente en cola de espera ({cola_espera.size} en espera)')
        finally:
            lock_partidas.release()

    else:  # Registrar usuario al lobby
        usuarios_lobby.append(Cliente(nombre_decoded, clt_socket))  # Usuario en lobby
        lock_cola_espera.acquire()
        if cola_espera.size != 0 and len(partidas_en_curso) < max_partidas:
            cliente_en_espera = cola_espera.desencolar()
            j1 = cliente_en_espera
            j2 = cliente_en_espera

            lock_partidas.acquire()
            try:
                if len(partidas_en_curso) == max_partidas:
                    cola_espera.encolar(j2)
                    print(f'Cliente en cola de espera ({cola_espera.size} en espera)')

                else:
                    juego = Partida(j1, j2)
                    partidas_en_curso.append(juego)
                    threading.Thread(target=jugar_partida, args=(juego,)).start()
                    print(f'{len(partidas_en_curso)} partidas en curso')
            finally:
                lock_partidas.release()
        lock_cola_espera.release()
    lock_lobby.release()

def terminar_partida():
    global lock_partidas, cola_espera, partidas_en_curso
    lock_partidas.acquire()
    try:
        while len(partidas_en_curso) < max_partidas  and cola_espera.size >= 2:
   
            j1 = cola_espera.desencolar()
            j2 = cola_espera.desencolar()

            juego = Partida(j1,j2)
            partidas_en_curso.append(juego)
            threading.Thread(target=jugar_partida, args=(juego,)).start()
            print(f'{len(partidas_en_curso)} partidas en curso')
    finally:    
            lock_partidas.release()


def jugar_partida(partida):
    global partidas_en_curso
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
            partidas_en_curso.remove(partida)
            terminar_partida()
            break

        # Actualizar el índice del jugador activo
        jugador_activo = (jugador_activo+1) % 2

        turno += 1


print("Arrancando servidor...")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', puerto))
server_socket.listen()

# Imprimir IP del servidor
nombre_server = socket.gethostname()
print(socket.gethostbyname(nombre_server))

try:
     # Inicia un hilo para manejar la cola de espera
    threading.Thread(target=manejar_cola_espera).start()
    while True:
        client_socket, addr = server_socket.accept()
        if client_socket:
            print("Cliente conectado: ", addr)
            threading.Thread(target=bienvenida_usuario, args=(client_socket,)).start()

except KeyboardInterrupt:
    print("Apagado solicitado")

server_socket.close()
print("Apagando servidor...")