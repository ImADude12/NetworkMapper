import argparse
import scapy.all as scapy
import pickle
import netifaces as ni
import nmap
import time
import socket
import threading

# TODO: Remove unneeded imports
BIND_PORT = 9000
BIND_ADDR = ('0.0.0.0', BIND_PORT)

# List of new hosts found on the scan
new_hosts = {}


class Host():
    def __init__(self, ip, mac=None, os=None) -> None:
        self.ip = ip
        self.mac = mac
        self.os = os


def get_args():  # TODO: Verify this is positional and must + have help
    # Getting args: sm_ip, sm_port
    parser = argparse.ArgumentParser()
    parser.add_argument('-sI', '--parent_ip', dest='sm_ip',
                        help='scan manager IP Address/Addresses')
    parser.add_argument('-sP', '--parent_ip', dest='sm_port',
                        help='scan manager IP Address/Addresses')
    options = parser.parse_args()

    # Quit the program if the argument is missing
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
        # Check if port is open first
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((ip, BIND_PORT))
        status = False
        if result == 0:
            print('port OPEN')
        else:
            print('port CLOSED')
            if self.send_scanner(ip):
                status = self.run_scanner(ip)
        return status


class Communicator():

    def __init__(self, sm_ip, sm_port) -> None:
        self.sm_ip = sm_ip
        self.sm_port = sm_port

    def init_relay(self) -> None:
        # Start comunication sockets
        fail = True
        while fail:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind(BIND_ADDR)
                # TODO: Verify best number, so that we wont lose connections
                s.listen(100)
                t_hi = threading.Thread(target=self.handle_inputs, args=(s,))
                t_hi.start()
                fail = False
            except socket.error as err:
                print(err)
            wait = 5
            print(
                f'Error setting up relay socket. trying again in {wait} seconds')
            time.sleep(wait)

    def handle_inputs(self, son_sock):
        while True:
            conn, addr = son_sock.accept()
            print(addr[0] + " connected")
            t_rr = threading.Thread(target=self.relay_results, args=(
                conn, addr))  # TODO: Verify syntax is correct
            t_rr.start()

    def send_results(self, results):
        # TODO: Create protocol to send all the data. currently - IP, MAC, OS
        # TODO: Verify success
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # TODO: Verify success
            s.connect((self.sm_ip, self.sm_port))
            s.send(pickle.dumps(results))
            s.close()
        except socket.error as err:
            print('error:', err)

    # Open socket at same port as the scan manager, receive packet and relay it back to scan manager
    def relay_results(self, conn, addr):  # inside thread
        # TODO: Verify success
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.sm_ip, self.sm_port))
            while True:
                data = conn.recv(1024)
                if data and data != b'':
                    s.send(data)
                else:
                    break
        except socket.error as err:
            print('error:', err)

    def close_all(self):
        self.s.close()


# FROM Here: Scanner --------------------------------------------------------------------------------------------------------------
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
            new_hosts[host] = Host(scanner[host]['addresses'])
            try:
                new_hosts[host].mac = scanner[host]['addresses']['mac']
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
    sm_port = 9000
    communicator = Communicator(sm_ip, sm_port)
    # communicator.init_relay()
    nmap_scanner = NmapScanner()
    # Start scanning
    local_ips = get_local_ips()
    for ip in local_ips[0:1]:
        # TODO: in new thread
        hosts = nmap_scanner.arp_pingsweep(ip)
        # nmap_scanner.os_detection(hosts[:4])
        print(new_hosts)
        # OPTIONAL: add information gathering commands

    # TODO: after threads -  Wait for all threads to finish

    # Send results back
    #communicator = Communicator(options.sm_ip, options.sm_port)

    communicator.send_results(new_hosts)

    manager = Manager()
    for host in new_hosts:
        print(host)
        manager.scan_host(host)


main()
