#!/bin/sh

# A simple smoke test to make sure everything we need in the container is
# working.

# Try importing our Python infrastructure.
python -c 'import tvm'
python -c 'import torch'

# Make sure the GraphIt compiler works.
cd graphit
./build/bin/graphitc -h
