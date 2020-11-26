import sys
import os
import time              
from datetime import datetime


def remaining_seconds(hour,minutes):
    now = datetime.now()

    current_hour = now.hour
    current_minute = now.minute
    current_second = now.second

    remaining_sec = hour*3600 + minute*60 - current_hour*3600 - current_minute*60 - current_second
    return remaining_sec

if __name__ == '__main__':
    hour, minute = sys.argv[1:]

    hour = int(hour)
    minute = int(minute)
    
    while(remaining_seconds(hour,minute) > 0):
        print("El programa empezará en: ", remaining_seconds(hour,minute), " seconds")
        time.sleep(1)

    print("Empezando captura de paquetes cada 15 segundos")
    os.system("sudo tcpdump -w /tmp/captura-%H-%M-%S.pcap  -G 15 -C 200")
    


