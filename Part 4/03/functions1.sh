#!/bin/bash
source "$(dirname $0)/functions.sh"

CHECK_MASK() {
if [[ "$1" =~ ^[a-zA-Z]{1,7}_[0-9]{6}$ ]]; then
   date_part=${1: -6: 6}
   name_part=${1::-7}
   if date -d "${date_part:0:2}-${date_part:2:2}-${date_part:4:2}" >/dev/null 2>&1; then
      return 0
   fi
fi
    echo "Error: Invalid input. Pattern should be: [1–7 letters]_[real date in ddmmyy]"
    echo "Please run $(dirname $0)/main.sh --help for extra info"
    return 1
}

P3() {
read -p "Mask: " mask
CHECK_MASK $mask || return 1
first="${name_part::1}"
last="${name_part: -1}"
regex=".*/${first}*${name_part}${last}*_$date_part"
find / -regextype posix-extended -regex $regex 2>/dev/null 1>$temp
FOLDER $temp
REMOVE $paths $temp
}
