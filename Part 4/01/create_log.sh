#!/bin/bash

LOG() {
folder="$(dirname $0)/log"
mkdir -p $folder
file="$(date +%d.%m.%Y_%H-%M-%S).log"
echo "full path       creation date       file size" > "$folder/$file"
echo "$folder/$file"
}
