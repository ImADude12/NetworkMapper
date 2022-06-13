import argparse
import netifaces as ni
import socket
import threading
import pickle
import neo
from re import findall
from uuid import getnode
import platform
import json
import subprocess
import sys
import os
# TODO: Remove unneeded imports
ips = []
# List of new hosts to scan
new_hosts = []
# List of hosts already scanned, so that we wont scan them twice
scanned_hosts = {}
# List of hosts failed to scan, maybe they were down
failure_hosts = []

BIND_ADDR = ('0.0.0.0', 9000)
with open('log.txt', 'w') as f:
    f.write('')


def print2(text):
    with open('log.txt', 'a') as f:
        f.write(text + "\n")
        print(text)


# if len(sys.argv) > 1:
#     creds = json.loads(sys.argv[1])
#     print(''.join(creds))


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
            print2(ip)
        except KeyError:
            print2(f'badface {face}')
    if '127.0.0.1' in local_ips:
        local_ips.remove('127.0.0.1')
    print2(''.join(local_ips))
    return local_ips


class BaseManager():
    def __init__(self) -> None:
        global ips
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
        t_hi.start()

    def handle_inputs(self, s):
        while True:
            conn, addr = s.accept()
            print2(addr[0] + " connected")
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
            print2('before')
            packet = conn.recv(4096)
            print2('after')

            if not packet:
                break
            data += packet
        if not data:
            print2('data problem')
            exit()
        # Get the new hosts found
        # Parse response
        response = self.parse_response(data)
        if response and response != {}:
            # Write to global variable? the new nodes to scan
            print2('sending to db')
            self.write_to_db(response)

    def parse_response(self, response):
        # TODO: Use pickle safely
        parsed_res = pickle.loads(response)
        # TODO: Understand how writing to db works and match to it
        print(parsed_res)
        print2('got res')
        for host in list(parsed_res['hosts'].keys()):
            if host in scanned_hosts:
                print2('Exists')
                # TODO: Maybe check if there is more info
                del parsed_res['hosts'][host]
            else:
                scanned_hosts[host] = parsed_res['hosts'][host]
        return parsed_res

    def scan_host(self):
        proc = subprocess.Popen(['python', 'networkscanner.py'] + ips + ['9000'], cwd=r'C:\Users\matan\Desktop\NetworkMapper\web\backend',
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out, err = proc.communicate()
        print(out, err)
        print(os.getcwd())

        return 1

    def write_to_db(self, data):
        # Enter node and relations to db
        # TODO: Handle multi thread writing( because it is done on thread)
        print2('wrote to db:')
        self.net.create_query(data)
        self.net.conn_query(data)
        #print2('wrote to db:', data)
        pass


def main():
    #options = get_args()
    target = '127.0.0.1'
    base = BaseManager()
    # base.scan_host(options.target)
    base.scan_host()


main()
