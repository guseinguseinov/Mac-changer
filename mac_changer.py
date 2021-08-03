import subprocess
import optparse

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
    return options

def change_mac(interface, macaddress):
    print("[+] Changing mac address for " + interface + " to " + macaddress)

    subprocess.call("ifconfig " + interface + " down", shell=True)
    subprocess.call("ifconfig " + interface + " hw ether " + macaddress, shell=True)
    subprocess.call("ifconfig " + interface + " up", shell=True)

options = get_args()
change_mac(options.interface, options.macaddress)
