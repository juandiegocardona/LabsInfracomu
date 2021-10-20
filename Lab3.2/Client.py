import socket
import select
import time
from datetime import datetime

UDP_IP = socket.gethostname()
IN_PORT = 9999
timeout = 3

fecha = datetime.now().strftime("%d-%m-%Y_%H_%M_%S")
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((UDP_IP, IN_PORT))


log = datetime.now().strftime("%d-%m-%Y | %H:%M:%S") + " | "
log_file = open('C'  + "-" + datetime.now().strftime("%d-%m-%Y_%H_%M_%S.txt"), 'w')
log_file.write(log)
log_file.close()


while True:
    data, addr = s.recvfrom(1024)
    if data:
        print("File name:", data)
        file_name = data.strip()

    f = open(file_name, 'wb')

    while True:
        ready = select.select([s], [], [], timeout)
        if ready[0]:
            data, addr = s.recvfrom(1024)
            f.write(data)
        else:
            print ("%s Finish!" % file_name)
            f.close()
            break
 