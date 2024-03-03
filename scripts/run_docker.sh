#!/bin/bash
ROOT_DIR="$(dirname "$(realpath "$0")")/.."
BASE_OPTS="-p 80:8080 --rm -e IS_DEV=1 --name python-scraper python-scraper"
EXTRA_OPTS="--volume $ROOT_DIR/scrape:/var/task/scrape"

if [ -n "$PROJECT_ROOT" ]; then
    for entry in $(cat "$PROJECT_SOURCES_FILE"); do
        EXTRA_OPTS="$EXTRA_OPTS --volume $PROJECT_ROOT/$entry:/var/task/$entry"
    done
else
    EXTRA_OPTS="$EXTRA_OPTS --volume $ROOT_DIR/main.py:/var/task/main.py"
fi


docker run --platform=linux/"$1" $EXTRA_OPTS $BASE_OPTS
