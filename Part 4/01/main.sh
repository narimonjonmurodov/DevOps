#!/bin/bash
source "$(dirname $0)/check.sh"
source "$(dirname $0)/data.sh"

CHECK $@ || exit 1
DATA $@ || exit 1

