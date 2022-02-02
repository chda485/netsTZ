import socket, requests
import threading
from multiprocessing import Process

#IP = '192.168.0.0/24'
#PORTS = [21, 22, 25, 80, 443]

def scan_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    try:
        connect = sock.connect((ip, port))      
        if port == 80 or port == 443:
            result = requests.get('http://{}:{}/'.format(ip, port))
            if result.status_code == 200:
                domain_url = result.text.split(
                    '</html>')[1].split(
                        'url="')[1].split(
                            ';')[0][:-1]
                result = requests.head(domain_url)
                if result.status_code != 405:
                    if 'Server' in result.headers:
                        print("{} {} {}, server - {}".format(ip, port, ' OPEN',
                                                              result.headers['Server']))
                        return
                    
        print('{} {} {}'.format(ip, port,' OPEN'))
        sock.close()
    except:
        pass

if __name__ == "__main__":
    while True:
        IP = input("Введите IP или q для выхода: ")
        if IP == 'q':
            break
        PORTS = input("Введите список портов через запятую или q для выхода: ")
        if PORTS == 'q':
            break
        start = int(IP.split('/')[0].split('.')[-1])
        end = int(IP.split('/')[1])
        for i in range(start, end+1):
            IP = IP.split('/')[0]
            length = len(IP.split('.')[-1])
            ip = IP[:-length]+str(i)
            for p in PORTS.split(','):
                potoc = Process(target=scan_port, args=(ip, int(
                    p.replace(' ', ''))))
                potoc.start()
                potoc.join()


