import socket
import sys
from email.base64mime import body_encode as encode_base64
from email.base64mime import EMPTYSTRING

# Local server host and port
SMTP_PORT = 25
SMTP_SERVER_HOST = "localhost"

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
    """

    def __init__(self, user, pswd):
        self.sock = None
        self.user = str(user)
        self.pswd = str(pswd)
        self.debug = 1
        self.encoding = "ascii" # encoding
        self.MAXLINE = 1024 # RFC 821
        self.CRLF = "\r\n" # line terminator

        # connecting to server
        self.connect(SMTP_SERVER_HOST, SMTP_PORT)

    """ connection methods """

    def connect(self, host=SMTP_SERVER_HOST, port=SMTP_PORT):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

        # connection
        self.sock.connect((host, port))
        (code, msg) = self.resp()
        
        if code != 220:
            self.close()
            sys.exit("unable to connect to server.\n")

    def sendEmail(self, userAddr="", rcpt=[], subject="", data=""):
        ### for all -> check code ###

        # DATA

        # RCPT TO

        # send date

        # send from

        # send subject

        # send to

        # send data

        # quit

        return

    def close(self):
        sock = self.sock
        self.sock = None
        
        if sock:
            sock.close()
            sys.exit("\nclosing connection...\n")

    """ connection and communication helpers """

    def resp(self):
        if self.sock:
            resp = self.sock.recv(self.MAXLINE)

            if not resp:
                self.close()
                raise Exception("server connection closed.\n")
            if self.debug > 0:
                print("\n- reply: %s" % repr(resp))
            if len(resp) > self.MAXLINE:
                self.close()
                raise Exception("line too long.\n")
            
            try:
                code = int(resp[:3])
            except ValueError:
                code = -1
            
            msg = resp[4:].strip(b'\t\r\n')
        
        return code, msg

    def send(self, line):
        if self.sock:
            try:
                if isinstance(line, str):
                    line = line.encode(self.encoding)

                if self.debug > 0:
                    print("\n- sending: %s" % line)

                self.sock.sendall(line)
            except OSError:
                self.close()
                raise Exception("error sending line to server.\n")
        else:
            raise Exception("socket not available.\n")

    def cmd(self, cmd, args=""):
        if args == "":
            line = '%s%s' % (cmd, self.CRLF)
        else:
            line = '%s %s%s' % (cmd, args, self.CRLF)
        
        self.send(line)

    def sendCmd(self, cmd, args=""):
        self.cmd(cmd, args)
        return self.resp()

    """ SMTP commands """

    def helo(self):
        return self.sendCmd("HELO", self.user)

    def auth(self):
        # AUTH LOGIN
        (code, msg) = self.sendCmd("AUTH LOGIN")

        if self.debug > 0:
            print("\n- AUTH LOGIN: code: %d, msg: %s" % (code, msg))
        if code != 334:
            self.close()
            raise Exception("error in AUTH LOGIN.\n")
        
        # sending user
        (code, msg) = self.sendCmd(
            encode_base64(
                self.user.encode(self.encoding), eol=EMPTYSTRING
            )
        )
        
        if self.debug > 0:
                print("\n- user: %s, encoded: %s" % (self.user, encode_base64(self.user.encode(self.encoding))))
        if code != 334:
            self.close()
            raise Exception("error in auth: user.\n")

        # sending password
        (code, msg) = self.sendCmd(
            encode_base64(
                self.pswd.encode(self.encoding), eol=EMPTYSTRING
            )
        )

        if self.debug > 0:
            print("\n- password: %s, encoded: %s" % (self.user, encode_base64(self.user.encode(self.encoding))))

        # checking auth result
        if code != 235:
            self.close()
            raise Exception("error in auth: password.\n")

    def mailFrom(self):
        return self.sendCmd("MAIL FROM:", self.user)
    
    def rcptTo(self, toAddr=[]):
        resList = []

        for addr in toAddr:
            resList.append(self.sendCmd("RCPT TO:", addr))
        
        return resList

    def data(self):
        return self.sendCmd("DATA")

    def rset(self):
        return self.sendCmd("RSET")

    def quit(self):
        (code, msg) = self.sendCmd("QUIT")

        if self.debug > 0:
            print("\n- QUIT: code: %d, msg: %s" % (code, msg))
        if code == 221:
            self.close()

def run():
    c = SMTPClient("user1", "user1")
    
    while c.isOpen():
        c.cmd(input())

if __name__ == '__main__':
    run()