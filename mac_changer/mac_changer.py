#!/usr/bin/env python

import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info")
    elif not options.new_mac:
        parser.error("[-] Please specify a MAC, use --help for more info")
    return options

def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result.decode("utf-8"))
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address.")

def changeCheck_MAC(interface, new_mac):
    current_mac_1 = get_current_mac(interface)
    change_mac(interface, new_mac)
    current_mac_2 = get_current_mac(interface)
    if current_mac_2 == new_mac:
        print("[+] MAC address was succesfully changed from " + current_mac_1 + " to " + current_mac_2)
    else:
        print("[-] MAC address did not get changed")

try:
    options = get_arguments()
    interface = options.interface
    new_mac = options.new_mac
    changeCheck_MAC(interface, new_mac)

except:
    interface = input("interface > ")
    new_mac = input("new MAC > ")
    changeCheck_MAC(interface, new_mac)