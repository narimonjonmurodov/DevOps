#!/bin/bash
source "$(dirname $0)/data.sh"
source "$(dirname $0)/file_saver.sh"

if [ $# -ne 0 ]
then
echo "Error: This script must be run without parameters."
exit 1
fi

DATA

SAVE_FILE
