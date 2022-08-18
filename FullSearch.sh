#!/bin/bash

sMDT_path="/Users/evan/Google Drive/Shared Drives/sMDT Tube Testing Reports"
read -n1 -p "Tension or DC? [t/d]: " T_DC
printf "\n"
read -n9 -p "ID: " tubeID # reads in 9 characters, -p menas it is a prompt, so assign the input to a variable (tubeID here)

while [ "$tubeID" != "stop" ]
do
    case $T_DC in 
        t) 
        grep -rh --exclude='*.gdoc' $tubeID "$sMDT_path"/TubeTension | awk 'BEGIN{FS="\t"} {print $1,$2,$7}';; 
        d)
        find -name "$sMDT_path"/CAEN/*.log -exec head -n 20 {} ";" | grep -r --exclude='*.gdoc' $tubeID  ;;
    esac
    read -n9 -p "ID: " tubeID
done