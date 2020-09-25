

class net_packege (object):

    def __init__(self, ip = None, mac = None):
        if ip != None: self.ip = ip
        else: self.ip = '127.0.0.1'
        if mac != None: self.mac = mac
        else: self.mac = '00:00:00:00:00:00'

    def add_ip (self, ip):
        self.ip = ip

    def add_mac (self, mac):
        self.mac = mac

    def get_ip (self):
        return self.ip

    def get_mac (self):
        return self.mac

    def print_packege (self):
        print ('ip adress: ', self.ip, '\tmac: ', self.mac)

    def get_string_to_write (self):
        return ('ip adress: ' + self.ip + '\tmac: ' + self.mac)

    pass