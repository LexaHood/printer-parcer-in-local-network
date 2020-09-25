import socket
import threading
import time
import subprocess
from threading import Thread
import packege_class

start_time = time.time()

mac_printer_list = [
'3c:2a:f4', #Brother
'00:17:c8', #Koycera
'f4:30:b9'] #HP

length_mac_lsit = len(mac_printer_list)
list_printers = []

def delimiter_mac_address (ip_adress):
    result = subprocess.run(['arp', ip_adress], stdout=subprocess.PIPE)
    tmp = result.stdout.decode('utf-8')
    index_first = tmp.find("ether") + 8
    index_last = tmp.find(" ", index_first)
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

    file = open("printer list.conf", "w", 1 , "UTF-8")

    def thread_function(start_adress, end_adress):  
        for adress in range (start_adress, end_adress, 1):
            print ('check ip: ', ip, adress)
            mac_adress = delimiter_mac_address(ip + str(adress))
            res = check_mac(mac_adress)
            if res == True:
                list_printers.append(packege_class.net_packege(ip + str(adress), mac_adress))
            pass
        pass
    
    def thread_launcher():
        thread1 = Thread(target=thread_function, args=(1, 64))
        thread2 = Thread(target=thread_function, args=(64, 128))
        thread3 = Thread(target=thread_function, args=(128, 192))
        thread4 = Thread(target=thread_function, args=(192, 254))

        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()

        thread1.join()
        thread2.join()
        thread3.join()
        thread4.join()
        pass

    thread_launcher()

    size = len(list_printers)
    print (size)
    if size != 0:
        for i in range (size):
            list_printers[i].print_packege()
            file.write(list_printers[i].get_string_to_write)
            pass
        pass
    else: 
        print ("printers not founded")


    file.close()
    pass

main()
print("--- %s second ---" % (time.time() - start_time))