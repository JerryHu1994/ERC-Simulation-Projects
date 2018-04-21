#!/bin/bash
# file name: Alk_1000.sh

echo "Starting CONDOR job"
echo "JobId: $1"
python Wrapper_Alkylate_1000rpm_step4_CONDOR.py $1
echo "Finishing..."

