#!/usr/bin/env bash

trap "trap - SIGTERM && echo KILLING && kill -- -$$" SIGINT SIGTERM EXIT

RECIPE_HOST=${RECIPE_HOST:-0.0.0.0}
RECIPE_PORT=${RECIPE_PORT:-8000}
export RUKO_HOST=0.0.0.0
export RUKO_PORT=33633

ruko-server --file data.db $RUKO_HOST:$RUKO_PORT --log-level info &

source .venv/bin/activate
gunicorn -b "$RECIPE_HOST:$RECIPE_PORT" "$@" recipe_server:app

