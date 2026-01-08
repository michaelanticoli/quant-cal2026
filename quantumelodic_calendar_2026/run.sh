#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 setup_and_run.py "$@"
