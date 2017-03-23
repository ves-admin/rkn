#!/usr/bin/env python3
# Скрипт для последовательного преобразование доменных имен в IP

import argparse

#Парсинг аргументов командной строки
parser = argparse.ArgumentParser(add_help=True, description='Parser for dump.xml') 

parser.add_argument("-if", "--ipfile", action="store", default='ip_file',
        required=False, type=str, help="full path to the file IP")

parser.add_argument("-df", "--domfile", action="store", default='dom_file',
        required=False, type=str, help="full path to the file HOSTS")

args = parser.parse_args()


def domtoip(DOM_FILE, IP_FILE):

    import gevent
    from gevent import monkey; monkey.patch_all()
    import re
    import socket

    print('Read file:', DOM_FILE)
    df = open(DOM_FILE, 'rt')
    tmp1 = df.readlines()
    tmp2 = set()
    count = 0
    warn = 0
    df.close()
    #Регулярное выражение для выделения URL
    url = re.compile(r'^([а-яёa-z0-9]([а-яёa-z0-9\-]{0,61}[а-яёa-z0-9])?\.)+[а-яёa-z0-9]{2,6}$')
    while count < len(tmp1):
        if url.match(tmp1[count]):
            tmp2.update(tmp1[count].split('\n'))
        else:
            warn += 1
            count += 1
            continue
        count += 1
    #Переменная list() содержащая доменные имена
    hosts = list(tmp2)
    print('Entries counter error:', warn)
    print('Counter unique hosts:', len(hosts))
    print('===< Run hosttoip() >===')
    #Переменная set() для уникальных ip адресов
    ip = set()
    noneip = 0   
    count = 0
    jobs = []
    while count < len(hosts):
        try:
            if socket.gethostbyname(hosts[count]):
                '''В этой строке происходит преобразование HOST -> URL
                ip c помощью метода update "запоминает" ip если он еще не
                встречался'''
                ip.update([socket.gethostbyname(hosts[count])])
        except socket.gaierror:
            noneip += 1
        count += 1
    print('Counter unique IP:', len(ip))
    print("URL's no IP:", noneip)
    ipstr = '\n'.join(ip)
    ipfiles = open(IP_FILE, 'ab')
    ipfiles.write(ipstr.encode('utf-8'))
    ipfiles.close()

domtoip(args.domfile, args.ipfile)
