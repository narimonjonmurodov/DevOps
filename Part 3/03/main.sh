#!/bin/bash

source "$(dirname $0)/colours.sh"
source "$(dirname $0)/checking_input.sh"
source "$(dirname $0)/data.sh"

CHECK $@ || exit 1

DATA | while IFS= read -r line
do
  PRINT $@ "$line"
done
