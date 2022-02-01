import threading
import pickle
import socket
from design import UI, root

BUFFER_SIZE = 1024

class User(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self,target=User.run)
        
        self.conn = conn
        self.exit = False
        self.data = ''

    def run(self):
        while not self.exit:
            self.data = self.conn.recv(BUFFER_SIZE)
            app.to_write(self.data.decode())
        self.conn.close()



if __name__ == '__main__':
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((socket.gethostname(),8001))

    user = User(connection)
    user.start()

    app = UI(user=user, master=root, socket=connection)
    root.mainloop()



    
