import socket
import time

cl_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    cl_socket.connect(('localhost', 5454))
    print('Conectado al Servidor')

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

    for i in range(3):
        print((i+1) * '.')
        time.sleep(1)

    print('\n' + empieza)

    while cl_socket:
        pass

except ConnectionRefusedError:
    print('No se ha podido conectar')

except ConnectionResetError:
    print('La conexión se cerró desde el lado del servidor')

finally:
    cl_socket.close()






