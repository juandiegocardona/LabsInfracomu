import socket
import os
import hashlib
import time
from datetime import datetime


def hash_file(filename):
    h = hashlib.sha1()
    with open(filename, 'rb') as file:
        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)
            h.update(chunk)
    return h.hexdigest()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 8080
buffer_size = 500 * 1024

s.connect((host, port))
s.listen(25)
print("Conexion establecida con {}:{}".format(host, port))
s.sendall("Preparado".encode())

log = datetime.now().strftime("%d-%m-%Y | %H:%M:%S") + " | "

with s, s.makefile('rb') as serverfile:
    thread_num = serverfile.readline().strip().decode()
    filename = serverfile.readline().strip().decode()
    length = int(serverfile.readline())
    log = log + filename + " | " + str(round((length / 1024), 2)) + "KB"
    hash_recibido = serverfile.readline().strip().decode()
    print("Hash recibido: {}".format(hash_recibido))
    initial_length = length
    print(f'Descargando {filename}')
    with open('C' + thread_num + "-" + filename, 'wb') as f:
        while length:
            chunk = min(length, buffer_size)
            data = serverfile.read(chunk)
            if not data: break
            f.write(data)
            length -= len(data)
            print("\r{}% completado".format(round((1 - (length / initial_length)) * 100, 2)), end='', flush=True)
        print("")
        fin = time.time()
        if length != 0:
            print('Descarga invalida')
            log = log + " | Error en descarga"
        else:
            print('Descarga terminada')
            hash_local = hash_file('C' + thread_num + "-" + filename)
            if hash_local == hash_recibido:
                print("Hash Correcto - Enviando Recibido")
                s.sendall("Recibido".encode())
                inicio = float(serverfile.readline().strip().decode())
                tiempo = round(fin - inicio, 2)
                print("Tiempo total: {} segundos".format(tiempo))
                s.sendall(str(tiempo).encode() + b'\n')
                log = log + " | Tiempo: " + str(tiempo) + "s | Exitoso"
            else:
                print("Error en el Hash")
                log = log + " | Error en Hash"

log_file = open('C' + thread_num + "-" + datetime.now().strftime("%d-%m-%Y_%H_%M_%S.txt"), 'w')
log_file.write(log)
log_file.close()
