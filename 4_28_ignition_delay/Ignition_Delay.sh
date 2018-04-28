#!/bin/bash
# file name: Ignition_Delay.sh

echo "Starting Wiebe CONDOR job"
echo "Jobid: $1"
python Ignition_Delay_Temp_ALG_CONDOR_alkylate $1
echo "Finishing..."

