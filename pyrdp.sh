#!/bin/bash

if [ -L "$0" ]; then
   BASE_DIR="$(dirname $(readlink $0))";
else
   BASE_DIR="$(dirname $0)";
fi

export PYTHONPATH="$PYTHONPATH":"$BASE_DIR"

python "$BASE_DIR"/pyrdp/main.py "$@" &