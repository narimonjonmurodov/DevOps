#!/bin/bash
source "$(dirname $0)/check.sh"
source "$(dirname $0)/Prometheus.sh"
source "$(dirname $0)/node_exp_install.sh"
source "$(dirname $0)/Grafana.sh"
source "$(dirname $0)/data.sh"

DATA $@
