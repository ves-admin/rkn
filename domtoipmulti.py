#!/usr/bin/env python3
# Скрипт асинхронного преобразования доменых имен в IP 
import argparse

parser = argparse.ArgumentParser(add_help=True, description='Parser for dump.xml')

parser.add_argument("-if", "--ipfile", action="store", default='ip_file',
        required=False, type=str, help="full path to the file IP")

parser.add_argument("-df", "--domfile", action="store", default='dom_file',
        required=False, type=str, help="full path to the file HOSTS")

args = parser.parse_args()


def domtoip(DOM_FILE='dom_file', IP_FILE='ip_file'):

    import gevent
    from gevent import monkey; monkey.patch_all()
    import re
    import socket
    from urllib.parse import urlparse

    print('Read file:', DOM_FILE)
    df = open(DOM_FILE, 'rt')
    tmp1 = df.readlines()
    df.close()
    tmp2 = set()
    count = 0
    warn = 0
    url = re.compile(r'^([а-яёa-z0-9]([а-яёa-z0-9\-]{0,61}[а-яёa-z0-9])?\.)+[а-яёa-z0-9]{2,6}$')
    while count < len(tmp1):
        if url.match(tmp1[count]):
            tmp2.update(tmp1[count].split('\n'))
            #print(url.group())
        else:
            warn += 1
            count += 1
            continue
        count += 1
    hosts = list(tmp2)
    print('Entries counter error:', warn)
    print('Counter unique hosts:', len(hosts))
    print('===< Run hosttoip() >===')
    ip = set()
    count = 0
    noneip = 0
    while True:
        if count >= len(hosts):
            break    
        elif (len(hosts) - count) < 1000:
            host = hosts[count:]
            count = len(hosts)
        else:        
            host = hosts[count:count+1000]
            count += 1001  
        jobs = [gevent.spawn(socket.gethostbyname, url) for url in host]
        gevent.joinall(jobs, timeout=60) #, timeout=60
        for job in jobs:
            if job.value != None:
                ip.update([job.value])
            else:
                noneip += 1  
    print('Counter unique IP:', len(ip))
    print("URL's no IP:", noneip)
    ipstr = '\n'.join(ip)
    ipfiles = open(IP_FILE, 'ab')
    ipfiles.write(ipstr.encode('utf-8'))
    ipfiles.close()

if __name__ == "__main__":
    domtoip()

