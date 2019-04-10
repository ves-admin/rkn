#!/usr/bin/env bash

req='request.xml'
sig='request.bin'
iptmp='ip_tmp'
ipfile='ip_file'
urlfile='url_file'
domain='dom_file'
./download.py -r ${req} -s ${sig}
./parser.py -if ${ipfile}  -uf ${urlfile} -df ${domain}
echo -e ${domaine} >> ${urlfile}
cat ${urlfile} | grep 'https:' | sed 's|.*://||' | sed -e 's/\/.*//g' | sort | uniq >> ${domain}
./domtoip.py -if ${ipfile} -df ${domain}
for ip in $(cat ${ipfile})
do
echo -e "-q table 33 add $ip" > ${iptmp}
done
#for i in $( cat ${domain} ); do
#for ip in $( /usr/bin/host -t A ${i} 127.0.1.1 | /bin/grep "has address" | /usr/bin/awk '{ print $4 }')
#do
#echo -e ${ip} >> ${iptmp}
#done
#done
#cat ${iptmp} | sort | uniq > ${ipfile}
