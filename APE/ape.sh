#!/bin/bash

# Resolve the directory this script lives in (even if symlinked)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

SWIPL_EXEC="swipl"
APE_FILE="$SCRIPT_DIR/ape.pl"

# Run APE using SWI-Prolog with passed arguments
exec "$SWIPL_EXEC" -f "$APE_FILE" -g "ape,halt" -- "$@"

