#!/bin/sh
set -e

cd "$(dirname "$0")/.."

with_groups() {
    echo "::group::$@"
    "$@" && echo "::endgroup::"
}

"$@" autoflake -i -r --remove-all-unused-imports --remove-unused-variables markdown_callouts tests
"$@" isort -q markdown_callouts tests
"$@" black -q markdown_callouts tests
"$@" pytest -q
python -c 'import sys; sys.exit(sys.version_info >= (3,9))' ||
"$@" mypy markdown_callouts
