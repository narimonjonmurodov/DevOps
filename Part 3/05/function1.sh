#!/bin/bash
NUM_FOLDERS() {
n=$(du $1 2>/dev/null | wc -l)
echo "Total number of folders (including all nested ones) = $(($n-1))"
}

FOLDERS_LARGEST_SIZE() {
n=1
echo "TOP 5 folders of maximum size arranged in descending order (path and size):"
du -h $1 2>/dev/null | grep -v "$1"$ | sort -hr | head -n 5 | while read size folder
do
   echo "$n - $folder, ${size::-1} ${size: -1}B"
   n=$(($n + 1))
done
}

NUM_FILES() {
num_f=$(find "$1" -type f 2>/dev/null | wc -l)
echo "Total number of files = $num_f"
}

NUM_OF() {
conf=$(find "$1" -type f -name "*.conf" 2>/dev/null | wc -l)
log=$(find "$1" -type f -name "*.log" 2>/dev/null | wc -l)
text=$(find "$1" -type f -exec file {} \; 2>/dev/null | grep -i text | wc -l)
exe=$(find "$1" -type f -executable 2>/dev/null | wc -l)
arch=$(find "$1" -type f \( -name "*.zip" -o -name "*.tar" -o -name "*.gz" -o -name "*.rar" \) 2>/dev/null | wc -l)
link=$(find "$1" -type l 2>/dev/null| wc -l)
echo "Number of:"
echo "Configuration files (with the .conf extension) = $conf"
echo "Text files = $text"
echo "Executable files = $exe"
echo "Log files (with the extension .log) = $log"
echo "Archive files = $arch"
echo "Symbolic links = $link"
}
