class MailBox():
    def __init__(self, emails=[]):
        self.emails = emails

    def show(self):
        for mail in self.emails:
            print(mail)

    def delete(self, id):
        return
    
    def getEmail(self, id):
        return