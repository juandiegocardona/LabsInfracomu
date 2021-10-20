import socket
import time
from datetime import datetime

TCP_IP = 'localhost'
TCP_PORT = 9001
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
log = datetime.now().strftime("%d-%m-%Y | %H:%M:%S") + " | "
recived_f = 'imgt_thread'+str(time.time()).split('.')[0]+'.txt'
recived_f += log
with open(recived_f, 'wb') as f:
    print('file opened')
    while True:
        #print('receiving data...')
        data = s.recv(BUFFER_SIZE)
        print('data=%s', (data))
        if not data:
            f.close()
            print('file close()')
            break
        # write data to a file
        f.write(data)



print('Successfully get the file')
s.close()
print('connection closed')
