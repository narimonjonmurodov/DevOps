#!/bin/bash

GATEWAY(){
 echo "GATEWAY = $(ip r | grep default | awk '{print $3}' | head -n1)"
}

RAM_TOTAL() {
echo "RAM_TOTAL = $(awk '/MemTotal/ {printf "%.3f GB", $2/1024/1024}' /proc/meminfo)"
}

RAM_USED() {
total=$(awk '/MemTotal/ {print $2}' /proc/meminfo)
avail=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
used=$(awk "BEGIN{printf \"%.3f\", ($total - $avail)/1024/1024}")
echo "RAM_USED = $used GB"
}

RAM_FREE() {
echo "RAM_FREE = $(awk '/MemAvailable/ {printf "%.3f GB", $2/1024/1024}' /proc/meminfo)"
}

SPACE_ROOT() {
echo "SPACE_ROOT = $(df / | awk 'NR==2{printf "%.2f", $2/1024}') MB"
}

SPACE_ROOT_USED() {
echo "SPACE_ROOT_USED = $(df / | awk 'NR==2{printf "%.2f", $3/1024}') MB"
}

SPACE_ROOT_FREE() {
echo "SPACE_ROOT_FREE = $(df / | awk 'NR==2{printf "%.2f", $4/1024}') MB"
}
