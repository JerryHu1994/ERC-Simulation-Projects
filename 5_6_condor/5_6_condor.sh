#!/bin/bash
# file name: 5_6_condor.sh

echo "Starting 5_6 CONDOR job"
echo "Jobid: $1"
python Thesis_IgDelay_wrapper_LLNL_Aromatic_Condor.py $1
echo "Finishing..."

