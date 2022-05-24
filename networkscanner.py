import argparse
from asyncio.windows_events import NULL
from mimetypes import init
import scapy.all as scapy
import pickle
import netifaces as ni
import nmap
import socket
import threading

# TODO: Remove unneeded imports
BIND_ADDR = ('0.0.0.0', 1234)
HANDSHAKE_SYN = 'hola'
HANDSHAKE_SYNACK = 'bola'
HANDSHAKE_ACK = 'holabolaa'


# List of new hosts found on the scan
new_hosts = {}


class Host():
    def __init__(self, ip, mac=NULL, os=NULL) -> None:
        self.ip = ip
        self.mac = mac
        self.os = os

# Getting args: sm_ip, sm_port


def get_args():  # TODO: Verify this is positional and must + have help
    parser = argparse.ArgumentParser()
    parser.add_argument('-sI', '--scanmanager_ip', dest='sm_ip',
                        help='scan manager IP Address/Addresses')
    parser.add_argument('-sP', '--scanmanager_port', dest='sm_port',
                        help='scan manager IP Address/Addresses')
    options = parser.parse_args()

    if not options.sm_ip or not options.sm_port:
        # Code to handle if interface is not specified
        parser.error(
            "[-] Please specify an IP Address or Addresses, use --help for more info.")
    return options


class Manager():
    # TODO: Probably should be copied from scan manager
    def send_scanner(self, ip):
        # Sends scanner file to target to initiate scan
        # TODO: GET FROM SAPIR
        pass

    def run_scanner(self, ip):
        # Sends scanner file to target to initiate scan
        # TODO: GET FROM SAPIR
        pass

    def scan_host(self, ip):
        status = False
        if self.send_scanner(ip):
            status = self.run_scanner(ip)
        return status


class Communicator():

    def init_relay(self) -> None:
        # Set up connection to the db
        # Start comunication sockets
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(BIND_ADDR)
        # TODO: Verify best number, so that we wont lose connections
        s.listen(100)
        while True:
            conn, addr = s.accept()
            print(addr[0] + " connected")
            threading.Thread(target=self.handle_scanner_response, args=(
                conn, addr))  # TODO: Verify syntax is correct

    def __init__(self, sm_ip, sm_port) -> None:
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # TODO: Verify success
        # TODO: Handle failure
        self.s.connect((sm_ip, sm_port))

    def send_results(self, results):
        # TODO: Create protocol to send all the data. currently - IP, MAC, OS
        # TODO: Wrap in try catch
        # TODO: Verify success
        # TODO: Handle failure
        self.s.send(pickle.dumps(results))

    def relay_results():
        # TODO: Open socket at same port as the scan manager, receive packet and relay it back to scan manager
        pass

    def close_all(self)
    self.s.close()


class NmapScanner():
    def __init__(self) -> None:
        # TODO: get best ports or how to use nmap defaults
        default_ports = [80, 445, 443, 135, 139, 22, 21, 23]
        self.scanner = nmap.PortScanner()

    def os_detection(self, hosts):
        scanner = nmap.PortScanner()
        hostlist = ' '.join(hosts)
        print('hostlist join:', hostlist)
        scanner.scan(hosts=hostlist, arguments='-O ')
        print('hostlist after scan:', scanner.all_hosts())
        for host in scanner.all_hosts():
            if scanner[host]['osmatch']:
                print(scanner[host]['osmatch'][0]['osclass'][0]['osfamily'])
                new_hosts[host].os = scanner[host]['osmatch'][0]['osclass'][0]['osfamily']

    def udpscan():
        pass

    def arp_pingsweep(self, ip):
        scanner = nmap.PortScanner()
        scanner.scan(hosts=ip + '/24', arguments='-PEPM -sn -n')
        hosts_list = [(x, scanner[x]['status']['state'])
                      for x in scanner.all_hosts()]
        for host, status in hosts_list:
            new_hosts[host] = Host(scanner['192.168.1.42']['addresses'])
            try:
                new_hosts[host].mac = scanner['192.168.1.42']['addresses']['mac']
            except KeyError:
                pass
            print(host, status)
        print('all hosts:', scanner.all_hosts())
        return scanner.all_hosts()
        # self.os_detection(scanner.all_hosts())


def get_local_ips():
    interfaces = ni.interfaces()
    local_ips = []
    for face in interfaces:
        try:
            ip = ni.ifaddresses(face)[ni.AF_INET][0]['addr']
            local_ips.append(ip)
            print(ip)
        except KeyError:
            print('badface', face)
    if '127.0.0.1' in local_ips:
        local_ips.remove('127.0.0.1')
    print(local_ips)
    return local_ips


def main():
    sm_ip = '127.0.0.1'
    sm_port = 1234
    nmap_scanner = NmapScanner()
    # Start scanning
    local_ips = get_local_ips()
    for ip in local_ips:
        # TODO: in new thread
        hosts = nmap_scanner.arp_pingsweep(ip)
        nmap_scanner.os_detection(hosts[:4])
        print(new_hosts)
        # OPTIONAL: add information gathering commands

    # TODO: Wait for all threads to finish

    # Send results back
    #communicator = Communicator(options.sm_ip, options.sm_port)
    communicator = Communicator(sm_ip, sm_port)
    communicator.send_results(new_hosts)

    for host in new_hosts:
        print(host)


def aside():
    # options = get_args()
    # scanned_output = scan(options.target)
    # print(netifaces.interfaces())
    # interfaces = netifaces.interfaces()
    # for interf in interfaces:
    #     scanned_output = arp_scan('192.168.1.0/24', interf)
    #     display_result(scanned_output)
    pass


main()
