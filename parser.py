#!/usr/bin/env python3


import argparse
import os

parser = argparse.ArgumentParser(add_help=True, description='Parser for dump.xml')

parser.add_argument("-d", "--dump", action="store", default='dump.xml',
        required=False, type=str, help="full path to dump.xml file")

parser.add_argument("-if", "--ipfile", action="store", default='ip_file',
        required=False, type=str, help="full path to output file for IP")

parser.add_argument("-uf", "--urlfile", action="store", default='url_file',
        required=False, type=str, help="full path to output file for URL")

parser.add_argument("-df", "--domfile", action="store", default='dom_file',
        required=False, type=str, help="full path to output file for DOMAIN")


args = parser.parse_args()


def dump(DUMP_FILE_NAME, IP_FILE, URL_FILE, DOM_FILE):
    
    import xml.etree.ElementTree as ET 

    tree = ET.parse(DUMP_FILE_NAME)
    root = tree.getroot()
    
    url = set()
    ip = set()
    dom = set()
    
    for data in root.iter('url'):
        url.update([data.text])
    for data in root.iter('ip'):
        ip.update([data.text])
    for data in root.iter('domain'):
        dom.update([data.text])
    
    urlstr = '\n'.join(url)
    ipstr = '\n'.join(ip)
    domstr = '\n'.join(dom)
    
    print('Путь к файлу:', os.path.abspath(DUMP_FILE_NAME))
    print('Колличество URL:', len(url))
    print('Колличество IP:', len(ip))
    print('Колличество DOMAIN:', len(dom))
    print('Общеее колличество записей:', len(url | ip | dom))

    ipfiles = open(IP_FILE, 'wb')
    ipfiles.write(ipstr.encode('utf-8'))
    ipfiles.close()
    
    urlfiles = open(URL_FILE, 'wb')
    urlfiles.write(urlstr.encode('utf-8'))
    urlfiles.close()
    
    domfiles = open(DOM_FILE, 'wb')
    domfiles.write(domstr.encode('utf-8'))
    domfiles.close()
    
dump(args.dump, args.ipfile, args.urlfile, args.domfile)

