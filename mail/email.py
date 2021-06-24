class Email:
    def __init__(self, id, emailFrom, emailTo, emailSubject, body):
        self.id = id
        self.emailFrom = emailFrom
        self.emailTo = emailTo
        self.emailSubject = emailSubject
        self.body = body

    def __str__(self):
        return "Id: {}\nFrom: {}\nTo: {}\nSubject: {}\nBody: {}\n".format(
            self.id,
            self.emailFrom,
            self.emailTo,
            self.emailSubject,
            self.body
        )