#!/bin/bash
# file name: aro_1000.sh

echo "Starting CONDOR job"
echo "JobId: $1"
python Wrapper_Aromatic_1000rpm_step4_Condor.py $1
echo "Finishing..."

