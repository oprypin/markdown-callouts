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
python -c 'import sys, os; sys.exit((3,8) <= sys.version_info < (3,10) and os.name == "posix")' ||
"$@" pytype markdown_callouts
