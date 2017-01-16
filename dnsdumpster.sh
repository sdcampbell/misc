#!/bin/bash

echo -n "Enter a domain name and press [ENTER]: "
read domain

# Generate a random cookie value
rando=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)

curl --silent --header "Host:dnsdumpster.com" --referer https://dnsdumpster.com --user-agent "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0" --data "csrfmiddlewaretoken=$rando&targetip=$domain" --cookie "csrftoken=$rando; _ga=GA1.2.1737013576.1458811829; _gat=1" https://dnsdumpster.com > tmp

dumpsterxls=$(grep 'xls' tmp | tr '"' ' ' | cut -d ' ' -f10)

wget -q $dumpsterxls -O $domain.xlsx

ssconvert -E Gnumeric_Excel:xlsx -T Gnumeric_stf:stf_csv $domain.xlsx $domain.csv 2>/dev/null

cat $domain.csv | sed 's/,"//g' | egrep -v '(Hostname|MX|NS)' | cut -d ',' -f1-2 | grep -v '"' | sed 's/,/ /g' | sort -u | column -t > $domain.txt

wget -q https://dnsdumpster.com/static/map/$domain.png -O $domain.png

rm tmp

echo "Saving files $domain.xlsx, $domain.csv, $domain.txt, and $domain.png to current working directory."



