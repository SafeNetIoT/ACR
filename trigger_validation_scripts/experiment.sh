#!/bin/bash

# Setting up variables
repeat_times=1

   # Read the parameters from the file
    echo "Reading parameters from the file..."

IFS="." read -r prefix suffix <<< "$1"
RESULT_FILE="/data/disk1/iot-tv/experiments/results/${prefix}_results.txt" # File for recording the results
PHONE="pixel3A_5" # The phone  ids/phone

TRAFFIC_DIR="/data/disk1/iot-tv/experiments/results" # File for saving pcap file

# Function to wait for the phone to be ready
function waitphone {
    while [ -z "$PHONE_FOUND" ]; do
        echo "Phone not found, waiting for $PHONE/$ANDROID_SERIAL"
        sleep 5
        PHONE_FOUND=$(adb devices | grep "$ANDROID_SERIAL")
    done
}


# Check if the phone's id file exists
if [ ! -f "ids/$PHONE" ]; then
    echo "Devices ids/$PHONE does not exist. Aborting."
    exit 1
else
    # If it exists, get the phone's ID
    export ANDROID_SERIAL=$(cat "ids/$PHONE")
    echo "Phone is: $PHONE/$ANDROID_SERIAL"
    PHONE_FOUND=$(adb devices | grep "$ANDROID_SERIAL" | grep device)
    waitphone
    echo "Phone ready, proceeding..."
fi


# Main loop
for ((i=0; i<repeat_times; i++)); do
    echo "Experiment $((i+1))"

if [ "$1" == "exp_samsung.txt" ]; then
	while IFS=";" read name name_exp package mac_address crop_info tap1 tap2 tap3 tap4
	do
    		# Get the current date and time for each iteration
    		DATE=$(date "+%m%d_%H%M%S") # The current date and time

    		# Start the monitor
    		cd /opt/moniotr
    		/opt/moniotr/bin/tag-experiment.sh cancel "$mac_address" "$name"
    		sleep 5
    		/opt/moniotr/bin/tag-experiment.sh start "$mac_address" "$name"
    		sleep 5

    		# Close app before opening it
    		adb shell am force-stop "$package"

    		# Launch the app
    		adb shell -n monkey -p "$package" -c android.intent.category.LAUNCHER 1
    		sleep 5

		# If it is the first time after the TV has been reset, go manually on the kids channel and switch off the TV
        	adb shell input swipe 500 1000 300 300
                sleep 10s
                adb shell -n input "$tap1" # Choose remote control
        	sleep 5s
        	adb shell -n input "$tap2" # Switch on
        	sleep 15s # Time for switching on the TV
		sleep "$(( $2 * 60 ))s" # How long staying on the channel
		adb shell am force-stop "$package" # Closing the app 
		adb shell -n monkey -p "$package" -c android.intent.category.LAUNCHER 1 # Reopening the app for running all the TVs simultaneously
                sleep 10s
                adb shell input swipe 500 1000 300 300
                sleep 10s
		adb shell -n input "$tap3" # Choosing the remote again
		sleep 5s
        	adb shell -n input "$tap4" # Switch off
		echo "The experimental operations have finished, taking a screenshot…"

    		# Stop the monitor
    		/opt/moniotr/bin/tag-experiment.sh stop "$mac_address" "$name" "$TRAFFIC_DIR"
    		sleep 10s

		# In the result folder, it creates a folder with the name of the device on devices.txt
                device_name_folder=$(grep -i "$mac_address" "/opt/moniotr/etc/devices.txt" | awk '{print $2}')

                # folder path where the pcap has been created
                FOLDER_PATH="${TRAFFIC_DIR}/${device_name_folder}/${name}"

                # Assuming $FILE_EXTENSION contains the file extension you want to filter
                FILE_EXTENSION=".pcap"

                # Getting the pcap file (the last created)
                pcap=$(find "$FOLDER_PATH" -type f -name "*$FILE_EXTENSION" -printf "%T@ %p\n" | sort -n -r | head -n 1 | cut -d " " -f 2-)

                # Getting size of pcap file
                PCAP_SIZE=$(wc -c "${pcap}" | awk '{print $1}')

    		# Checking the sizeof the pcap file for understanding whether the experiments is successful ***decide threshold***
    		if ((PCAP_SIZE > 1000000)); then
        		result_msg="Successful"
        		echo "Experiment $((i+1)) is successful."
    		else
        		result_msg="Failure"
        		echo "Experiment $((i+1)) is failure."
    		fi
    		# Save the result to the file
    		echo -e "Experiment: $((i+1)), Date: $DATE, Result: $result_msg" >> "$RESULT_FILE"
    		echo "Experiment $((i+1)) completed."
    		echo
	done < $1
