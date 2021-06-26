import socket
import sys

# POP3 default port and local server
POP3_PORT = 110
POP3_SERVER_HOST = "localhost"

# Line terminator
CRLF = b'\r\n'

# encoding
encoding = "latin-1"

# 2048 from poplib. RFC 1939 -> 512
MAXLINE = 2048

class POP3Client:
    """
        Commands:
            - USER
            - PASS
            - STAT
            - LIST
            - RETR
            - DELE
            - QUIT
    """

    def __init__(self):
        self.sock = None
        self.open = False

        self.__connect(POP3_SERVER_HOST, POP3_PORT)

    # connect and close methods

    def __connect(self, host=POP3_SERVER_HOST, port=POP3_PORT):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        self.sock.connect((host, port))
        
        if self.sock is None:
            print("\nunable to connect to server.\n")
            sys.exit()

        self.connOpen = True
        resp = self.__resp()

    def __close(self):
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

        line = bytes(line, encoding)
        self.sock.sendall(line + CRLF)

    def cmd(self, line):
        """ Sends a cmd to the server """
        self.__send(line)
        return self.__resp()

    # setters

    def isOpen(self):
        """ Sets the state of the connection """
        return self.connOpen

def run():
    c = POP3Client()

    while c.isOpen():
        c.cmd(input())

if __name__ == "__main__":
    run()