#  TCP-Server.py - Adapted from echo-server.py https://realpython.com/python-sockets/#echo-client-and-server
#  Created by : Benjamin Williams
#  For        : Telecommunications Programming Project 2
#  Purpose    : The purpose of this project is to create a set of programs in Python to send and receive data over
#       a TCP connection.  There will be two programs written, a server program and a client program.
#       The programs will take ASCII input and process it on the server and send the results back to the client.
#       The server program will listen on TCP port 23456 for TCP connections.
#       It will take the received ASCII data, process it, determine if it is a valid command, and return the results back to the sender.

import socket
from datetime import datetime
import atexit
import sys


# Executes Callback on program exit to ensure that the TCP socket is closed
def exit_handler():
    TCP.close()

# Create callback for the exit_handler function to execute upon program termination
atexit.register(exit_handler)

# Makes sure that the passed HOST_IP argument is a valid IP Format
def checkIP(HOST_IP):
    syntaxFlag = True
    IP_SPLIT = HOST_IP.split('.')
    for num in IP_SPLIT:
        if not num.isdigit() or int(num) > 255 or int(num) < 0:
            syntaxFlag = False
    return syntaxFlag

# Uses datetime library to get and format the time and date string. Then send to client
def getTime():
    now = datetime.now()
    today = now.date()
    time = now.time()
    timestring = time.strftime("%I:%M:%S")  # Server> 2022-10-10 15:44:28.167187
    daystring = today.strftime("%Y-%m-%d ")
    reply = daystring + timestring
    print(f"Server> {daystring} {timestring}")
    conn.sendall(bytes(reply, 'utf-8'))

# Initialize the server's IP address from program arguement,
if sys.argv[1]:
    HOST_IP = sys.argv[1]
else:
    HOST_IP = None
PORT = 23456                    # Port to listen on (non-privileged ports are > 1023)
command = ""                    # initialize client input command string
default = "Invalid Command."    # Default response for unrecognized command
Q = "QUIT"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCP:

    bound = False
    while not bound:
        if HOST_IP and checkIP(HOST_IP):
            try:
                TCP.bind((HOST_IP, PORT))
                TCP.listen()
            except OSError:
                print("TCP Connection failed.")
                HOST_IP = input("Enter new server IP->")
            else:
                bound = True

    print("Server started")
    # Accept Connection as conn and save (IP, PORT) into addr
    conn, addr = TCP.accept()

    with conn:
        print(f"Connected to {addr}")

        # Parse commands until client sends QUIT
        while command != "QUIT":

            # Receive and print command from client
            data = conn.recv(1024)
            command = data.decode('utf-8')
            command.rstrip('b')
            print(f"Client> {command}")

            # Parse Client command
            if command == "TIME":
                getTime()

            elif command == "QUIT":
                conn.sendall(b'QUIT')
                print(f"Server> Closing connection to {HOST_IP}:{PORT}")
                TCP.close()
            else:
                print("Server> Invalid Command")
                conn.sendall(bytes(default, 'utf-8'))


