import socket
from email.parser import Parser
from mail.email import Email

# POP3 default port and local server
POP3_PORT = 110
POP3_SERVER_HOST = 'localhost'

# Line terminators
CR = b'\r'
LF = b'\n'
CRLF = b'\r\n'

# 2048 took from poplib. RFC 1939 -> 512 characters
MAXLINE = 2048

# Exception raised when an error or invalid response is received:
class errorProto(Exception): pass

class POP3Client:
    """
        Commands:
            USER string -> string(string)
            PASS string -> pass_(string)
            STAT -> stat()
            LIST[msg] -> list(msg = None)
            RETR msg -> retr(msg)
            DELE msg -> dele(msg)
            QUIT -> quit()
    """

    encoding = "UTF-8"

    def __init__(self):
        self.sock = self.createSocket((POP3_SERVER_HOST, POP3_PORT))
        self.file = self.sock.makefile("rb")
        self.debug = 0
        self.welcome = self.getResp()

    def getEmails(self):
        print("Mailbox Status: %s emails.\n" % self.stat()[0])

        mails = self.list()[1]
        mailBox = []

        for i in range(len(mails)):
            resp, emails, octs = self.repr(i+1)
            
            msgContent = b'\r\n'.join(emails).decode("utf-8")
            msg = Parser().parsestr(msgContent)

            id = i+1
            msgBody = emails[-1].decode('utf-8')
            emailFrom = msg.get('From')
            emailTo = msg.get('To')
            emailSubject = msg.get('Subject')

            e = Email(id, msgBody, emailFrom, emailTo, emailSubject)
            mailBox.append(e)

        return mailBox

    """ POP cmds """

    def user(self, user):
        return self.shortCmd("USER %s" % user)

    def pass_(self, pswd):
        return self.shortCmd("PASS %s" % pswd)

    def stat(self):
        retval = self.shortCmd('STAT')
        rets = retval.split()

        if self.debug: print("- stat: ", repr(rets))

        numMsgs = int(rets[1])
        sizeMsgs = int(rets[2])

        return (numMsgs, sizeMsgs)

    def list(self, which=None):
        """
            If msg number is given -> result is a single response

            If not msg number is given -> 
        """
        if which is not None:
            return self.shortCmd('LIST %s' % which)
        
        return self.longCmd('LIST')

    def repr(self, which):
        return self.longCmd("RETR %s" % which)

    def dele(self, which):
        return self.shortCmd('DELE %s' % which)
    
    def quit(self):
        resp = self.shortCmd('QUIT')
        self.close()
        return resp

    """ Create a socket to the local server """

    def createSocket(self, address, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
        host, port = address
        err = None

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)

            if timeout is not socket._GLOBAL_DEFAULT_TIMEOUT:
                sock.settimeout(timeout)
            
            sock.connect((host, port))
            
            err = None
            return sock
        except err as error:
            err = error
            if sock is not None:
                sock.close()

        if err is not None:
            try:
                raise err
            finally:
                err = None
        else:
            raise err("error in createSocket.")

    def close(self):
        try:
            file = self.file
            self.file = None

            if file is not None:
                file.close()
        finally:
            sock = self.sock
            self.sock = None
            
            if sock is not None:
                try:
                    sock.shutdown(socket.SHUT_RDWR)
                except OSError as exc:
                    raise
                finally:
                    sock.close()


    """ Get helpers """

    def getLine(self):
        line = self.file.readline(MAXLINE + 1)
        if len(line) > MAXLINE:
            raise errorProto("line read > than MAXLINE.")

        if self.debug > 1: print('- getLine: ', repr(line))
        if not line: raise errorProto('-ERR EOF')
        lenLine = len(line)
            
        if line[-2:] == CRLF:
            return line[:-2], lenLine
        if line[:1] == CR:
            return line[1:-1], lenLine

        return line[:-1], lenLine

    def getResp(self):
        resp, _ = self.getLine()

        if self.debug > 1: print('- getResp: ', repr(resp))
        if not resp.startswith(b'+'):
            raise errorProto(resp)

        return resp
    
    def getLongResp(self):
        resp = self.getResp()
        list = []; octets = 0
        line, lenLine = self.getLine()

        while line != b'.':
            if line.startswith(b'..'):
                lenLine -= 1
                line = line[1:]
            
            octets += lenLine
            list.append(line)
            line, lenLine = self.getLine()
        
        return resp, list, octets

    """ Send helpers """

    def putLine(self, line):
        if self.debug > 1: print("- putLine: ", repr(line))
        self.sock.sendall(line + CRLF)

    def putCmd(self, line):
        if self.debug: print("- cmd: ", repr(line))
        line = bytes(line, self.encoding)
        self.putLine(line)

    """ Cmd helpers """
    
    def shortCmd(self, line):
        self.putCmd(line)
        return self.getResp()

    def longCmd(self, line):
        self.putCmd(line)
        return self.getLongResp()

    """ Degun setter """

    def setDebug(self, value):
        self.debug = value