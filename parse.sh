#!/bin/bash
#set -x

if [ "$#" -ne 1 ]; then
    echo "./parse_apache.sh <log file>"
    exit 1;
fi
N=0
while read -r line || [[ -n "$line" ]]; do

    if echo $line | grep -q "GET /fcgi-bin/iipsrv.fcgi?DeepZoom"; then
	if echo $line | grep -q "http"; then
#            echo "Accept: $line"
	    if echo $line | grep -v -q "dzi HTTP"; then
		fcgi_string=$(echo $line |
		    sed 's/^.*GET \/fcgi-bin/\/fcgi-bin/'|
		    sed 's/jpg.*$/jpg/'
		)
		ip_addr=$(echo $line |
		    sed 's/^.*http/http/' |
		    sed 's/\/camicroscope.*$//'
		)
		echo $ip_addr$fcgi_string
	    fi
        fi
    fi
done < "$1"

