#!/bin/bash
set -euo pipefail

tempdir="$(mktemp -d)"
cleanup () {
    CODE=$?
    rm -rd "$tempdir"
    exit $CODE
}
trap cleanup EXIT

PYTHON_PKG_DIR=python/lib/python3.12/site-packages/

python3 -m venv "$tempdir"/env
. "$tempdir"/env/bin/activate

cp requirements.txt "$tempdir"/requirements.txt
if [ -n "$PROJECT_ROOT" ] && [ -f "$PROJECT_ROOT"/requirements.txt ]; then
    cat "$PROJECT_ROOT"/requirements.txt >> "$tempdir"/requirements.txt
fi

pip install \
--platform manylinux2014_x86_64 \
--target="$tempdir"/"$PYTHON_PKG_DIR" \
--implementation cp \
--python-version 3.12 \
--only-binary=:all: --upgrade \
-r "$tempdir"/requirements.txt

pushd "$tempdir" > /dev/null
zip -r py_deps_layer.zip "$PYTHON_PKG_DIR"
popd > /dev/null

mkdir -p layers/
cp "$tempdir"/py_deps_layer.zip layers/
