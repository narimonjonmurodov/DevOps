#!/bin/bash

CREATING_DIR() {
log_file=$2
mkdir $1
echo "$1       $(date)" >> $log_file
}

CREATING_FILE() { # last_index=log_file last_2nd_index=size
log_file="${!#}" # log file
last_second_index=$(( $# - 1 )) # last second index for size like: 10KB
file_size=${!last_second_index}
size="${file_size::-2}"
# size should be in K(kilobites)

while [ $# -gt 2 ]; do
  space=$(df -k / | awk 'NR==2 {print $4}')
  remaining=$(( space - size ))
  if [ $remaining -le 1048576 ]
  then
     echo "Error: Less than 1GB of free space left in / partition!"
     return 1
  fi
  fallocate -l $size"K" $1
  echo "$1       $(date)       $file_size " >> $log_file
  shift
done

}
