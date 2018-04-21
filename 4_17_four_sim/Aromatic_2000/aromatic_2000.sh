#!/bin/bash
# file name: aromatic_2000.sh

echo "Starting CONDOR job"
echo "JobId: $1"
python Wrapper_ConstantP_Sweep_Step2_aro_2000.py $1
echo "Finishing..."

