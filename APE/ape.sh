#!/bin/bash

# Ensure we are in the directory containing ape.pl or adjust the path below
SWIPL_EXEC="swipl"
APE_FILE="ape.pl"

# Run APE using SWI-Prolog with passed arguments
$SWIPL_EXEC -f "$APE_FILE" -g "ape,halt" -- $@
