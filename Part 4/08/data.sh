#!/bin/bash
DATA() {
if [ $# -ne 1 ]
then
   echo "Error: Script runs with only 1 parametr!"
   echo "Please run ./main --help for extra info"
   exit 1
fi

case $1 in
--help)
   cat $(dirname $0)/README.txt
;;

--check)
   CHECK
;;

1)
   install_prometheus
;;

2)
   install_node_exporter
;;

3)
   install_grafana
;;

--all)
   install_prometheus
   install_node_exporter
   install_grafana
;;

*)
   echo "Error(1st Parametr): Please run ./main --help for extra info"
   exit 1
;;
esac
}
