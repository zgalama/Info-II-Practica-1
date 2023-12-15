import random
import socket
import pickle
import sys
import threading

class Nodo:
    def __init__(self, dato, next):
        self.dato = dato
        self.next = next

class Cola:
    def __init__(self):
        self.first = None
        self.last = None
        self.size = 0

    def vacia(self):
        return self.size == 0

    def peek(self):
        if self.vacia():
            return None
        return self.first.dato

    def encolar(self, dato):
        nodo = Nodo(dato, None)

        if self.vacia():
            self.first = nodo
            self.last = nodo
        else:
            self.last.next = nodo
            self.last = nodo

        self.size += 1

    def desencolar(self):
        if self.vacia():
            return None
        sacar = self.first
        if self.size == 1:
            self.first = None
            self.last = None
        else:
            self.first = self.first.next

        self.size -= 1
        return sacar.dato

puerto = 5555
max_partidas = 1

lock_lobby = threading.Lock()
lock_partidas = threading.Lock()
lock_cola_espera = threading.Lock()

usuarios_lobby = Cola()  # Cambio aquí
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
            j1 = usuarios_lobby.desencolar()  # Cambio aquí
            j2 = cliente_en_espera
            juego = Partida(j1, j2)
            partidas_en_curso.append(juego)
            threading.Thread(target=jugar_partida, args=(juego,)).start()
            print(f'{len(partidas_en_curso)} partidas en curso')
            lock_partidas.release()

def bienvenida_usuario(clt_socket):
    global lock_lobby
    global lock_partidas
    global lock_cola_espera
    global partidas_en_curso
    global cola_espera
    global usuarios_lobby

    nombre = clt_socket.recv(1024)
    if not nombre:
        clt_socket.close()
        print("El cliente ha cancelado la conexión antes de elegir nombre")
        return
    nombre_decoded = nombre.decode()

    lock_lobby.acquire()
    if not usuarios_lobby.vacia():  
        j1 = usuarios_lobby.desencolar()  # Cambio aquí
        j2 = Cliente(nombre_decoded, clt_socket)

        lock_partidas.acquire()
        try:
            if len(partidas_en_curso) < max_partidas:
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

    else:
        usuarios_lobby.encolar(Cliente(nombre_decoded, clt_socket))  
        lock_cola_espera.acquire()
        if cola_espera.size > 0 and len(partidas_en_curso) < max_partidas:
            cliente_en_espera = cola_espera.desencolar()
            j1 = cliente_en_espera
            j2 = usuarios_lobby.desencolar()  # Cambio aquí

            lock_partidas.acquire()
            try:
                if len(partidas_en_curso) < max_partidas:
                    juego = Partida(j1, j2)
                    partidas_en_curso.append(juego)
                    threading.Thread(target=jugar_partida, args=(juego,)).start()
                    print(f'{len(partidas_en_curso)} partidas en curso')
                else:
                    cola_espera.encolar(j2)
                    print(f'Cliente en cola de espera ({cola_espera.size} en espera)')
            finally:
                lock_partidas.release()
        lock_cola_espera.release()
    lock_lobby.release()

def jugar_partida(partida):
    print(f"Partida comenzada entre {partida.j1.nombre} y {partida.j2.nombre}")

    jugadores = [partida.j1, partida.j2]  

    jugadores[0].socket.sendall(jugadores[1].nombre.encode())
    jugadores[1].socket.sendall(jugadores[0].nombre.encode())

    jugador_activo = random.randint(0, 1)
    empieza_j1 = jugador_activo == 0

    jugadores[0].socket.sendall(pickle.dumps(empieza_j1))
    jugadores[1].socket.sendall(pickle.dumps(not empieza_j1))

    jugadores[0].socket.recv(1024)
    jugadores[1].socket.recv(1024)

    turno = 1
    while True:
        print("Ronda", turno, ". Ataca:", jugadores[jugador_activo].nombre, "Defiende:", jugadores[jugador_activo-1].nombre)
        codigo = jugadores[jugador_activo].socket.recv(1024)

        print("Contactando con el oponente para recibir resultado")
        jugadores[jugador_activo-1].socket.sendall(codigo)

        resultado = jugadores[jugador_activo-1].socket.recv(1024)
        resultado_decodificado = pickle.loads(resultado)
        print("Resultado recibido:", resultado_decodificado)

        print("Enviando resultado al atacante")
        jugadores[jugador_activo].socket.sendall(resultado)

        if resultado_decodificado is not None and resultado_decodificado["victoria"]:
            print("Partida terminada. Ha ganado:", jugadores[jugador_activo].nombre)
            break

        jugador_activo = (jugador_activo+1) % 2
        turno += 1

    print(len(partidas_en_curso))

print("Arrancando servidor...")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', puerto))
server_socket.listen()

nombre_server = socket.gethostname()
print(socket.gethostbyname(nombre_server))

try:
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


















