#!/bin/bash
source "$(dirname $0)/check.sh"
source "$(dirname $0)/functions.sh"

CHECK $@ || exit 1
CHECK_LOGS || exit 1
GO_INS

case $1 in

1)
terminal_analysis
;;

2)
web_interface
;;

esac
