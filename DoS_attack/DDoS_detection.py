import socket
import struct
from datetime import datetime

s = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, 8)

dict = {}

file_txt = open("attack_DDoS.txt",'a') # Text file in append mode to record the attack
t1 = str(datetime.now())
file_txt.writelines(t1) # Write current time
file_txt.writelines("\n")

# We will asume that if a particular IP is hitting for 
# more than 15 times then it would be an attack
No_of_IPs = 15
R_No_of_IPs = No_of_IPs +10
while True:
    pkt = s.recvfrom(2048)
    ipheader = pkt[0][14:34]
    ip_hdr = struct.unpack("!8sB3s4s4s",ipheader)
    IP = socket.inet_ntoa(ip_hdr[3])
    print("The Source of the IP is:"), IP
    
    # Check whether the IP exists in dictionary or not. 
    # If it exists then it will increase it by 1.
    if dict.has_key(IP):
        dict[IP] = dict[IP]+1
        print(dict[IP])
    
    # Remove redundancy
    if (dict[IP] > No_of_IPs) and (dict[IP] < R_No_of_IPs) :
        line = "DDOS attack is Detected: "
        file_txt.writelines(line)
        file_txt.writelines(IP)
        file_txt.writelines("\n")
    else:
        dict[IP] = 1