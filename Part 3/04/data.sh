#!/bin/bash

source "$(dirname $0)/function1.sh"
source "$(dirname $0)/function2.sh"
source "$(dirname $0)/function3.sh"

DATA() {
HOSTNAME
TIMEZONE
USER
OS
DATE
UPTIME
UPTIME_SEC
IP
MASK
GATEWAY
RAM_TOTAL
RAM_USED
RAM_FREE
SPACE_ROOT
SPACE_ROOT_USED
SPACE_ROOT_FREE
}
