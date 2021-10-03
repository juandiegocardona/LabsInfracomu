import socket
from _thread import *
import threading
import ntpath
import os
import hashlib
import time
import queue
from datetime import datetime

thread_count = 0
semaforo = threading.Semaphore()
event = threading.Event()
fecha = datetime.now().strftime("%d-%m-%Y_%H_%M_%S")
file_path = './archivos/1.dummy'

print("Archivos:")
print(" (1) 100MB.txt")
print(" (2) 250MB.mp4")
print("----------------")
archivo = int(input("Archivo a enviar (1 o 2): "))
if archivo == 2:
    file_path = './archivos/2.dummy'
num_clientes = int(input("Ingrese numero de clientes: "))
print("Esperando {} clientes".format(num_clientes))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 8080
buffer_size = 500*1024
s.bind((host, port))
s.listen(25)
print("Escuchando desde: {}:{}".format(host,port))

def hash_file(filename):
   h = hashlib.sha1()
   with open(filename,'rb') as file:
       chunk = 0
       while chunk != b'':
           chunk = file.read(1024)
           h.update(chunk)
   return h.hexdigest()


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def synchronize(count):
    global thread_count
    with semaforo:
        thread_count += 1
        print("Recibidos {} clientes listos".format(thread_count))
        if thread_count == count:
            event.set()
    event.wait()


def threaded(c, thread_count):
    client_ready = c.recv(buffer_size).decode()
    if client_ready == "Preparado":
        synchronize(num_clientes)
        with c,open(file_path, 'rb') as f:
            filename = path_leaf(file_path)
            filesize = f'{os.path.getsize(file_path)}'

            c.sendall(str(thread_count).encode()+b'\n')
            c.sendall(filename.encode()+b'\n')
            c.sendall(filesize.encode() + b'\n')
            c.sendall(hash_file(file_path).encode()+b'\n')

            log = "C" + str(thread_count) + " | " + fecha + " | "
            log = log + filename + " | " + str(round((int(filesize)/1024),2)) + "KB"
            inicio = time.time()
            while True:
                data = f.read(buffer_size)
                if not data: break
                c.sendall(data)
            client_recibido = c.recv(buffer_size).decode()
            if client_recibido == "Recibido":
                print("Enviado con exito a cliente {}".format(thread_count))
                c.sendall(str(inicio).encode()+b'\n')
                tiempo = float(c.recv(buffer_size).decode())
                log = log + " | Tiempo: " + str(tiempo) + "s | Exitoso\n"
            else:
                print("Errores en el envio a cliente {}".format(thread_count))
                log = log + " | Error\n"
    c.close()
    log_file = open("./logs/"+fecha+".txt",'a')
    log_file.write(log)
    log_file.close()


while True:
    c, addr = s.accept()     # Establish connection with client.
    print('Conectado a: {}:{}'.format(addr[0], addr[1]))
    start_new_thread(threaded, (c, thread_count,))