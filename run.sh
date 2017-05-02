#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "./parse_apache.sh <source file> <server IP addr>"
    exit 1;
fi
N=0
while read -r line || [[ -n "$line" ]]; do

    #   wget -q --no-cache $ip_addr$fcgi_string
    newline=$(echo $line |
	sed 's/^http:\/\/.*\/fcgi/http:\/\/'$2'\/fcgi/') 
    curl -s $newline > /dev/null
done < "$1"
   
