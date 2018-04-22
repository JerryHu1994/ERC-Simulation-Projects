#!/bin/bash
# file name: aro_2000.sh

echo "Starting CONDOR job"
echo "JobId: $1"
python Wrapper_Aromatic_2000rpm_step4_CONDOR.py $1
echo "Finishing..."

