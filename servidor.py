import threading
import socket
import pickle
from tkinter import EXCEPTION


#we create the thread
bd = {'name':[], 'socket':[]}



BUFFER_SIZE = 1024
class Thread(threading.Thread):
    def __init__(self,conn, addr):
        threading.Thread.__init__(self,target=Thread.run)
        #Connection
        self.conn = conn
        self.addr = addr
        self.data = ''
        self.state = False

    def run(self):
        with self.conn:
            print(f'{self.addr} is Online')
            while True:
                self.data = self.conn.recv(BUFFER_SIZE)

                if 'ADD' in self.data.decode() and  not self.state:
                    try:
                        self.state  = True
                        bd['name'].append(self.data.decode()[4:])
                        bd['socket'].append(self.conn)
                        #notification
                        for s in bd['socket']:
                            if s != self.conn:
                                msg = f'{self.data.decode()[4:]},login to chat'
                                s.send(msg.encode())
                    except:
                        self.conn(b'login error')
                
                elif 'TEXT' in self.data.decode() and self.state and 'TEXT TO' not in self.data.decode():
                    try:
                        name = bd['name'][bd['socket'].index(self.conn)]
                        for s in bd['socket']:
                            if s != self.conn:
                                msg = f'{name} says:{self.data.decode()[5:]}'
                                s.send(msg.encode())
                    except:
                        self.conn.send(b'error sending text')

                elif 'C' in self.data.decode():
                    c = 'ADD-> Enter a user | LIST-> Gets the list of connected clients| END-> Disconnect | TEXT-> Send a message to all connected users | TEXT TO-> Send a private message to a user.'
                    self.conn.send(c.encode())

                elif 'LIST' in self.data.decode() and self.state:
                    for el in bd['name']:
                        self.conn.send(el.encode())

                elif 'TEXT TO' in self.data.decode() and self.state:
                    nameOrigen = bd['name'][bd['socket'].index(self.conn)]
                    n = self.data.decode()[8:].split()
                    if n[0] in bd['name']:
                        i = bd['name'].index(n[0])
                        msg = f'{nameOrigen} says:{" ".join(n[1:])} this message is private'
                        bd['socket'][i].send(msg.encode())

                if not self.data:
                    break
                self.conn.send(b"You are online\n")

def create_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((socket.gethostname(),8001))
        s.listen(1)
        while True:
            conn, addr = s.accept()
            Thread(conn, addr).start()


if __name__ == '__main__':
    create_server()