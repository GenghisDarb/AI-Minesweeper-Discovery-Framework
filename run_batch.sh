#!/bin/bash
if command -v wolfram &> /dev/null
then
    echo "Wolfram Engine detected. Running batch scripts..."
    wolfram -script wolfram/run_all.wls
else
    echo "Wolfram Engine not found. Using pre-generated files."
fi
