import scapy.all as scapy
import argparse
import psutil
import netifaces


#addrs = psutil.net_if_addrs()
# print(addrs.keys())


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', dest='target',
                        help='Target IP Address/Adresses')
    options = parser.parse_args()

    # Check for errors i.e if the user does not specify the target IP Address
    # Quit the program if the argument is missing
    # While quitting also display an error message
    if not options.target:
        # Code to handle if interface is not specified
        parser.error(
            "[-] Please specify an IP Address or Addresses, use --help for more info.")
    return options


class remote_login():
    def __init__(self) -> None:
        pass

    def ssh():
        pass

    def wmiexec():
        pass

    def smbclient():
        pass


class local_commands():
    def __init__(self) -> None:
        self.os = self.os_identifier

    def os_identifier():
        pass

    def arp_table():
        pass

    def routing_table():
        pass

    def switch_tables():
        pass


class snmapscanner():
    def __init__(self) -> None:
        pass

    def login():
        pass

    def scan():
        pass


class nmapscanner():
    def __init__(self) -> None:
        # TODO: get best ports or how to use nmap defaults
        default_ports = [80, 445, 443, 135, 139, 22, 21, 23]

    def nmap_arpscan():
        pass

    def nmap_tcpscan():
        pass

    def nmap_udpscan():
        pass

    def nmap_pingsweep():
        pass


class arpscanner():

    def __init__(self) -> None:
        pass

    def arp_scan(ip, interf):  # TODO: Currently Probelm on windows, you need to set interface
        arp_req_frame = scapy.ARP(pdst=ip)

        broadcast_ether_frame = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")

        broadcast_ether_arp_req_frame = broadcast_ether_frame / arp_req_frame

        answered_list = scapy.srp(
            broadcast_ether_arp_req_frame, timeout=1, verbose=False, iface=interf)[0]
        result = []
        for i in range(0, len(answered_list)):
            client_dict = {
                "ip": answered_list[i][1].psrc, "mac": answered_list[i][1].hwsrc}
            result.append(client_dict)

        return result

    def display_result(result):
        print("-----------------------------------\nIP Address\tMAC Address\n-----------------------------------")
        for i in result:
            print("{}\t{}".format(i["ip"], i["mac"]))


# options = get_args()
# scanned_output = scan(options.target)
# print(netifaces.interfaces())
# interfaces = netifaces.interfaces()
# for interf in interfaces:
#     scanned_output = arp_scan('192.168.1.0/24', interf)
#     display_result(scanned_output)
