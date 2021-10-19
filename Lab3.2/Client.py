from socket import *
import sys
import select
import time
from datetime import datetime

host="0.0.0.0"
port = 9999
s = socket(AF_INET,SOCK_DGRAM)
s.bind((host,port))

log = datetime.now().strftime("%d-%m-%Y | %H:%M:%S") + " | "

addr = (host,port)
buf=1024

data,addr = s.recvfrom(buf)
print("Received File:",data.strip())
f = open(data.strip(),'wb')

data,addr = s.recvfrom(buf)

def file(filename):
 try:
    while(data):
        f.write(data)
        s.settimeout(2)
        data,addr = s.recvfrom(buf)
 except timeout:
    f.close()
    s.close()
    print("File Downloaded")

with s, s.makefile('rb') as serverfile:
    thread_num = serverfile.readline().strip().decode()
    filename = serverfile.readline().strip().decode()
    length = int(serverfile.readline())
    tam = round((length / 1024), 2)
    log = log + filename + " | " + str(tam) + "KB"
    hash_recibido = serverfile.readline().strip().decode()
    print("Hash recibido: {}".format(hash_recibido))
    initial_length = length
    print(f'Descargando {filename}')
    with open('C' + thread_num + "-" + filename, 'wb') as f:
        while length:
            chunk = min(length, buf)
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
            hash_local = file('C' + thread_num + "-" + filename)
            if hash_local == hash_recibido:
                print("Hash Correcto - Enviando Recibido")
                s.sendall("Recibido".encode())
                inicio = float(serverfile.readline().strip().decode())
                tiempo = round(fin - inicio, 2)
                print("Tiempo total: {} segundos".format(tiempo))
                s.sendall(str(tiempo).encode() + b'\n')
                log = log + " | Tiempo: " + str(tiempo) + "s | Paquetes: " + str(initial_length/chunk) +" | Exitoso"
            else:
                print("Error en el Hash")
                log = log + " | Error en Hash"

log_file = open('C' + thread_num + "-" + datetime.now().strftime("%d-%m-%Y_%H_%M_%S.txt"), 'w')
log_file.write(log)
log_file.close()