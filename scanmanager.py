from unicodedata import name
import scapy.all as scapy
import argparse
import netifaces as ni
import socket
import threading

# TODO: Remove unneeded imports

# List of new hosts to scan
new_hosts = []
# List of hosts already scanned, so that we wont scan them twice
scanned_hosts = []
# List of hosts failed to scan, maybe they were down
failure_hosts = []

BIND_ADDR = ('0.0.0.0', 1234)
HANDSHAKE_SYN = 'hola'
HANDSHAKE_SYNACK = 'bola'
HANDSHAKE_ACK = 'holabolaa'


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', dest='target',
                        help='Target IP Address/Addresses')
    options = parser.parse_args()

    # Check for errors i.e if the user does not specify the target IP Address
    # Quit the program if the argument is missing
    # While quitting also display an error message
    if not options.target:
        # Code to handle if interface is not specified
        parser.error(
            "[-] Please specify an IP Address or Addresses, use --help for more info.")
    return options


class Manager():
    def __init__(self) -> None:
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

    def send_scanner(self, ip):
        print('Mock, scanner send to ', ip)
        # Sends scanner file to target to initiate scan
        # TODO: GET FROM SAPIR
        return True

    def run_scanner(self, ip):
        print('Mock, scanner run on ', ip)
        # Sends scanner file to target to initiate scan
        # TODO: GET FROM SAPIR
        return True

    def scan_host(self, ip):
        status = False
        if self.send_scanner(ip):
            status = self.run_scanner(ip)
        return status

    # Thread started for each connection made to our socket
    def handle_scanner_response(self, conn, addr):
        # TODO: Wrap in try except
        # TODO: Create handshake
        data = conn.recv(1024)
        if data == HANDSHAKE_SYN:
            conn.send(HANDSHAKE_SYNACK.encode('utf-8'))
            data = conn.recv(1024)
            if data == HANDSHAKE_ACK:
                print('Handshake done successfully')
            else:
                print('Wrong SynAck!')
                conn.close()
                exit()
        else:
            print('Wrong Syn!')
            conn.close()
            exit()

        # Get the new hosts found
        # TODO: Verify getting all the data
        data = conn.recv(1024)

        # Parse response
        response = self.parse_response(data)
        # Write to global variable? the new nodes to scan
        # TODO: manage multi layer scan? should the node scan it by itslef
        # Write data to db
        self.write_to_db(response)
        pass

    def parse_response(self, response):
        # Parse response
        pass

    def write_to_db(self, data):
        # Enter node and relations to db
        pass


def main():

    init()
    # Start the scan by scanning localhost
    scan_host('127.0.0.1')
    scanned_hosts.append('127.0.0.1')

    # TODO: Start thread for failure hosts to try every once in a while. After X unsuccessful tries add to scanned

    # always go over new hosts
    while(True):
        # TODO: Verify this ain't a problem, that new_hosts keep chainging and we are in foreach
        for host in new_hosts:
            # Verify host has not been scanned and scan it
            if host not in scanned_hosts:
                if scan_host(host):
                    scanned_hosts.append(host)
                else:
                    failure_hosts.append(host)
            new_hosts.remove(host)


# options = get_args()
# scanned_output = scan(options.target)
# print(netifaces.interfaces())
# interfaces = netifaces.interfaces()
# for interf in interfaces:
#     scanned_output = arp_scan('192.168.1.0/24', interf)
#     display_result(scanned_output)
