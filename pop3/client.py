import socket

# POP3 default port
POP3_PORT = 110

# Line terminators
CR = b'\r'
LF = b'\n'
CRLF = b'\r\n'

# 512 characters (RFC 1939)
MAXLINE = 2048

# Exception raised when an error or invalid response is received:
class error_proto(Exception): pass

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

    def __init__(self, host, port=POP3_PORT, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
        self.host = host
        self.port = port
        self.sock = self.createSocket((self.host, self.port), timeout)
        # self.sock = socket.create_connection((self.host, self.port), timeout)
        self.file = self.sock.makefile("rb")
        self.debug = 2
        self.welcome = self.getResp()

    def createSocket(self, address, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, srcAddress=None):
        host, port = address
        err = None

        for res in socket.getaddrinfo(host, port, 0, socket.SOCK_STREAM):
            af, socktype, proto, _, sa = res
            sock = None
            print(res)

            try:
                sock = socket.socket(af, socktype, proto)

                if timeout is not socket._GLOBAL_DEFAULT_TIMEOUT:
                    sock.settimeout(timeout)
                if srcAddress:
                    sock.bind(srcAddress)
                
                sock.connect(sa)
                err = None
                return sock

            except error as _:
                err = _
                if sock is not None:
                    sock.close()

        if err is not None:
            try:
                raise err
            finally:
                err = None
        else:
            raise error("error in getaddrinfo.")

    def getLine(self):
        line = self.file.readline(MAXLINE + 1)
        if len(line) > MAXLINE:
            raise error_proto("line read > than MAXLINE.")

        if self.debug > 1: print('*getLine*', repr(line))
        if not line: raise error_proto('-ERR EOF')
        lenLine = len(line)
            
        if line[-2:] == CRLF:
            return line[:-2], lenLine
        if line[:1] == CR:
            return line[1:-1], lenLine

        return line[:-1], lenLine

    def getResp(self):
        resp, _ = self.getLine()

        if self.debug > 1: print('*getResp*', repr(resp))
        if not resp.startswith(b'+'):
            raise error_proto(resp)

        return resp
    
    def getLongResponse(self):
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

    def putLine(self, line):
        if self.debug > 1: print("*putLine*", repr(line))
        self.sock.sendall(line + CRLF)

    def putCmd(self, line):
        if self.debug: print("*cmd*", repr(line))
        line = bytes(line, self.encoding)
        self.putLine(line)

    def shortCmd(self, line):
        self.putCmd(line)
        return self.getResp()

    def longCmd(self, line):
        self.putCmd(line)
        return self.getLongResp()

    def setDebug(self, value):
        self.debug = value
    
    # POP cmds

    def user(self, user):
        return self.shortCmd("USER %s" % user)

    def pass_(self, pswd):
        return self.shortCmd("PASS %s" % pswd)

    def repr(self, which):
        return self.longCmd("RETR %s" % which)