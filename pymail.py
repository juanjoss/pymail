from mail.mailbox import MailBox
from pop3.client import POP3Client

cPOP3 = POP3Client()
cPOP3.user("user1")
cPOP3.pass_("user1")

box = MailBox(cPOP3.getEmails())
box.show()
