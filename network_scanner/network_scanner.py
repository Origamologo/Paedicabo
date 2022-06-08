#!/sur/bin/env python3
# $ route -n to check the router ip
# arp -a to check the ip and mac of the router
import scapy.all as scapy
import argparse
# import os
# import time

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="IP", help="IP adress to ask for its MAC address")
    options = parser.parse_args()
    if not options.IP:
        parser.error("[-] Please specify an IP or IP range, use --help for more info")
    return options


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    # print(arp_request.summary())
    # arp_request.show()
    # broadcast.show()
    # arp_request_broadcast.show()

    clients_list = []
    for element in answered_list:
        client_dict= {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)

    return clients_list

def print_result(result_list):
    print("IP\t\t\tMAC Address\n------------------------------------")
    for client in result_list:
        print(client["ip"] + "\t\t" + client["mac"])

try:
    options = get_arguments()
    ip = options.IP
    scan_result = scan(ip)
    print_result(scan_result)

except:
    ip = input("IP > ")
    scan_result = scan(ip)
    print_result(scan_result)

# def scan(ip):
#     scapy.arping(ip)
#
# scan("192.168.1.1/24")

# print("Turning Wifi off...\n")
# os.system("nmcli radio wifi off")
# time.sleep(5)
# os.system("nmcli radio wifi on")
# print("Starting Wifi...\n")