#!/bin/bash

FILES_LARGEST_SIZE() {
echo "TOP 10 files of maximum size arranged in descending order (path, size and type):"
n=1
find "$1" -type f -exec du -h {} + 2>/dev/null | sort -hr | head -n 10 | while read size path
do
   if [[ "$path" == *.* ]]
   then
      type="${path##*.}"
   else
      type=$(file -b "$path" | awk -F',' '{print $1}')
   fi
   echo "$n - $path, ${size::-1} ${size: -1}B, $type"
   n=$(($n + 1))
done
}

EXE_LARGEST_SIZE() {
echo "TOP 10 executable files of the maximum size arranged in descending order (path, size and MD5 hash of file):"
n=1
find "$1" -type f -executable -exec du -h {} + 2>/dev/null | sort -hr | head -n 10 | while read size path
do
   hash=$(md5sum "$path" | awk '{print $1}')
   echo "$n - $path, ${size::-1} ${size: -1}B, $hash"
   n=$(($n + 1))
done
}
