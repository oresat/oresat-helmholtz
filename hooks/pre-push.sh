#!/bin/sh

# Utils
function die() {
    RC=$2
    if [[ -z $RC ]]; then RC="-1"; fi
    echo -e "Hook failed <rc: $RC> with reason: $1"
    exit $RC
}

# Determine the source directory
MAX_LINE_LEN=100
SRC_DIR=$(git config hooks.srcDir)
if [[ -z $SRC_DIR ]]; then SRC_DIR="$PWD/src"; fi

# Format code
black --line-length $MAX_LINE_LEN $SRC_DIR
RC=$?
if [[ $RC -ne 0 ]]; then die "Black failed to complete formatting!" $RC; fi

# Lint code
python3 -m flake8 --max-line-length $MAX_LINE_LEN $SRC_DIR
RC=$?
if [[ $RC -ne 0 ]]; then die "Flake8 failed linting check!" $RC; fi