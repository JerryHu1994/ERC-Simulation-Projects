#!/bin/bash
# file name: alk_1000.sh

echo "Starting CONDOR job"
echo "JobId: $1"
python Wrapper_ConstantP_Sweep_Step2_alk_1000.py $1
echo "Finishing..."

