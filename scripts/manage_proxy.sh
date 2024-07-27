#!/bin/bash

# 현재 스크립트의 디렉토리 경로를 가져옴
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../" && pwd)"

# Python 스크립트 실행
python3 "$SCRIPT_DIR/python/manage_services.py"