elif [ "$1" == "exp_lg.txt" ]; then
	while IFS=";" read name name_exp package mac_address crop_info tap1 tap2 tap3 tap4 tap5 tap6
        do
		# Get the current date and time for each iteration
                DATE=$(date "+%m%d_%H%M%S") # The current date and time

                # Start the monitor
                cd /opt/moniotr
                /opt/moniotr/bin/tag-experiment.sh cancel "$mac_address" "$name"
                sleep 5
                /opt/moniotr/bin/tag-experiment.sh start "$mac_address" "$name"
                sleep 5

                # Close app before opening it
                adb shell am force-stop "$package"

                # Launch the app
                adb shell -n monkey -p "$package" -c android.intent.category.LAUNCHER 1
                sleep 5

                # If it is the first time after the TV has been reset, go manually on the kids channel and switch off the TV
                adb shell input swipe 500 1000 300 300
                sleep 10s
                adb shell -n input "$tap1" # Choose remote control
                sleep 5s
                adb shell -n input "$tap2" # Switch on
		#sleep 5s
		#adb shell -n input "$tap3" # Home
                #sleep 5s
		#adb shell -n input "$tap4" # OK
                sleep 15s # Time for opening the app
                sleep "$(( $2 * 60 ))s" # How long staying on the channel
		adb shell am force-stop "$package" # Closing the app
		adb shell -n monkey -p "$package" -c android.intent.category.LAUNCHER 1 # Reopening the app for running all the TVs simultaneously
                sleep 10s
                adb shell input swipe 500 1000 300 300
                sleep 10s
                adb shell -n input "$tap5" # Choosing the remote again
                sleep 5s
                adb shell -n input "$tap6" # Switch off
                echo "The experimental operations have finished, taking a screenshot…"

                # Stop the monitor
                /opt/moniotr/bin/tag-experiment.sh stop "$mac_address" "$name" "$TRAFFIC_DIR"
                sleep 10s

                # In the result folder, it creates a folder with the name of the device on devices.txt
                device_name_folder=$(grep -i "$mac_address" "/opt/moniotr/etc/devices.txt" | awk '{print $2}')

                # folder path where the pcap has been created
                FOLDER_PATH="${TRAFFIC_DIR}/${device_name_folder}/${name}"

                # Assuming $FILE_EXTENSION contains the file extension you want to filter
                FILE_EXTENSION=".pcap"

                # Getting the pcap file (the last created)
                pcap=$(find "$FOLDER_PATH" -type f -name "*$FILE_EXTENSION" -printf "%T@ %p\n" | sort -n -r | head -n 1 | cut -d " " -f 2-)

		# Getting size of pcap file
                PCAP_SIZE=$(wc -c "${pcap}" | awk '{print $1}')

                # Checking the sizeof the pcap file for understanding whether the experiments is successful ***decide threshold***
                if ((PCAP_SIZE > 1000000)); then
                        result_msg="Successful"
                        echo "Experiment $((i+1)) is successful."
                else
                        result_msg="Failure"
                        echo "Experiment $((i+1)) is failure."
                fi
                # Save the result to the file
                echo -e "Experiment: $((i+1)), Date: $DATE, Result: $result_msg" >> "$RESULT_FILE"
                echo "Experiment $((i+1)) completed."
                echo
        done < $1
fi
done
