import subprocess
import optparse
import re

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

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output("ifconfig " + interface, shell=True)
    macaddress_research_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if macaddress_research_result:
        return macaddress_research_result.group(0)  # it will only print the first result that matches.
    else:
        print("[-] Could not read Mac address.")

options = get_args()
current_mac = get_current_mac(options.interface)
print("Current MAC > " + str(current_mac))
change_mac(options.interface, options.macaddress)
current_mac = get_current_mac(options.interface)

if options.macaddress == current_mac:
    print("[+] MAC address was successfully changed to " + options.macaddress)
else:
    print("[-] MAC address was not changed.")
