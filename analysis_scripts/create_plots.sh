#!/bin/bash

pcap_folder="/data/disk1/iot-tv/experiments/results/"
lg_folder="LG_tv/lg_tv/IMC/CSVs"
samsung_folder="samsung_TV/samsung_tv/IMC/CSVs"
input=$1
output_folder="/opt/moniotr/bin/iot-tv/analysis/network_traffic/IMC_PAPER/plots/"


if [[ $input == "1" ]]; then
    scenario="login-optin"
elif [[ $input == "2" ]]; then
    scenario="logout-optin"
elif [[ $input == "3" ]]; then
    scenario="login-optout"
elif [[ $input == "4" ]]; then
    scenario="logout-optout"
fi

for folder_country in "$pcap_folder$lg_folder"/*; do
    country=$(basename "$folder_country")
    for file in "$folder_country"/*; do
        file_basename=$(basename "$file")
        if [[ $file_basename == *"$scenario"* ]]; then
            if [[ $file_basename == *"antenna"* ]]; then
                file1="$file"
            elif [[ $file_basename == *"ctv_vendor"* ]]; then
                file2="$file"
            elif [[ $file_basename == *"home"* ]]; then
                file3="$file"
            elif [[ $file_basename == *"netflix"* ]]; then
                file4="$file"
            elif [[ $file_basename == *"youtube"* ]]; then
                file5="$file"
            elif [[ $file_basename == *"hdmi"* ]]; then
                file6="$file"
            elif [[ $file_basename == *"screen_casting"* ]]; then
                file7="$file"
            elif [[ $file_basename == *"gaming"* ]]; then
                file8="$file"
            fi
        fi
    done
    if [[ $country == "UK" ]]; then
        echo "python3 cumulative_time_series_per_scenario.py 7 "$file1" "$file2" "$file3" "$file4" "$file5" "$file6" "$file7" "$output_folder$country-$scenario-LG.png""
        python3 cumulative_time_series_per_scenario.py 7 "$file1" "$file2" "$file3" "$file4" "$file5" "$file6" "$file7" "$output_folder$country-$scenario-LG.png"
    elif [[ $country == "US" ]]; then
        echo "python3 cumulative_time_series_per_scenario.py 7 "$file1" "$file2" "$file3" "$file4" "$file5" "$file6" "$file8" "$output_folder$country-$scenario-LG.png""
#        python3 cumulative_time_series_per_scenario.py 7 "$file1" "$file2" "$file3" "$file4" "$file5" "$file6" "$file8" "$output_folder$country-$scenario-LG.png"
    fi
done

for folder_country2 in "$pcap_folder$samsung_folder"/*; do
    country2=$(basename "$folder_country2")
    for file in "$folder_country2"/*; do
        file_basename=$(basename "$file")
        if [[ $file_basename == *"$scenario"* ]]; then
            if [[ $file_basename == *"antenna"* ]]; then
                file9="$file"
            elif [[ $file_basename == *"ctv_vendor"* ]]; then
                file10="$file"
            elif [[ $file_basename == *"home"* ]]; then
                file11="$file"
            elif [[ $file_basename == *"netflix"* ]]; then
                file12="$file"
            elif [[ $file_basename == *"youtube"* ]]; then
                file13="$file"
            elif [[ $file_basename == *"hdmi"* ]]; then
                file14="$file"
            elif [[ $file_basename == *"screen_casting"* ]]; then
                file15="$file"
            elif [[ $file_basename == *"gaming"* ]]; then
                file16="$file"
            fi
        fi
    done
    if [[ $country2 == "UK" ]]; then
        echo "python3 cumulative_time_series_per_scenario.py 7 "$file9" "$file10" "$file11" "$file12" "$file13" "$file14" "$file15" "$output_folder$country2-$scenario-Samsung.png""
        python3 cumulative_time_series_per_scenario.py 7 "$file9" "$file10" "$file11" "$file12" "$file13" "$file14" "$file15" "$output_folder$country2-$scenario-Samsung.png"
    elif [[ $country2 == "US" ]]; then
        echo "python3 cumulative_time_series_per_scenario.py 7 "$file9" "$file10" "$file11" "$file12" "$file13" "$file14" "$file16" "$output_folder$country2-$scenario-Samsung.png""
#        python3 cumulative_time_series_per_scenario.py 7 "$file9" "$file10" "$file11" "$file12" "$file13" "$file14" "$file16" "$output_folder$country2-$scenario-Samsung.png"
    fi
done
