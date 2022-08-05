#!/bin/bash
sMDT_path="/Users/evan/Google Drive/Shared Drives/sMDT Tube Testing Reports"
read -n9 -p "ID: " tubeID
printf "\n"
read -n1 -p "Tension or DC? [t/d]: " T_DC
case $T_DC in 
    t) 
    printf "\n"
    grep -R $tubeID "$sMDT_path"/TubeTension/Processed/*.log ;;
    d) 
    printf "\n" 
    grep -R $tubeID "$sMDT_path"/CAEN/Processed/2022/2022_07/*.log
    grep -R $tubeID "$sMDT_path"/CAEN/Processed/2022/2022_06/*.log ;;
    #grep -l $tubeID "$sMDT_path"/CAEN/Processed/*.log | wc -l ;;
esac