#!/usr/bin/env python3

import requests

def download(url):
    get_response = requests.get(url)
    # print(get_response.content)
    file_name =  url.split("/")[-1]
    with open(file_name, "wb") as out_file: # We create a binary file with wrtite permission and we'll call out_file in the code
        out_file.write(get_response.content)


url = input("Write an url: ")
download(url)