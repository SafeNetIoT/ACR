#!/bin/bash

pcap=$1
csv_file=$2


tshark -r $pcap -Y "ip and not ipv6" -T fields -e frame.number -e frame.time_epoch -e frame.len -e frame.protocols -e eth.src -e eth.dst -e ip.src -e ip.dst -e ip.proto -e ip.len -e ip.id -e tcp.srcport -e tcp.dstport -e udp.srcport -e udp.dstport -e tcp.flags -e dns.qry.name -e dns.resp.name -e dns.a -e http.request.method -E header=n -E separator=, -E quote=d -E occurrence=f > $csv_file
