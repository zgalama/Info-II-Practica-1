import socket
import time

cl_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    cl_socket.connect(('localhost', 5454))
    print('Conectado al Servidor')

except ConnectionRefusedError:
    print('No se ha podido conectar')

cl_socket.send(input('Tu nombre: ').encode())


