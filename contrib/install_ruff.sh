#!/bin/bash -e

if [[ $1 == "-f" ]] || [[ $1 == "--force" ]]; then
    force=y
fi

VERSION=${VERSION:-"0.14.0"}
FILENAME="ruff-x86_64-unknown-linux-gnu.tar.gz"
URL="https://github.com/astral-sh/ruff/releases/download/$VERSION/$FILENAME"

TMP_DIR="$(mktemp -d /tmp/ruff_XXXXX)"

if [[ -z $force ]] && command -v ruff >/dev/null; then
    echo "ruff already installed!"
    exit 1
fi

cd "$TMP_DIR"

wget "$URL"

tar -xvf "$FILENAME"
mv ./*/ruff /usr/local/bin/ruff

rm -r "$TMP_DIR"
