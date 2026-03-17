#!/bin/bash

CHECK(){
PROM_SERVICE="prometheus"
GRAFANA_SERVICE="grafana-server"
NODE_EXPORTER_BIN="/usr/local/bin/node_exporter"
f=1
if ! ( systemctl list-unit-files | grep -q "$PROM_SERVICE" ); then
   echo "Prometheus NOT installed"
   echo "Please install Prometheus!"
   f=0
fi

if ! [ -f "$NODE_EXPORTER_BIN" ]; then
   echo "Node Exporter is not  installed"
   echo "Please install Node Exporter!"
   f=0
fi

if ! ( systemctl list-unit-files | grep -q "$GRAFANA_SERVICE" ); then
   echo "Grafana NOT installed"
   echo "Please install Grafana!"
   f=0
fi

if [ $f -eq 1 ]
then
   echo "Everything is installed"
   exit 0
fi

}
