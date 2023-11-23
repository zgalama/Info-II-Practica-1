import pickle
import socket
import threading
from game import (Jugador)
from utils_2 import print_puntos
from utils_me import limpiar_terminal, pertenencia_a_jugador
import time

cl_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cl_socket_ping = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

def handle_connection(id):

    if id == 0:
        while True:
            cl_socket_ping.send('ok'.encode())
            msg = cl_socket_ping.recv(1024)
            if msg == 'out':
                print('El oponente ha abandonado la partida')
                print('Cerrando programa')
                print_puntos()
                print('Programa cerrado')
                cl_socket_ping.close()
                cl_socket.close()
            time.sleep(3)

    if id == 1:
        while True:
            msg = cl_socket_ping.recv(1024)
            if msg == 'out':
                print('El oponente ha abandonado la partida')
                print('Cerrando programa')
                print_puntos()
                print('Programa cerrado')
                cl_socket_ping.close()
                cl_socket.close()
            time.sleep(3)
            cl_socket_ping.send('ok'.encode())

# -- Programa Cliente --

try:

    print('Conectando con el servidor')
    print_puntos()

    cl_socket.connect(('localhost', 7777))
    cl_socket_ping.connect(('localhost', 7778))

    print('-- Conectado al Servidor --\n')
    print(' -- BIENVENIDOS A TACTICAL BATTLE -- \n')

    # ENV 1

    name = input('Tu nombre: ')
    cl_socket.send(name.encode())

    # RECV 1

    lobby_pos = cl_socket.recv(1024).decode()

    int_lobby = int(lobby_pos)

    conexion = threading.Thread(target=handle_connection, args=(int_lobby,))
    conexion.start()

    comienzo = cl_socket.recv(1024).decode()
    print(comienzo)

    # RECV 2

    elegir_c_cr = cl_socket.recv(1024).decode()

    # ENV 2

    if elegir_c_cr == '1':
        print('\nSe lanzará una moneda para ver quien empieza')
        cl_socket.send(input('Te toca elegir primero 0 (cara), 1 (cruz): ').encode())
    else:
        print('\nSe lanzará una moneda para ver quien empieza')
        print('El rival escoge cara o cruz')

    # RECV 3

    empieza = cl_socket.recv(1024).decode()

    print('Lanzando moneda')

    print_puntos()

    print('\n' + empieza)

    time.sleep(2)

    turno = cl_socket.recv(1024).decode()

    # -- CREAR JUEGO

    j = Jugador()
    pertenencia_a_jugador(j.equipo,j) # Que cada personaje 'sepa' a que equipo pertenece
    j.nombre = name
    j.crear_equipo()

    # -- POSICIONAR EQUIPO

    j.posicionar_equipo()

    input('\nPulsaa INTRO si estas listo')

    print_puntos()

    # -- actualizar datos con oponente

    ser_j = pickle.dumps(j)
    cl_socket.sendall(ser_j)

    time.sleep(1)

    ser_opo = cl_socket.recv(1024)
    opo = pickle.loads(ser_opo)

    j.oponente = opo

    if turno == '1':

        str2 = '0' # Valor inicial sin relevancia, para completar la logica de ejecucion posterior

        while True:

            ser_act_recv = cl_socket.recv(10000)
            act_recv = pickle.loads(ser_act_recv)
            j.oponente = act_recv

            cl_socket.send('ok'.encode())

            ser_eq_recv = cl_socket.recv(3000)
            eq_recv = pickle.loads(ser_eq_recv)
            j.equipo = eq_recv

            j.recibir_accion(str2)

            j.eliminar_personajes_muertos()

            final = j.turno_online()
            if final:
                print(f' - {j.oponente.nombre} HA GANADO LA PARTIDA! - \n')
                cl_socket.send('fin'.encode())
                break

            print(j.informe)

            str1 = j.realizar_accion()
            print('')
            cl_socket.send(str1.encode())

            act_env = pickle.dumps(j)
            cl_socket.sendall(act_env)

            ok = cl_socket.recv(1024)

            ser_eq_env = pickle.dumps(j.oponente.equipo)
            cl_socket.sendall(ser_eq_env)

            print('Esperando la acción del oponente')
            str2 = cl_socket.recv(8000).decode()
            limpiar_terminal()
            if str2 == 'fin':
                print(f' - {j.nombre} HA GANADO LA PARTIDA! - \n')
                break

    if turno == '0':

        while True:

            ser_act_env = pickle.dumps(j)
            cl_socket.sendall(ser_act_env)

            ok = cl_socket.recv(1024)

            ser_eq_env = pickle.dumps(j.oponente.equipo)
            cl_socket.sendall(ser_eq_env)

            print('Esperando la acción del oponente')
            str2 = cl_socket.recv(8000).decode()
            limpiar_terminal()
            if str2 == 'fin':
                print(f' - {j.nombre} HA GANADO LA PARTIDA! - ')
                break

            ser_act1 = cl_socket.recv(10000)
            act1 = pickle.loads(ser_act1)
            j.oponente = act1

            cl_socket.send('ok'.encode())

            ser_eq_recv = cl_socket.recv(3000)
            eq_recv = pickle.loads(ser_eq_recv)
            j.equipo = eq_recv

            j.recibir_accion(str2)

            j.eliminar_personajes_muertos()

            final = j.turno_online()
            if final:
                print(f' - {j.oponente.nombre} HA GANADO LA PARTIDA! - ')
                cl_socket.send('fin'.encode())
                break

            print(j.informe)

            str1 = j.realizar_accion()
            print('')
            cl_socket.send(str1.encode())

except ConnectionRefusedError:
    print('No se ha podido conectar')

except ConnectionResetError:
    print('La conexión se cerró desde el lado del servidor')

finally:
    print('Programa cerrado')
    cl_socket.close()






