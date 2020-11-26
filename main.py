
from scapy.all import  rdpcap
from scapy.all import  scapy, RawPcapNgReader
import csv
import os
from upload_data import *
import time
from datetime import datetime
import sys
from emailer import *

#label 1: HTTP, 2:SMTP, 3:STREAM
def resume_pkts(pkts_list, label, ip):
    
    # filtrar paquetes

    filter_pkts = []
    ip = ip.split(".")[:-1]
    ip = ".".join(ip)

    for pkt in pkts_list:
        try:
            if (pkt['IP'].src.startswith(ip)  or pkt['IP'].dst.startswith(ip)):
                filter_pkts.append(pkt)
        except:
            continue

    result = {}
    
    if (len(filter_pkts) == 0):
        return

    pk1 = filter_pkts[0]
    srcip = pk1['IP'].src
    srcport = pk1['TCP'].sport
    dstip = pk1['IP'].dst
    dstport = pk1['TCP'].dport
    proto = pk1['IP'].proto 

    result['srcip'] = srcip
    result['srcport'] = srcport
    result['dstip'] = dstip
    result['dstport'] = dstport
    result['proto'] = proto

    t_srcip = srcip.split(".")[:-1]
    t_srcip = ".".join(srcip)

    

    # fordward packets
    total_fpackets = 0
    total_bpacket = 0
    total_fvolume = 0
    total_bvolume = 0
    for pkt in filter_pkts:
        if (pkt['IP'].dst.startswith(ip)):
            total_fpackets += 1
            total_fvolume += len(pkt)
        if (pkt['IP'].src.startswith(ip)):
            total_bpacket += 1
            total_bvolume += len(pkt)
    
    result['total_fpackets'] = total_fpackets
    result['total_bpackets'] = total_bpacket
    result['total_fvolume'] = total_fvolume
    result['total_bvolume'] = total_bvolume

    result['label'] = label

    return result


def write_data(pkt_resume):    
    values = [pkt_resume['srcip'],pkt_resume['srcport'],pkt_resume['dstip'],
    pkt_resume['dstport'],pkt_resume['proto'],pkt_resume['total_fpackets'],pkt_resume['total_bpackets'] ,
    pkt_resume['total_fvolume'],pkt_resume['total_bvolume'] , pkt_resume['label']  ]
    add_record(values)
    print("Record Uploaded")

def get_pcaps(directorio):
    list_d = os.listdir(directorio)
    pcap = []

    for f in list_d:
        if os.path.isfile(os.path.join(directorio,f)) and f.endswith('.pcap'):
            pcap.append(f)
    return pcap

def rm_pcaps(directorio):
    pcap = get_pcaps(directorio)
    for f in pcap:
        os.system("sudo rm "+ directorio +f )

def generateHTTP():
    f = open("/home/daniel/Documents/Utec/7to ciclo/Redes y Comunicaciones/Proyecto/scripts/page_ip.txt", 'r')
    
  
    for linea in f:
        url = linea.strip("\n").split(" ")[0]
        ip = linea.strip("\n").split(" ")[1]

        command = "wget -O index.html -T 4 " + url
        os.system(command)
        
        pcap = get_pcaps("/tmp/")
        

        #solo para el primer paquete
        while (len(pcap) < 2):
            time.sleep(1)
            pcap = get_pcaps('/tmp/')
        
        max_pkt = min(pcap)

        print("Nuevo paquete: ", max_pkt)

        pkts_list =  rdpcap("/tmp/" + max_pkt)
       
        try:
            resume = resume_pkts(pkts_list,1, ip)
            write_data(resume)
        except:
            pass
        os.system("sudo rm "+ "/tmp/" +max_pkt )

        # esperar a que halla un paquete mas

def remaining_seconds(hour,minutes):
    now = datetime.now()

    current_hour = now.hour
    current_minute = now.minute
    current_second = now.second

    remaining_sec = hour*3600 + minute*60 - current_hour*3600 - current_minute*60 - current_second
    return remaining_sec

def generateSMTP():
    for i in range(100):
        sendRandomEmail()

        pcap = get_pcaps("/tmp/")
        while (len(pcap) < 2):
            time.sleep(1)
            pcap = get_pcaps('/tmp/')
        
        min_pkt = min(pcap)
        print("Nuevo paquete: ", min_pkt)
        pkts_list =  rdpcap("/tmp/" + min_pkt)
        
        try:
            resume = resume_pkts(pkts_list,2, "64.233.186.109")
            write_data(resume)
        except:
            pass

        os.system("sudo rm "+ "/tmp/" +min_pkt )

if __name__ == '__main__':
    rm_pcaps('/tmp/')
    hour, minute = sys.argv[1:]

    hour = int(hour)
    minute = int(minute)
    
    while(remaining_seconds(hour,minute) > 0):
        print("El programa empezará en: ", remaining_seconds(hour,minute), " seconds")
        time.sleep(1)
    print("Empezando a generar trafico...")
    time.sleep(2)
    #generateHTTP()
    generateSMTP()

 

