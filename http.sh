#!/usr/bin/env bash
iptmp='ip_tmp'
ipfile='ip_file'
urlfile='url_file'
domain='dom_file'
./parser.py -if ${ipfile}  -uf ${urlfile} -df ${domain}
echo -e ${domaine} >> ${urlfile}
cat ${urlfile} | grep 'https:' | sed 's|.*://||' | sed -e 's/\/.*//g' | sort | uniq >> ${domain}
./domtoip.py -if ${ipfile} -df ${domain}
for ip in $(cat ${ipfile})
do
echo -e "-q table 33 add $ip" > ${iptmp}
done
