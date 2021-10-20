from socket import *
import socket
from _thread import *
import sys
import os
import ntpath
import time
from datetime import datetime
from threading import Thread

fecha = datetime.now().strftime("%d-%m-%Y_%H_%M_%S")
file_path = './archivos/1.dummy'
file_name= '1.dummy'

print("Archivos:")
print(" (1) 100MB.txt")
print(" (2) 250MB.mp4")
print("----------------")
archivo = int(input("Archivo a enviar (1 o 2): "))
if archivo == 2:
    file_path = './archivos/2.dummy'
    file_name= '2.dummy'
num_clientes = int(input("Ingrese numero de clientes: "))
print("Esperando {} clientes".format(num_clientes))


TCP_IP = 'localhost'
TCP_PORT = 9001
BUFFER_SIZE = 1024


class ClientThread(Thread):

    def __init__(self, ip, port, sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print(" New thread started for "+ip+":"+str(port))

    def run(self):
        filename = file_path
        f = open(filename, 'rb')
        while True:
            l = f.read(BUFFER_SIZE)
            while (l):
                self.sock.send(l)
                #print('Sent ',repr(l))
                l = f.read(BUFFER_SIZE)
            if not l:
                f.close()
                self.sock.close()
                break


tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []

def threaded(c, thread_count):
    client_ready = c.recv(BUFFER_SIZE).decode()
    if client_ready == "Preparado":
        
        with c,open(file_path, 'rb') as f:
            
            filesize = f'{os.path.getsize(file_path)}'

            c.sendall(str(thread_count).encode()+b'\n')
            c.sendall(file_name.encode()+b'\n')
            c.sendall(filesize.encode() + b'\n')

            log = "C" + str(thread_count) + " | " + fecha + " | "
            log = log + file_name + " | " + str(round((int(filesize)/1024),2)) + "KB"
            inicio = time.time()
            while True:
                data = f.read(BUFFER_SIZE)
                if not data: break
                c.sendall(data)
            client_recibido = c.recv(BUFFER_SIZE).decode()
            if client_recibido == "Recibido":
                print("Enviado con exito a cliente {}".format(thread_count))
                c.sendall(str(inicio).encode()+b'\n')
                tiempo = float(c.recv(BUFFER_SIZE).decode())
                log = log + " | Tiempo: " + str(tiempo) + "s | Paquetes: "+str(int(filesize)/BUFFER_SIZE)+" | Exitoso "+"\n"
            else:
                print("Errores en el envio a cliente {}".format(thread_count))
                log = log + " | Error\n"
    c.close()
    log_file = open("./logs/"+fecha+".txt",'a')
    log_file.write(log)
    log_file.close()


while True:
    tcpsock.listen(5)
    print("Waiting for incoming connections...")
    (conn, (ip, port)) = tcpsock.accept()
    print('Got connection from ', (ip, port))
    newthread = ClientThread(ip, port, conn)
    newthread.start()
    threads.append(newthread)

    for t in threads:
       t.join()

