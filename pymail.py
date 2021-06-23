#!usr/bin/env python3

from pop3.client import POP3Client

cPOP3 = POP3Client("localhost")
cPOP3.user("user1")
cPOP3.pass_("user1")