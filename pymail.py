#!usr/bin/env python3

from pop3.client import ClientPOP3
from smtp.client import ClientSMTP

c1 = ClientSMTP("SMTP")
c2 = ClientPOP3("POP3")

print(c1.getMsg())
print(c2.getMsg())
