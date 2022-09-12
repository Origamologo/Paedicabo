#!/sur/bin/env python

import scapy.all as scapy
import subprocess
from uuid import getnode as get_mac
import socket

hostname=socket.gethostname()
IPAddr=socket.gethostbyname(hostname)
# To allow packets flow:
# sysctl net.ipv4.ip_forward=1

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)

def process_sniffed_packet(packet):
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op ==2: # With op==2 we check if it's a response
        # print(packet.show())
        try:
            real_mac = get_mac(packet[scapy.ARP].psrc)
            response_mac = packet[scapy.ARP].hwsrc

            if real_mac != response_mac:
                if packet[scapy.ARP].hwsrc == '00:0c:29:00:ba:b7':
                    attacker_ip = packet[scapy.ARP].pdst
                    print(f"[+] You are under attack by {attacker_ip}!!!")
                print(f"[+] You are under attack!!")
        except IndexError:
            pass

subprocess.call(['sysctl', 'net.ipv4.ip_forward=1'])
subprocess.run('sysctl net.ipv4.ip_forward=1', shell=True)
sniff("eth0")
