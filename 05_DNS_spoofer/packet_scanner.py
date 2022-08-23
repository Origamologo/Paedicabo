#!/sur/bin/env python3

import subprocess
import netfilterqueue
import scapy.all as scapy

# Modify route: we'll modify the FORWARD chain and trap its content in NFQUEUE O
# iptables -I FORWARD -j NFQUEUE --queue-num 0

subprocess.run('iptables --flush', shell=True)
subprocess.run('iptables -I FORWARD -j NFQUEUE --queue-num 0', shell=True)
# Enabling port forwarding
subprocess.run('echo 1 > /proc/sys/net/ipv4/ip_forward', shell=True)


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    print(scapy_packet.show())
    packet.accept() # allow the connection
    # packet.drop() # to stop the connection


try:
    queue = netfilterqueue.NetfilterQueue()
    # Now we'll connect this queue with the one we created with subprocess
    # and the function 'process_packet' wil be executed in each packet trapped
    # in the queue
    queue.bind(0, process_packet)
    queue.run()
except KeyboardInterrupt:
    subprocess.run('iptables --flush', shell=True)
    print("[+] Detected  CTRL + C ...... Deleting IP tables..... Please wait.\n")