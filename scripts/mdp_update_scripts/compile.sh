#!/bin/bash

# Check to be inside scripts/mdp_update_experiments
if [[ "$PWD" != */scripts/mdp_update_scripts ]]; then
    echo "Make sure to run this script from inside scripts/mdp_update_scripts"
    exit
fi

# -- COMPILE TONIC
echo "Compiling Tonic code..."
cd code
rm -rf Tonic-build
mkdir Tonic-build
cd Tonic-build
ls
cmake ../../../..
make
cd ../../