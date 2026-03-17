#!/bin/bash

source "$(dirname $0)/check.sh"
source "$(dirname $0)/functions.sh"
source "$(dirname $0)/functions1.sh"


CHECK $@ || exit 1

case $1 in
   1) P1 || exit 1 ;;
   2) P2 || exit 1 ;;
   3) P3 || exit 1 ;;
esac
