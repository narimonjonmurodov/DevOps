#!/bin/bash
log_dir="$(dirname $0)/../04"
path="$(dirname $0)/main.sh"

CHECK() {
if [ $# -ne 1 ]
then
   echo "Error: Script run with 1 parametr"
   echo "For extra info $path --help"
   return 1
elif [[ $1 == "--help" ]]
then
   cat README.txt
   return 1
elif ! [[ $1 =~ ^[1-2]$ ]]
then
   echo "Error(1st Parametr): should be number [1-2] "
   return 1
fi
}

CHECK_LOGS() {
if ! ls "$log_dir"/nginx_log_day*.log 1> /dev/null 2>&1; then
    echo "Error: No nginx log files found in $log_dir directory"
    return 1
fi

awk '!($1 ~ /^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$/ && $9 ~ /^[0-9]{3}$/)' "$log_dir"/nginx_log_day*.log | head -1 | grep -q .
if [ $? -eq 0 ]; then
    echo "Error: Log format is invalid in $log_dir directory"
    return 1
fi
}

GO_INS() {
if ! command -v goaccess &> /dev/null; then
   echo "Installing GoAccess..."
   sudo apt install -y goaccess
fi
}
