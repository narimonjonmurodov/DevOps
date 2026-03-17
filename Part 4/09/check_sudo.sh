#!/bin/bash

CHECK_SUDO() {
if [ -n "$SUDO_USER" ] || [ "$EUID" -eq 0 ]
then
   return 0
else
   echo "Error: Permission denied!"
   echo "Please run code with sudo or as a root"
   return 1
fi
}
