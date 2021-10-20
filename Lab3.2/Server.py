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


s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

host =socket.gethostname()
port = 9999
buf =1024
addr = (host,port)


s.sendto(str.encode(file_path),addr)

f=open(file_path,"rb")
data = f.read(buf)
while (data):
    if(s.sendto(data,addr)):
        print("sending ...")
        data = f.read(buf)
s.close()
f.close()