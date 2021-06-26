import socket
import sys
from email.base64mime import body_encode as encode_base64
from email.base64mime import EMPTYSTRING
import smtplib

# Local server host and port
SMTP_PORT = 25
SMTP_SERVER_HOST = "localhost"

# Line terminators
CRLF = b'\r\n'

# encoding
encoding = "ascii"

# RFC 821
MAXLINE = 1024

class SMTPClient:
    """
        Commands:
        - HELO
        - AUTH LOGIN
        - MAIL FROM
        - RCPT TO
        - DATA
        - RSET
        - QUIT

        user1 = dXNlcjE=
        user2 = dXNlcjI=

        DATA From: User 2 <user2@localhost>\r\nSubject: Test\r\nTo: user1@localhost\r\nHello\r\n.
    """

    def __init__(self):
        self.sock = None
        self.connOpen = False
        self.sendingData = False

        # connecting to server
        self.__connect(SMTP_SERVER_HOST, SMTP_PORT)

    """ connection methods """

    def __connect(self, host=SMTP_SERVER_HOST, port=SMTP_PORT):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

        # connection
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
    c = SMTPClient()

    while c.isOpen():
        c.cmd(input())

if __name__ == '__main__':
    run()