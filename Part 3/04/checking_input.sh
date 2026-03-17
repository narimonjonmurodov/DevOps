#!/bin/bash

CHECK() {

if [[ $# -ne 4 ]]; then
  return 2
fi

for param in "$@"
do
  if ! [[ $param =~ ^[1-6]$ ]]; then
    echo "Error: The parameters should be numeric. From 1 to 6. Please run the script again."
    echo "Please edit config.conf"
    return 1
    fi
done

if [[ $1 -eq $2 || $3 -eq $4 ]]; then
  echo "Error: The font and background colours of one column must not match. Please run the script again."
  echo "Please edit config.conf"
  return 1
fi

}
