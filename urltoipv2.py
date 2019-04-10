#!/usr/bin/env python3


def host_to_ip(host):
    import socket
    try:
        if socket.gethostbyname(host) != None:
            return socket.gethostbyname(host)
    except:
        print('IP not found: %s' %host)
        return '255.255.255.255'

#    ip = set()
#    try:
#        if socket.gethostbyname(host):
#            ip.update([socket.gethostbyname(host)])
#    except socket.gaierror:
#        print('IP not found: %s' %host)
#    return ' '.join(ip)

hosts = []
with open('dom_file', 'r') as f:
    for host in f.readlines():
        host = host.strip('*.')
        hosts.append(host_to_ip(host.strip('\n')))

ipstr = '\n'.join(hosts)

with open('ip_file', 'wb') as f:
    f.write(ipstr.encode('utf-8'))
    
#for host in hosts:
#    ip = host_to_ip(host.split('/n'))



#if __name__ == '__main__':
#    multi(hosts)

    

