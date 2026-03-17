#!/bin/bash

CHECK() {
path="$(dirname $0)/main.sh"
if [ $# -ne 1 ]
then
   echo "Error: Script run with 1 parametr"
   echo "For extra info $path --help"
   return 1

elif [[ $1 == "--help" ]]
then
   cat "$(dirname $0)/requirements.txt"
   return 1

elif ! [[ $1 =~ ^[1-4]$ ]]
then
   echo "Error(1st parametr): Invalid parameter. Use 1, 2, 3 or 4 !"
   echo "For extra info $path --help"
   return 1

fi
}

CHECK_LOGS() {
log_dir="$(dirname $0)/../04"

if ! ls "$log_dir"/nginx_log_day*.log 1> /dev/null 2>&1; then
    echo "Error: No nginx log files found in $log_dir directory"
    return 1
fi

awk '!($1 ~ /^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$/ && $9 ~ /^[0-9]{3}$/)' "$log_dir"/nginx_log_day*.log | head -1 | grep -q .
if [ $? -eq 0 ]; then
    echo "Error: Log format is invalid in $log_dir directory"
    exit 1
fi
}
