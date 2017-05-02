#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "./parse_apache.sh <source file>"
    exit 1;
fi
N=0
while read -r line || [[ -n "$line" ]]; do

    #   wget -q --no-cache $ip_addr$fcgi_string
    newline=$(echo $line |
	sed 's/^http:\/\/.*\/fcgi/http:\/\/localhost\/fcgi/') 
    curl -s $newline > /dev/null
done < "$1"
   
