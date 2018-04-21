#!/bin/bash
# file name: iso_2000.sh

echo "Starting CONDOR job"
echo "JobId: $1"
python Wrapper_constantmass_Sweep_CONDOR_Wiebe.py $1
echo "Finishing..."

