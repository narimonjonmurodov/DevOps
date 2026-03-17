#!/bin/bash

TIME_CHECK() {
script="$(dirname $0)/main.sh"
while [ $# -gt 0 ]
do
  if date -d "$1" "+%Y-%m-%d %H:%M" >/dev/null 2>&1; then
    shift
  else
     echo "Error: Invalid date!"
     echo "Please run $script --help  for extar info!"
     return 1
  fi
done
}

LOG_CHECK() {
path="$(dirname "$0")/../02/"
count=$(ls -l "$path"*.log 2>/dev/null | wc -l )
if [ "$count" -gt 1 ]
then
  echo "Error: you have more than 1 logfiles in $path " >&2
  echo "Please delate not related logfiles from Task 2 !" >&2
  return 1
elif [ $count -eq 1 ]
then
  file=$(ls "$path"*.log)
else
  echo "Error: you have no log file in $path" >&2
  echo "Please make sure you did Task 2 and provide correct log !" >&2
  return 1
fi

echo $file
}

