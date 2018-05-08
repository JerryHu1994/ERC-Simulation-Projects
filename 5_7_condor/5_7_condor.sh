#!/bin/bash
# file name: 5_7_condor.sh

echo "Starting 5_7 CONDOR job"
echo "Jobid: $1"
python Thesis_IgDelay_wrapper_LLNL_Iso.py $1
echo "Finishing..."

