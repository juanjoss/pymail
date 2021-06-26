# PyMail
Python program implementing SMTP and POP3 clients for sending and retreiving emails from local servers.

This implementation was built as a final project for a networks and communications course. The topic was sockets and the task build two clients to communicate with local servers.

Notes:
- This implementation just uses basic sockets functionality.
- It's not secure (no SSL support).

Commands implemented for POP3:
> USER, PASS, STAT, LIST, RETR, DELE and QUIT.

Commands implemented for SMTP:
> HELO, AUTH LOGIN and QUIT.
