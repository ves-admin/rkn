#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(add_help=True, description='Parser for dump.xml')

parser.add_argument("-if", "--ipfile", action="store", default='ip_file',
        required=False, type=str, help="full path to the file IP")

parser.add_argument("-uf", "--domfile", action="store", default='url_file',
        required=False, type=str, help="full path to the file URL's")

parser.add_argument("-t", "--type", action="store", default=None,
        required=False, type=str, help="HTTP or HTTPS, default ALL")

args = parser.parse_args()


def urltoip(URL_FILE, IP_FILE, TYPE):

    import gevent
    from gevent import monkey; monkey.patch_all()
    import re
    import socket
    from urllib.parse import urlparse
    

    print('Read file:', URL_FILE)
    df = open(URL_FILE, 'rt')
    tmp1 = df.readlines()
    df.close()
    tmp2 = set()
    count = 0
    warn = 0
    while True:
        if count < len(tmp1):
            url = urlparse(tmp1[count])
            if (url.scheme == TYPE or TYPE == None) and url.hostname:            
                url = url.hostname
                tmp2.update(url.split('\n'))
            else:
                warn += 1
        else:
            break
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

urltoip(args.domfile, args.ipfile, args.type)
