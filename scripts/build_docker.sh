#!/bin/bash
set -euo pipefail

requirements_file=merged-requirements.txt
cleanup () {
    CODE=$?
    rm -f "$requirements_file"
    exit $CODE
}
trap cleanup EXIT

cp requirements.txt "$requirements_file"
if [ -n "$PROJECT_ROOT" ] && [ -f "$PROJECT_ROOT"/requirements.txt ]; then
    cat "$PROJECT_ROOT"/requirements.txt >> "$requirements_file"
fi

docker build --platform linux/"$1" -f "$2" --build-arg requirements_file="$requirements_file" . -t python-scraper
