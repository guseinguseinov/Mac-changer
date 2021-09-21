import subprocess
import optparse
import random
import time 


def get_random_MAC():
    mac_address = " "
    for i in range(12):
        n = random.randint(0,9)          
        if i % 2 == 0:
            mac_address += f"{n}"
        else:
            mac_address += f"{n}:"
    mac_address = mac_address.rstrip(mac_address[-1]).strip()
    if int(mac_address[1]) % 2 != 0 or mac_address[1] == "0":
        random_num = random.choice([2,4,6,8])
        if mac_address[1] == mac_address[0]:
            if int(mac_address[0]) > 5:
                mac_address = mac_address.replace(f"{mac_address[0]}",f"{int(mac_address[0])-1}",1)
            else:
                mac_address = mac_address.replace(f"{mac_address[0]}",f"{int(mac_address[0])+1}",1)
        mac_address = mac_address.replace(f"{mac_address[1]}",f"{random_num}", 1)      
    return mac_address

def get_args():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change MAC address")
    parser.add_option("-m", "--mac", dest="macaddress", help="New MAC address")
    (options, arguments) = parser.parse_args() # (options, arguments) = parser.parse_args()
    if not options.interface and not options.macaddress:
        parser.error("[-] Please specify an interface and a MAC address, use --help for mor info.")
    elif not options.interface:
        parser.error("[-] Please specify an interface, use --help for mor info.")
    elif not options.macaddress:
        parser.error("[-] Please specify a MAC address, use --help for mor info.")
    elif options.macaddress == "random":
        options.macaddress = get_random_MAC()
    return options

def change_mac(interface, macaddress):
    time.sleep(1)
    print(f"[+] Changing mac address for {interface} to {macaddress}")
    subprocess.call(f"ifconfig {interface} down", shell=True)
    subprocess.call(f"ifconfig {interface} hw ether {macaddress}", shell=True)
    subprocess.call(f"ifconfig {interface} up", shell=True)

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(f"more /sys/class/net/{interface}/address", shell=True)
    macaddress_result = ifconfig_result[:-1].decode("utf-8") 
    if macaddress_result:
        return f"{macaddress_result}"
    else:
        time.sleep(1)
        print("[-] Could not read Mac address.")

options = get_args()
first_mac = get_current_mac(options.interface)
time.sleep(1)
print("[*] Current MAC > " + first_mac)
change_mac(options.interface, options.macaddress)
second_mac = get_current_mac(options.interface)

time.sleep(1)
if first_mac != second_mac:
    print("[+] MAC address was successfully changed to " + options.macaddress)
else:
    print("[-] MAC address was not changed.")
