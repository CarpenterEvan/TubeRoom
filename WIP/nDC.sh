path="$HOME/Google Drive/Shared drives/sMDT Tube Testing Reports/CAEN"
find "$path"/*.log #-type d #-exec ls; #-name *test.log
awk 'FNR==16 {print FILENAME, $0}' "$path"/*test?.log #>$HOME/output.txt
#head -n 15 $f| tail -n 1;