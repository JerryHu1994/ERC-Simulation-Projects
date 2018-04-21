#!/bin/bash
# file name: Wiebe_Condor.sh

echo "Starting Wiebe CONDOR job"
echo "$1"
python Ignition_Delay_Temp_ALG.py $1
echo "Finishing..."

