# PyMail
Python program implementing SMTP and POP3 clients for sending and retreiving emails from local servers.

This implementation was built as a final project for a networks and communications course. The topic was sockets and the task build two clients to communicate with local servers.

Notes:
- This implementation just uses basic sockets functionality.
- It's not secure (no SSL support).

Both clients read commads from standard input, send them to the servers and then they show the response.

Requirements:
- Python >= 3
- Local SMTP and POP3 servers running.

Default connection variables:
- For SMTPClient
> SMTP_SERVER_HOST = "localhost", SMTP_PORT = 25

- For POP3Client
> POP3_SERVER_PORT = "localhost", POP3_PORT = 110

How to run it:
> python main.py