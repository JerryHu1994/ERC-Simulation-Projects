#!/bin/bash
# file name: Ignition_Delay.sh

echo "Starting Ignition Delay CONDOR job"
echo "Jobid: $1"
python Ignition_Delay_Temp_ALG_CONDOR_alkylate.py $1
echo "Finishing..."

