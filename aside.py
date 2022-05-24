
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


class snmpscanner():
    def __init__(self) -> None:
        pass

    def login():
        pass

    def scan():
        pass
