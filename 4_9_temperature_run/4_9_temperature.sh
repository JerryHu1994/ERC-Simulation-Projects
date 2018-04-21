#!/bin/bash
# file name: 4_9_temperature.sh

echo "Starting CONDOR job"
echo "JobId: $1"
python Wrapper_constantmass_Sweep_CONDOR.py $1
echo "Finishing..."

