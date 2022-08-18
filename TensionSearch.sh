#!/bin/bash

sMDT_path="/Users/evan/Google Drive/Shared Drives/sMDT Tube Testing Reports"

read -n9 -p "ID: " tubeID # reads in 9 characters, -p menas it is a prompt, so assign the input to a variable (tubeID here)

while [ "$tubeID" != "stop" ]
do
    grep -rh --exclude='*.gdoc' $tubeID "$sMDT_path"/TubeTension | awk 'BEGIN {FS="\t"} {print $1,$2,$7}'
	#grep $tubeID "$sMDT_path"/CAEN/Processed/*.log
    read -n9 -p "ID: " tubeID
done