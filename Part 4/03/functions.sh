#!/bin/bash
source "$(dirname $0)/extra_check.sh"
temp="$(dirname $0)/narimon.txt"

REMOVE() {
while [ $# -ne 0 ]
do
  rm -rf $1 2>/dev/null
  shift
done
}

FOLDER() {
paths=""

while read path date size
do
   if [[ ${path::1} == "/" ]] && [[ ${path: -6: 6} =~ ^[0-9]+$ ]]
   then
      paths+="$path "
   fi
done < $1
}

P1() {
log=$(LOG_CHECK) || return 1
FOLDER $log
REMOVE $paths
}

P2() {
read -p "Start time: " start
read -p "End time: " end
TIME_CHECK "$start" "$end" || return 1
find / -newermt "$start" ! -newermt "$end" 2>/dev/null  1>$temp
FOLDER $temp
REMOVE $paths $temp
}
