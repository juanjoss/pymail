import sys
from smtp import client as SMTP
from pop3 import client as POP3

# application entry point

if __name__ == "__main__":
    while True:
        print("\n*** Welcome ***\n")
        op = input("* Choose a client (smtp | pop3): ")

        if op.lower() == "smtp":
            SMTP.run()
            sys.exit("\nconnection closed.")
        
        elif op.lower() == "pop3":
            POP3.run()
            sys.exit("\nconnection closed.")
        
        else:
            print("\nclient %s not recognized.\n" % op)