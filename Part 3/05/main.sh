#!/bin/bash

START=$(date +%s.%N)

source "$(dirname $0)/check_input.sh"
source "$(dirname $0)/function1.sh"
source "$(dirname $0)/function2.sh"

CHECK $@ || exit 1
NUM_FOLDERS $@
FOLDERS_LARGEST_SIZE $@
NUM_FILES $@
NUM_OF $@
FILES_LARGEST_SIZE $@
EXE_LARGEST_SIZE $@

END=$(date +%s.%N)
EXEC_TIME=$(echo "$END - $START" | bc)
echo "Script execution time (in seconds) = $EXEC_TIME"
