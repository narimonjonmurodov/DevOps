#!/bin/bash

FILE_COUNTER() {
date=$(date +%d%m%y)
count_files=$(ls -ld $1*$date 2>/dev/null | wc -l)
default_folders="$(ls -d $1*$date 2>/dev/null)"
}

ALLOWED() {
list=()
while [ $# -ne 0 ]
do
  if [ -e $1 ] && [ -w $1 ]
  then
    list+=("$1")
  fi
  shift
done
}
