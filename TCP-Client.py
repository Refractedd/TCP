#  TCP-Client.py - Adapted from echo-client.py https://realpython.com/python-sockets/#echo-client-and-server
#  Created by : Benjamin Williams
#  For        : Telecommunications Programming Project 2
#  Purpose    : The purpose of this project is to create a set of programs in Python to send and receive data over
#       a TCP connection.  There will be two programs written, a server program and a client program.
#       The programs will take ASCII input and process it on the server and send the results back to the client.
#       The server program will listen on TCP port 23456 for TCP connections.
#       It will take the received ASCII data, process it, determine if it is a valid command, and return the results back to the sender.

import socket
import atexit
import sys

# Purpose:  Executes Callback on program exit to ensure that the TCP socket is closed
def exit_handler():
    TCP.close()

# Makes sure that the passed HOST_IP argument is a valid IP Format
def checkIP(HOST_IP):
    syntaxFlag = True
    IP_SPLIT = HOST_IP.split('.')
    for num in IP_SPLIT:
        if not num.isdigit() or int(num) > 255 or int(num) < 0:
            syntaxFlag = False
    return syntaxFlag

# Attempts to start a TCP Connection returns True if successful
def startConnection(HOST_IP):
    try:
        print(f"Connecting to {HOST_IP}...")
        TCP.connect((HOST_IP, PORT))
    except OSError:
        print("Client> Error Connecting to Server.")
        return False
    else:
        print("Connection Successful.")
        return True

# Send Command and get reply
def sendAndRecv(cmd):
    TCP.sendall(bytes(cmd, 'utf-8'))
    return TCP.recv(1024).decode('utf-8')

# Create callback for the exit_handler function to execute upon program termination
atexit.register(exit_handler)

# Initialize the server's IP address from program argument,
if sys.argv[1]:
    HOST_IP = sys.argv[1]
else:
    HOST_IP = None

# Initialize the port used by the server, and byte data reply variables
PORT = 23456
reply = bytes(0)

# Create a TCP Socket labelled TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCP:

    connected = False       # bool for tracking if TCP Connection is successful

    # Attempt Connection until successful
    while not connected:
        if HOST_IP and checkIP(HOST_IP):
            connected = startConnection(HOST_IP)
            if not connected:
                HOST_IP = input("Enter server IP ->")
        else:
            print("Invalid IP Address format { [0-255].[0-255].[0-255].[0-255] }")

    # Continuously send Client inputs until the connection is closed by "QUIT"
    while connected:
        command = input("Client> ")
        reply = sendAndRecv(command)
        print(f"Server> {reply}")

        # Exit case if server replys QUIT, change connected bool to exit bottom of file
        if reply == "QUIT":
            print(f"Closing connection to {HOST_IP}:{PORT}")
            TCP.close()
            print("Exiting Program.")
            connected = False


