import threading
import time
import subprocess
from threading import Thread
import packege_class

start_time = time.time() #запомниаем когда запустилась программа

mac_printer_list = [ #Список мак адресов производителей принтеров
'3c:2a:f4', #Brother
'00:17:c8', #Koycera
'f4:30:b9'] #HP

length_mac_lsit = len(mac_printer_list) #узнаем колличесво мак адресов производителей
list_printers = [] #создаем лист под найденные адреса принтеров в сети

def delimiter_mac_address (ip_adress): #эта функция делает арп по айпишнику и выделяет мак адрес из выода консоли
    result = subprocess.run(['arp', ip_adress], stdout=subprocess.PIPE) #записываем результат из терминала
    tmp = result.stdout.decode('utf-8') #для полной уверенности переведем строчку в юникод 
    index_first = tmp.find("ether") + 8 #ищем где же начинается мак адрес
    index_last = tmp.find(" ", index_first) #ищем где заканчивается 
    return (tmp[index_first:index_last]) 

def check_mac (mac_adress): #проверяем, полученный мак адрес это принтер
    for i in range (length_mac_lsit):
        tmp = mac_adress[0 : 8]
        if tmp.find(mac_printer_list[i]) != -1: #если в получаном адресе есть код указанного производителя вернуть правду
            return True
    pass
    return False

def main ():

    ip = '10.1.1.'

    file = open("printer list.conf", "w", 1 , "UTF-8") #открываем файл для записи

    def thread_function(start_adress, end_adress): #основная функция всей обработки, скомпонована для более простым управлением потока
        for adress in range (start_adress, end_adress, 1):
            print ('check ip: ', ip, adress)
            mac_adress = delimiter_mac_address(ip + str(adress)) #получаем мак по заданному ip
            res = check_mac(mac_adress) #проверяем принадлежит ли мак адрес нужному производителю
            if res == True:
                list_printers.append(packege_class.net_packege(ip + str(adress), mac_adress)) #записываем айпи и мак адрес принтера в массив
            pass
        pass
    
    def thread_launcher(): #Запускаем и останавливаем потоки
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
    #print (size)
    if size != 0:
        for i in range (size): #записываем все найденные принтеры в файл
            list_printers[i].print_packege()
            file.writelines(list_printers[i].get_string_to_write() + '\n')
            pass
        pass
    else: 
        print ("printers not founded") #если list_printers пустой, значит мы ничего не нашли
        print ("printers either are not present in the local network, or the poppy address is not entered in the search base")


    file.close()
    pass

main()
print("--- %s second ---" % (time.time() - start_time)) #выводим время за которое выполнилась программа