from unicodedata import name
import scapy.all as scapy
import argparse
import netifaces as ni
import socket
import threading
import pickle
import neo
from re import findall
from uuid import getnode
import platform
# TODO: Remove unneeded imports

# List of new hosts to scan
new_hosts = []
# List of hosts already scanned, so that we wont scan them twice
scanned_hosts = {}
# List of hosts failed to scan, maybe they were down
failure_hosts = []

BIND_ADDR = ('0.0.0.0', 9000)
# HANDSHAKE_SYN = 'hola'
# HANDSHAKE_SYNACK = 'bola'
# HANDSHAKE_ACK = 'holabolaa'


class Host():
    def __init__(self, ip, mac=None, os=None) -> None:
        self.ip = ip
        self.mac = mac
        self.os = os


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', dest='target',
                        help='Target IP Address/Addresses')
    options = parser.parse_args()

    # Quit the program if the argument is missing
    if not options.target:
        parser.error(
            "[-] Please specify an IP Address or Addresses, use --help for more info.")  # TODO: Rewrite
    return options


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


class BaseManager():
    def __init__(self) -> None:
        # Set up connection to the db
        self.net = neo.Network()
        mac = ':'.join(findall('..', '%012x' % getnode()))
        ips = get_local_ips()
        self.net.create_host(ips, mac, platform.system().lower())
        # Start comunication sockets
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(BIND_ADDR)
        # TODO: Verify best number, so that we wont lose connections
        s.listen(100)
        t_hi = threading.Thread(target=self.handle_inputs, args=(s,))
        t_hi.run()

    def handle_inputs(self, s):
        while True:
            conn, addr = s.accept()
            print(addr[0] + " connected")
            t_sr = threading.Thread(target=self.handle_scanner_response, args=(
                conn, addr))  # TODO: Verify syntax is correct
            t_sr.start()

    # Thread started for each connection made to our socket
    def handle_scanner_response(self, conn, addr):
        # TODO: Wrap in try except
        # TODO: Create handshake
        # TODO: Verify getting all the data
        #data = conn.recv(1024)
        data = b''
        while True:
            print('before')
            packet = conn.recv(4096)
            print('after')

            if not packet:
                break
            data += packet
        if not data:
            print('data problem')
            exit()
        # Get the new hosts found
        # Parse response
        response = self.parse_response(data)
        if response and response != {}:
            # Write to global variable? the new nodes to scan
            print('sending to db')
            self.write_to_db(response)

    def parse_response(self, response):
        # TODO: Use pickle safely
        parsed_res = pickle.loads(response)
        # TODO: Understand how writing to db works and match to it
        print(parsed_res)
        for host in list(parsed_res['hosts'].keys()):
            if host in scanned_hosts:
                print('Exists')
                # TODO: Maybe check if there is more info
                del parsed_res['hosts'][host]
            else:
                scanned_hosts[host] = parsed_res['hosts'][host]
        return parsed_res

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

    def write_to_db(self, data):
        # Enter node and relations to db
        # TODO: Handle multi thread writing( because it is done on thread)
        print('wrote to db:')
        self.net.create_query(data)
        self.net.conn_query(data)
        #print('wrote to db:', data)
        pass


def main():
    #options = get_args()
    target = '127.0.0.1'
    base = BaseManager()
    # base.scan_host(options.target)
    base.scan_host(target)


main()
