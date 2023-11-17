import pickle
import socket
from game import (Jugador)
from utils_2 import print_puntos
import time

def act_oponente():
    ser_j = pickle.dumps(j)
    cl_socket.sendall(ser_j)

    time.sleep(1)

    ser_opo = cl_socket.recv(1024)
    opo = pickle.loads(ser_opo)

    j.oponente = opo

cl_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    print('Conectando con el servidor')
    print_puntos()
    cl_socket.connect(('localhost', 5454))

    print('-- Conectado al Servidor --\n')
    print(' -- BIENVENIDOS A TACTICAL BATTLE -- \n')

    # ENV 1

    cl_socket.send(input('Tu nombre: ').encode())

    # RECV 1

    lobby = cl_socket.recv(1024).decode()
    print(lobby)
    comienzo = cl_socket.recv(1024).decode()
    print(comienzo)

    # RECV 2

    elegir_c_cr = cl_socket.recv(1024).decode()

    # ENV 2

    if elegir_c_cr == '1':
        cl_socket.send(input('\nTe toca elegir primero [ 0 (cara), 1 (cruz) ]: ').encode())
    else:
        print('\nEl rival escoge cara o cruz')

    # RECV 3

    empieza = cl_socket.recv(1024).decode()

    print('Lanzando moneda')

    print_puntos()

    print('\n' + empieza)

    time.sleep(2)

    turno = cl_socket.recv(1024).decode()

    # -- CREAR JUEGO

    j = Jugador()
    j.crear_equipo()

    # -- POSICIONAR EQUIPO

    j.posicionar_equipo()

    input('Pulsaa INTRO si estas listo')

    print_puntos()

    # -- actualizar datos con oponente

    ser_j = pickle.dumps(j)
    cl_socket.sendall(ser_j)
    print('informacion sobre jugador enviada (dev)')

    time.sleep(1)

    print('esperando informacion del oponente (dev)')
    ser_opo = cl_socket.recv(1024)
    opo = pickle.loads(ser_opo)
    print('informacion del oponente recivida (dev)')

    j.oponente = opo

    if turno == '1':

        while True:

            print('Esperando actualizacion del estado del equipo rival (dev)')
            ser_act2 = cl_socket.recv(10000)
            print('recibido')
            act2 = pickle.loads(ser_act2)
            j.oponente = act2
            print('oponente actualizado')

            str1 = j.realizar_accion()
            print('')
            cl_socket.send(str1.encode())

            act1 = pickle.dumps(j)
            cl_socket.sendall(act1)

            print("Esperando acción del jugador 0...")
            str2 = cl_socket.recv(1024).decode()
            j.recibir_accion(str2)

            j.eliminar_personajes_muertos()
            final = j.turno_online()
            if final:
                print(' ----- EL JUGADOR 1 HA GANADO LA PARTIDA! ----- ')
                cl_socket.send('fin')
                break

            print(j.informe)

    if turno == '0':

        while True:

            act2 = pickle.dumps(j)
            cl_socket.sendall(act2)
            print('act enviado')

            print("Esperando acción del oponente...")
            str2 = cl_socket.recv(1024).decode()
            print("Recibido:", str2)
            j.recibir_accion(str2)

            print('recibiendo actualizacion de equipo (dev)')
            ser_act1 = cl_socket.recv(10000)
            act1 = pickle.loads(ser_act1)
            j.oponente = act1
            print('oponente actualizado')

            j.eliminar_personajes_muertos()
            final = j.turno_online()
            if final:
                print(' ----- EL JUGADOR 1 HA GANADO LA PARTIDA! ----- ')
                cl_socket.send('fin' + str(id_lobby))
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
    cl_socket.close()






