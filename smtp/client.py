import socket
import sys

# Local server host and port
SMTP_PORT = 25
SMTP_SERVER_HOST = "localhost"

# Line terminator
CRLF = b'\r\n'

# encoding
encoding = "latin-1"

# RFC 821
MAXLINE = 1024

class SMTPClient:
    def __init__(self):
        self.sock = None
        self.connOpen = False
        self.sendingData = False

        self.__connect(SMTP_SERVER_HOST, SMTP_PORT)

    # connect and close methods

    def __connect(self, host=SMTP_SERVER_HOST, port=SMTP_PORT):
        """ Creates the socket and starts the connection """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        self.sock.connect((host, port))
        
        if self.sock is None:
            print("\nunable to connect to server.\n")
            sys.exit()

        self.connOpen = True
        resp = self.__resp()

    def __close(self):
        """ Closes the socket connection """
        if self.sock is not None:
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()

    # connection methods

    def __resp(self):
        """ Retreives a response from the server """
        resp = self.sock.recv(MAXLINE)

        for s in resp.split(CRLF):
            if s not in [b'', b'.']:
                print(s.decode(encoding))
        
        if not self.connOpen:
            self.__close()

        return resp

    def __send(self, line):
        """ Encodes and sends a line to the server """
        if "quit" in line.lower():
            self.connOpen = False

        if "data" == line.lower():
            self.sendingData = True
        
        line = bytes(line, encoding)
        self.sock.sendall(line + CRLF)

    def cmd(self, line):
        """ Sends a cmd to the server """
        self.__send(line)
        return self.__resp()

    # setters

    def isConnOpen(self):
        """ Sets the state of the connection """
        return self.connOpen

    def isSendingData(self):
        return self.sendingData

    def setSendingData(self, value=False):
        self.sendingData = value

def run():
    c = SMTPClient()

    data = ""
    while c.isConnOpen():
        if c.isSendingData():
            aux = input()

            if aux == ".":
                c.setSendingData(False)
                data += aux
                c.cmd(data)
            else:
                data += aux + "\r\n"
                
        else:
            c.cmd(input())

if __name__ == '__main__':
    run()