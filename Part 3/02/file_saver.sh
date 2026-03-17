#!/bin/bash

source "$(dirname $0)/data.sh"

SAVE_FILE() {
echo -e "\nDo you want to save to file: Y/N"
read input
file="$(date +%d_%m_%y_%H_%M_%S).status"
if [[ $nput = "Y" || $input = "y" ]]
then
DATA > $file
echo "DATA saved in $file"
else
echo ""
fi
}
