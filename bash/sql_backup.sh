#!/bin/bash

docker exec -t mattfm_sql pg_dumpall -c -U $1 > $1/dump_`date +%d-%m-%Y"_"%H_%M_%S`.sql