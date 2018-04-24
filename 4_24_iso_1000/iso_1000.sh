#!/bin/bash
# file name: iso_1000.sh

echo "Starting CONDOR job"
echo "JobId: $1"
python Wrapper_Iso_1000rpm_CONDOR_Step4.py $1
echo "Finishing..."

