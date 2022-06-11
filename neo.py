from neo4j import GraphDatabase

######################################################################################


class Host:
    def __init__(self, ip, mac=None, os=None) -> None:
        self.ip = ip
        self.mac = mac
        self.os = os


class Network:
    def __init__(self, uri=None, user=None, pasw=None):
        if not uri:
            uri = "bolt://localhost:7687"
        if not user:
            user = "neo4j"
        if not pasw:
            pasw = "Aa123456"
        self.driver = GraphDatabase.driver(uri, auth=(user, pasw))
        self.session = self.driver.session()
        # Delete all from previous scan
        self.session.run("MATCH (n) DETACH DELETE n")

    def close(self):
        self.session.close()
        self.driver.close()

    def check_host(self, mac):
        check_host = self.session.run(
            "match (n) where n.mac=$mac return n", mac=mac)
        sig = check_host.single()
        if(sig):
            return True
        else:
            return False

    def create_host(self, ip, mac, os=None):
        check = self.check_host(mac)
        if(check == True):
            find_ip = self.session.run(
                "MATCH (n) WHERE n.mac=$mac RETURN n.ip as ips", mac=mac)
            cur_ips = [record["ips"] for record in find_ip]
            new_ips = cur_ips[0]
            if(ip in new_ips):
                return 0
            new_ips.append(ip)
            set_ip = self.session.run(
                "MATCH (n) WHERE n.mac=$mac SET n.ip = $ips", mac=mac, ips=new_ips)
        if(check == False):
            if type(ip) != list:
                temp_arr = []
                temp_arr.append(ip)
            else:
                temp_arr = ip
            self.session.run("CREATE (Host {ip: $ip, os: $os, mac: $mac})",
                             ip=temp_arr, os=os, mac=mac)

    def check_conn(self, ips, Host):
        mac = self.find_mac(ips)
        check_conn = self.session.run(
            "MATCH (n {mac: $ips_mac})-->(h) where h.mac=$host_mac RETURN h.mac as mac", ips_mac=mac, host_mac=Host.mac)
        sig = check_conn.single()
        if(sig):
            return True
        else:
            return False

    def find_mac(self, ips):
        for ip in ips:
            match = self.session.run(
                "MATCH (n) WHERE $ip in n.ip RETURN n.mac as mac", ip=ip)
            sig = match.single()
            if(sig):
                mac = sig["mac"]
                return mac
        return ""  # TODO: Handle

    def create_conn(self, ips, Host):
        check = self.check_conn(ips, Host)
        if(check):
            print("connection already exists")
        else:
            mac = self.find_mac(ips)
            if mac:
                self.session.run("MATCH (n),(h) WHERE n.mac=$mac AND h.mac=$host_mac CREATE (n)-[r:Connected]->(h)",
                                 mac=mac, host_mac=Host.mac)

    def create_query(self, the_dict):
        for h in the_dict['hosts'].values():
            ip1 = h.ip
            os1 = h.os
            mac1 = h.mac
            self.create_host(ip1, mac1, os1)

    def conn_query(self, the_dict):
        ips = the_dict['ips']
        for h in the_dict['hosts'].values():
            self.create_conn(ips, h)


######################################################################################
# h1 = Host(ip='192.168.1.10', mac="ccc", os="windows")
# h2 = Host(ip='192.168.1.14', mac="ddd", os="linux")
# h3 = Host(ip='192.168.1.42', mac="fff", os="linux")
# ips = ['192.168.1.42', '192.168.202.1', '127.0.0.1']
# hosts = {}
# hosts['192.168.1.10'] = h1
# hosts['192.168.1.14'] = h2
# hosts['192.168.1.42'] = h3
# d = {}
# d['ips'] = ips
# d['hosts'] = hosts
# net = Network()
# net.create_query(d)
# net.conn_query(d)
