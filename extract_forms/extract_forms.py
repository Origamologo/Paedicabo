#!/usr/bin/env python3
"""
For boxes always check the url where the input will be submitted to (action)
WITH THE INSPECTOR, AS THE URL CAN BE DIFFERENT FROM THE ONE SHOWN IN THE BROWSER
and the inputs inside the form
"""
import requests
from bs4 import BeautifulSoup
import urllib.parse as urlparse

def request(url):
    try:
        return requests.get(url)
    except requests.exceptions.ConnectionError:
        pass

target_url = "http://192.168.30.137/mutillidae/index.php?page=dns-lookup.php"
response = request(target_url)
# print(response.content) for the html code of the page
parsed_html = BeautifulSoup(response.content, features="lxml")
form_list = parsed_html.findAll("form")
# print(form_list)
for form in form_list:
    action = form.get("action") # to check the url where the input will be submitted
    post_url = urlparse.urljoin(target_url, action)
    # if a relative url starts with / means that the path is the web route;
    # otherwise the path is the current directory
    # print(post_url)
    method = form.get("method") # to check how the info will be submitted
    #print(method)

    inputs_list = form.findAll("input")
    post_data = {}
    for input in inputs_list: # to check all the inputs, both boxes and buttons
        input_name = input.get("name")
        #print(input_name)
        input_type = input.get("type")
        input_value = input.get("value") # if the input is a button (not text) its value will be the one given in the html code by default
        if input_type == "text":
            input_value = "test"

        post_data[input_name] = input_value
        # print(post_data)
    if method == "post":
        result = self.session.post(post_url, data=post_data)
    else:
        result = requests.get(post_url, params=post_data)
    print(result.content)
