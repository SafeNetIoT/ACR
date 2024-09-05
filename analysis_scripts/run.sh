#!/bin/bash

pcap=$1
csv_file=$2
device_ip=$3
#device_ip2=$4

./extract_csv_from_pcap.sh $pcap $csv_file
python3 refine_csv.py $csv_file $device_ip # $device_ip2
