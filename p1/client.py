import socket
import time

cl_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    cl_socket.connect(('localhost', 5454))
    print('Conectado al Servidor')

    cl_socket.send(input('Tu nombre: ').encode())
    lobby = cl_socket.recv(1024).decode()
    print(lobby)
    comienzo = cl_socket.recv(1024).decode()
    print(comienzo)

    while cl_socket:
        pass

except ConnectionRefusedError:
    print('No se ha podido conectar')

except ConnectionResetError:
    print('La conexión se cerró desde el lado del servidor')

finally:
    cl_socket.close()






