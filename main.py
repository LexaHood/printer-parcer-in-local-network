import socket
import threading
import time
import subprocess

start_time = time.time()

mac_printer_list = ['3c:2a:f4', '00:17:c8', 'f4-30-b9'] #brother, koycera, hp
length_mac_lsit = len(mac_printer_list)
list_printers = []

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

    pass

def delimiter_mac_address (ip_adress):
    result = subprocess.run(['arp', ip_adress], stdout=subprocess.PIPE)
    tmp = result.stdout.decode('utf-8')
    #print (tmp)
    index_first = tmp.find("ether") + 8
    index_last = tmp.find(" ", index_first)
    #print ("index first = ", index_first, "\tindex_last = ", index_last)
    #print (tmp[index_first:index_last])
    return (tmp[index_first:index_last])

def check_mac (mac_adress):
    for i in range (length_mac_lsit):
        tmp = mac_adress[0 : 8]
        if tmp.find(mac_printer_list[i]) != -1:
            return True
    pass
    return False

def main ():

    ip = '10.1.1.'

    def thread_function(adress):
        mac_adress = delimiter_mac_address(ip + str(adress))
        res = check_mac(mac_adress)
        if res == True:
            list_printers.append(net_packege(ip + str(adress), mac_adress))
        
        

    for adress in range (1, 255, 1):

        thread_function(adress)
        #potoc = threading.Thread(target=thread_function, args=(adress))
        #potoc.start()
        pass

    size = len(list_printers)
    print (size)
    if size != 0:
        for i in range (size):
            list_printers[i].print_packege()
            pass
        pass
    else: 
        print ("printers not founded")

main()