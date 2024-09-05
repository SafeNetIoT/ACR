#!/bin/bash

pcap_folder="/data/disk1/iot-tv/experiments/results/"
lg_folder="LG_tv/lg_tv/IMC"
samsung_folder="samsung_TV/samsung_tv/IMC"

for folder1 in "$pcap_folder$lg_folder"/*; do
    folder1_basename=$(basename "$folder1")
    if [[ $folder1_basename != "CSVs" ]]; then # && [[ $folder1_basename != "login-optin" ]] && [[ $folder1_basename != "logout-optin" ]]; then
        echo $folder1_basename
        for folder2 in "$folder1"/*; do
            folder2_basename=$(basename "$folder2")
            for pcap in "$folder2"/*.pcap; do
                pcap_basename=$(basename "$pcap")
                if [[ $pcap_basename == *"LG"* ]]; then
                    echo "Processing $pcap"
                    ./run.sh "$pcap" "$pcap_folder$lg_folder/CSVs/US/LG-$folder2_basename-$folder1_basename.csv" 10.42.0.97
                else
                    echo "Processing $pcap"
                    ./run.sh "$pcap" "$pcap_folder$lg_folder/CSVs/UK/LG-$folder2_basename-$folder1_basename.csv" 18.10.0.3
                fi
            done
         done
    fi
done
for folder3 in "$pcap_folder$samsung_folder"/*; do
    folder3_basename=$(basename "$folder3")
    if [[ $folder3_basename != "CSVs" ]]; then
        for folder4 in "$folder3"/*; do
            folder4_basename=$(basename "$folder4")
            for pcap in "$folder4"/*.pcap; do
                pcap_basename=$(basename "$pcap")
                if [[ $pcap_basename == *"Samsung"* ]]; then
                    echo "Processing $pcap"
                    ./run.sh "$pcap" "$pcap_folder$samsung_folder/CSVs/US/SM-$folder4_basename-$folder3_basename.csv" 10.42.0.233
                else
                    if [[ $folder4_basename == "screen_casting" ]]; then
                        echo "Processing $pcap"
                        ./run.sh "$pcap" "$pcap_folder$samsung_folder/CSVs/US/SM-$folder4_basename-$folder3_basename.csv" 18.10.0.7
                    else
                        echo "Processing $pcap"
                        ./run.sh "$pcap" "$pcap_folder$samsung_folder/CSVs/UK/SM-$folder4_basename-$folder3_basename.csv" 10.20.0.2
                    fi
                fi
            done
         done
    fi
done
